"""
Main application window
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QMessageBox, QProgressBar, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from .drag_drop_area import DragDropArea
from .document_overview import DocumentOverview
from .modification_form import ModificationForm
from .styles import get_light_theme, get_dark_theme, get_drag_drop_styles
from ..processors.document_processor import DocumentProcessor
from ..config.settings import AppSettings

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, settings: AppSettings):
        super().__init__()
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.document_processor = DocumentProcessor()
        self.current_document = None
        
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.apply_theme()
        
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("WPDAdjuster - Word Processing Document Adjuster")
        self.setMinimumSize(1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Document overview and drag drop
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Drag drop area
        self.drag_drop_area = DragDropArea()
        self.drag_drop_area.file_dropped.connect(self.on_file_dropped)
        self.drag_drop_area.file_rejected.connect(self.on_file_rejected)
        left_layout.addWidget(self.drag_drop_area)
        
        # Document overview
        self.document_overview = DocumentOverview()
        self.document_overview.hide()  # Initially hidden
        left_layout.addWidget(self.document_overview)
        
        # Right panel - Modification form
        self.modification_form = ModificationForm()
        self.modification_form.hide()  # Initially hidden
        self.modification_form.settings_applied.connect(self.on_settings_applied)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.modification_form)
        splitter.setSizes([400, 600])  # Initial sizes
        
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open Document", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        theme_action = QAction("Toggle &Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(theme_action)
        
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        
        self.status_bar.showMessage("Ready - Drop a document to begin")
        
    def apply_theme(self):
        """Apply current theme"""
        theme_style = get_dark_theme() if self.settings.is_dark_theme else get_light_theme()
        drag_drop_style = get_drag_drop_styles()
        
        self.setStyleSheet(theme_style + drag_drop_style)
        
    def open_file_dialog(self):
        """Open file dialog for document selection"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Word Documents (*.docx);;RTF Documents (*.rtf);;All Files (*)"
        )
        
        if file_path:
            self.process_document(Path(file_path))
            
    def on_file_dropped(self, file_path: Path):
        """Handle file dropped event"""
        self.process_document(file_path)
        
    def on_file_rejected(self, error_message: str):
        """Handle file rejected event"""
        QMessageBox.warning(self, "Invalid File", error_message)
        
    def process_document(self, file_path: Path):
        """Process dropped or selected document"""
        self.logger.info(f"Processing document: {file_path}")
        self.status_bar.showMessage("Processing document...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Process document in thread to avoid UI freezing
        self.process_thread = DocumentProcessThread(file_path, self.document_processor)
        self.process_thread.document_processed.connect(self.on_document_processed)
        self.process_thread.error_occurred.connect(self.on_processing_error)
        self.process_thread.start()
        
    def on_document_processed(self, document_data: dict):
        """Handle successful document processing"""
        self.current_document = document_data
        self.logger.info("Document processed successfully")
        
        # Update UI
        self.document_overview.update_document(document_data)
        self.document_overview.show()
        
        self.modification_form.update_document(document_data)
        self.modification_form.show()
        
        self.drag_drop_area.hide()
        
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(f"Document loaded: {document_data.get('filename', 'Unknown')}")
        
    def on_processing_error(self, error_message: str):
        """Handle document processing error"""
        self.logger.error(f"Document processing error: {error_message}")
        QMessageBox.critical(self, "Processing Error", f"Failed to process document:\n{error_message}")
        
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Ready - Drop a document to begin")
        
    def on_settings_applied(self, settings: dict):
        """Handle modification settings applied"""
        if not self.current_document:
            return
            
        self.logger.info("Applying modification settings")
        self.status_bar.showMessage("Applying modifications...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        # Apply modifications in thread
        self.apply_thread = SettingsApplyThread(self.current_document, settings, self.document_processor)
        self.apply_thread.settings_applied.connect(self.on_settings_applied_success)
        self.apply_thread.error_occurred.connect(self.on_apply_error)
        self.apply_thread.start()
        
    def on_settings_applied_success(self, output_path: Path):
        """Handle successful settings application"""
        self.logger.info(f"Settings applied successfully: {output_path}")
        QMessageBox.information(self, "Success", f"Document modified and saved to:\n{output_path}")
        
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Settings applied successfully")
        
    def on_apply_error(self, error_message: str):
        """Handle settings application error"""
        self.logger.error(f"Settings application error: {error_message}")
        QMessageBox.critical(self, "Application Error", f"Failed to apply settings:\n{error_message}")
        
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage("Ready")
        
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.settings.theme = "dark" if self.settings.theme == "light" else "light"
        self.apply_theme()
        self.logger.info(f"Theme changed to: {self.settings.theme}")

class DocumentProcessThread(QThread):
    """Thread for processing documents"""
    document_processed = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, file_path: Path, processor: DocumentProcessor):
        super().__init__()
        self.file_path = file_path
        self.processor = processor
        
    def run(self):
        """Run document processing"""
        try:
            document_data = self.processor.process_document(self.file_path)
            self.document_processed.emit(document_data)
        except Exception as e:
            self.error_occurred.emit(str(e))

class SettingsApplyThread(QThread):
    """Thread for applying modification settings"""
    settings_applied = pyqtSignal(Path)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, document_data: dict, settings: dict, processor: DocumentProcessor):
        super().__init__()
        self.document_data = document_data
        self.settings = settings
        self.processor = processor
        
    def run(self):
        """Run settings application"""
        try:
            output_path = self.processor.apply_modifications(self.document_data, self.settings)
            self.settings_applied.emit(output_path)
        except Exception as e:
            self.error_occurred.emit(str(e))
