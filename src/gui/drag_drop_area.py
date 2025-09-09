"""
Drag and drop area widget
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from pathlib import Path
import logging

from ..utils.file_validator import validate_file, is_supported_extension

class DragDropArea(QWidget):
    """Custom drag and drop area for file uploads"""
    
    file_dropped = pyqtSignal(Path)
    file_rejected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.setup_ui()
        self.setAcceptDrops(True)
        self.setObjectName("dragDropArea")
        
    def setup_ui(self):
        """Setup the drag drop area UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Main label
        self.main_label = QLabel("Drop DOCX or RTF files here")
        self.main_label.setObjectName("dragDropLabel")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Sub label
        self.sub_label = QLabel("Only .docx and .rtf files are supported")
        self.sub_label.setObjectName("dragDropSubLabel")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.main_label)
        layout.addWidget(self.sub_label)
        
        # Set minimum size
        self.setMinimumSize(400, 200)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and len(urls) == 1:
                file_path = Path(urls[0].toLocalFile())
                if is_supported_extension(file_path):
                    event.acceptProposedAction()
                    self.setProperty("dropActive", True)
                    self.style().unpolish(self)
                    self.style().polish(self)
                    return
        
        event.ignore()
        
    def dragLeaveEvent(self, event):
        """Handle drag leave event"""
        self.setProperty("dropActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().dragLeaveEvent(event)
        
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        self.setProperty("dropActive", False)
        self.style().unpolish(self)
        self.style().polish(self)
        
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and len(urls) == 1:
                file_path = Path(urls[0].toLocalFile())
                
                # Validate file
                is_valid, error_msg = validate_file(file_path)
                if is_valid:
                    self.logger.info(f"File dropped and validated: {file_path}")
                    self.file_dropped.emit(file_path)
                else:
                    self.logger.warning(f"File dropped but validation failed: {error_msg}")
                    self.file_rejected.emit(error_msg)
                    
        event.acceptProposedAction()
