"""
Modification form widget for document settings
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QLineEdit, QFormLayout, QScrollArea,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFontDatabase
from typing import Dict, Any, List

class ModificationForm(QWidget):
    """Form widget for modifying document settings"""
    
    settings_applied = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.document_data = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the modification form UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Create scroll area for form content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Form content widget
        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout(self.form_widget)
        
        scroll_area.setWidget(self.form_widget)
        layout.addWidget(scroll_area)
        
        # Apply button (outside scroll area)
        self.apply_button = QPushButton("Apply Modifications")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)
        layout.addWidget(self.apply_button)
        
        # Initially show placeholder
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder when no document is loaded"""
        self.clear_content()
        
        placeholder = QLabel("Load a document to modify settings")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #757575; font-style: italic;")
        self.form_layout.addWidget(placeholder)
        
    def clear_content(self):
        """Clear all content from the form"""
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def update_document(self, document_data: Dict[str, Any]):
        """Update the form with document data"""
        self.document_data = document_data
        self.clear_content()
        
        # Add RTF warning if applicable
        if document_data.get('file_type') == 'rtf':
            self.add_rtf_warning()
        
        # Page settings group
        self.add_page_settings_group()
        
        # Margin settings group
        self.add_margin_settings_group()
        
        # Font settings group
        self.add_font_settings_group()
        
        # Line spacing group
        self.add_line_spacing_group()
        
        # Enable apply button
        self.apply_button.setEnabled(True)
        
    def add_rtf_warning(self):
        """Add warning for RTF files about limitations"""
        warning_group = QGroupBox("⚠️ RTF File Notice")
        layout = QVBoxLayout(warning_group)
        
        warning_text = QLabel(
            "<b>RTF Format Limitations:</b><br/>"
            "• Page size changes are not supported for RTF files<br/>"
            "• Only margin modifications will be applied (if not already present)<br/>"
            "• Original document formatting and text content are fully preserved<br/>"
            "• RTF formatting codes (like \\f0, \\fs28) are normal and not text content"
        )
        warning_text.setObjectName("measurementUnit")
        warning_text.setWordWrap(True)
        layout.addWidget(warning_text)
        
        self.form_layout.addWidget(warning_group)
        
    def add_page_settings_group(self):
        """Add page size settings group"""
        group = QGroupBox("📏 Page Size")
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # Check if RTF file
        is_rtf = self.document_data and self.document_data.get('file_type') == 'rtf'
        
        # Page size dropdown
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["A4", "Letter", "Legal", "Custom"])
        self.page_size_combo.currentTextChanged.connect(self.on_page_size_changed)
        self.page_size_combo.setEnabled(not is_rtf)
        layout.addRow("Size:", self.page_size_combo)
        
        # Custom dimensions (initially hidden)
        self.custom_width = QDoubleSpinBox()
        self.custom_width.setRange(1.0, 20.0)
        self.custom_width.setValue(8.5)
        self.custom_width.setSuffix(" inches")
        self.custom_width.setDecimals(2)
        self.custom_width.setEnabled(not is_rtf)
        self.custom_width.hide()
        layout.addRow("Width:", self.custom_width)
        
        self.custom_height = QDoubleSpinBox()
        self.custom_height.setRange(1.0, 30.0)
        self.custom_height.setValue(11.0)
        self.custom_height.setSuffix(" inches")
        self.custom_height.setDecimals(2)
        self.custom_height.setEnabled(not is_rtf)
        self.custom_height.hide()
        layout.addRow("Height:", self.custom_height)
        
        # Add unit info label
        if is_rtf:
            unit_info = QLabel("Page size changes not supported for RTF files")
            unit_info.setObjectName("measurementUnit")
        else:
            unit_info = QLabel("All measurements are in inches")
            unit_info.setObjectName("measurementUnit")
        layout.addRow("", unit_info)
        
        # Set current page size
        self.set_current_page_size()
        
        self.form_layout.addWidget(group)
        
    def add_margin_settings_group(self):
        """Add margin settings group"""
        group = QGroupBox("📐 Margins")
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # Margin inputs (now supported for both DOCX and RTF)
        self.margin_top = QDoubleSpinBox()
        self.margin_top.setRange(0.1, 5.0)
        self.margin_top.setValue(1.0)
        self.margin_top.setSuffix(" inches")
        self.margin_top.setDecimals(2)
        layout.addRow("Top:", self.margin_top)
        
        self.margin_bottom = QDoubleSpinBox()
        self.margin_bottom.setRange(0.1, 5.0)
        self.margin_bottom.setValue(1.0)
        self.margin_bottom.setSuffix(" inches")
        self.margin_bottom.setDecimals(2)
        layout.addRow("Bottom:", self.margin_bottom)
        
        self.margin_left = QDoubleSpinBox()
        self.margin_left.setRange(0.1, 5.0)
        self.margin_left.setValue(1.0)
        self.margin_left.setSuffix(" inches")
        self.margin_left.setDecimals(2)
        layout.addRow("Left:", self.margin_left)
        
        self.margin_right = QDoubleSpinBox()
        self.margin_right.setRange(0.1, 5.0)
        self.margin_right.setValue(1.0)
        self.margin_right.setSuffix(" inches")
        self.margin_right.setDecimals(2)
        layout.addRow("Right:", self.margin_right)
        
        # Add unit info label
        unit_info = QLabel("All margin measurements are in inches")
        unit_info.setObjectName("measurementUnit")
        layout.addRow("", unit_info)
        
        # Set current margins
        self.set_current_margins()
        
        self.form_layout.addWidget(group)
        
    def add_font_settings_group(self):
        """Add font settings group"""
        group = QGroupBox("🔤 Font Settings")
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # Font family dropdown
        self.font_family_combo = QComboBox()
        self.populate_font_families()
        layout.addRow("Font Family:", self.font_family_combo)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(6, 72)
        self.font_size.setValue(12)
        self.font_size.setSuffix(" points")
        layout.addRow("Font Size:", self.font_size)
        
        # Add unit info label
        unit_info = QLabel("Font size is measured in points (pt)")
        unit_info.setObjectName("measurementUnit")
        layout.addRow("", unit_info)
        
        # Set current font
        self.set_current_font()
        
        self.form_layout.addWidget(group)
        
    def add_line_spacing_group(self):
        """Add line spacing group"""
        group = QGroupBox("📏 Line Spacing")
        layout = QFormLayout(group)
        layout.setSpacing(8)
        
        # Line spacing dropdown
        self.line_spacing_combo = QComboBox()
        self.line_spacing_combo.addItems([
            "Single (1.0)",
            "1.15",
            "1.5",
            "Double (2.0)",
            "Custom"
        ])
        self.line_spacing_combo.currentTextChanged.connect(self.on_line_spacing_changed)
        layout.addRow("Spacing:", self.line_spacing_combo)
        
        # Custom line spacing (initially hidden)
        self.custom_line_spacing = QDoubleSpinBox()
        self.custom_line_spacing.setRange(0.5, 5.0)
        self.custom_line_spacing.setValue(1.0)
        self.custom_line_spacing.setDecimals(2)
        self.custom_line_spacing.hide()
        layout.addRow("Custom Value:", self.custom_line_spacing)
        
        # Add unit info label
        unit_info = QLabel("Line spacing is a multiplier (1.0 = single, 1.5 = 1.5x, etc.)")
        unit_info.setObjectName("measurementUnit")
        layout.addRow("", unit_info)
        
        self.form_layout.addWidget(group)
        
    def populate_font_families(self):
        """Populate font family dropdown with system fonts"""
        try:
            font_db = QFontDatabase()
            families = font_db.families(QFontDatabase.WritingSystem.Any)
        except:
            # Fallback to common fonts if QFontDatabase fails
            families = []
            
        # Add common fonts first
        common_fonts = ["Times New Roman", "Arial", "Calibri", "Helvetica", "Georgia", "Verdana", "Courier New"]
        for font in common_fonts:
            self.font_family_combo.addItem(font)
            if font in families:
                families.remove(font)
                
        # Add separator
        self.font_family_combo.insertSeparator(self.font_family_combo.count())
        
        # Add remaining fonts
        for font in sorted(families):
            self.font_family_combo.addItem(font)
            
    def set_current_page_size(self):
        """Set current page size based on document data"""
        if not self.document_data:
            return
            
        dimensions = self.document_data.get('page_dimensions', {})
        width = dimensions.get('width', 8.5)
        height = dimensions.get('height', 11.0)
        
        # Determine page size
        if abs(width - 8.5) < 0.1 and abs(height - 11.0) < 0.1:
            self.page_size_combo.setCurrentText("Letter")
        elif abs(width - 8.27) < 0.1 and abs(height - 11.69) < 0.1:
            self.page_size_combo.setCurrentText("A4")
        elif abs(width - 8.5) < 0.1 and abs(height - 14.0) < 0.1:
            self.page_size_combo.setCurrentText("Legal")
        else:
            self.page_size_combo.setCurrentText("Custom")
            self.custom_width.setValue(width)
            self.custom_height.setValue(height)
            self.custom_width.show()
            self.custom_height.show()
            
    def set_current_margins(self):
        """Set current margins based on document data"""
        if not self.document_data:
            return
            
        margins = self.document_data.get('margins', {})
        self.margin_top.setValue(margins.get('top', 1.0))
        self.margin_bottom.setValue(margins.get('bottom', 1.0))
        self.margin_left.setValue(margins.get('left', 1.0))
        self.margin_right.setValue(margins.get('right', 1.0))
        
    def set_current_font(self):
        """Set current font based on document data"""
        if not self.document_data:
            return
            
        fonts = self.document_data.get('fonts_used', {})
        if fonts:
            # Get most used font
            most_used_font = max(fonts.items(), key=lambda x: x[1])[0]
            index = self.font_family_combo.findText(most_used_font)
            if index >= 0:
                self.font_family_combo.setCurrentIndex(index)
                
    def on_page_size_changed(self, text: str):
        """Handle page size selection change"""
        if text == "Custom":
            if hasattr(self, 'custom_width'):
                self.custom_width.show()
            if hasattr(self, 'custom_height'):
                self.custom_height.show()
        else:
            if hasattr(self, 'custom_width'):
                self.custom_width.hide()
            if hasattr(self, 'custom_height'):
                self.custom_height.hide()
            
            # Set standard dimensions
            if text == "A4" and hasattr(self, 'custom_width') and hasattr(self, 'custom_height'):
                self.custom_width.setValue(8.27)
                self.custom_height.setValue(11.69)
            elif text == "Letter" and hasattr(self, 'custom_width') and hasattr(self, 'custom_height'):
                self.custom_width.setValue(8.5)
                self.custom_height.setValue(11.0)
            elif text == "Legal" and hasattr(self, 'custom_width') and hasattr(self, 'custom_height'):
                self.custom_width.setValue(8.5)
                self.custom_height.setValue(14.0)
                
    def on_line_spacing_changed(self, text: str):
        """Handle line spacing selection change"""
        if text == "Custom":
            self.custom_line_spacing.show()
        else:
            self.custom_line_spacing.hide()
            
            # Set standard values
            if "Single" in text:
                self.custom_line_spacing.setValue(1.0)
            elif "1.15" in text:
                self.custom_line_spacing.setValue(1.15)
            elif "1.5" in text:
                self.custom_line_spacing.setValue(1.5)
            elif "Double" in text:
                self.custom_line_spacing.setValue(2.0)
                
    def apply_settings(self):
        """Apply the current settings"""
        if not self.document_data:
            return
            
        try:
            settings = self.collect_settings()
            self.settings_applied.emit(settings)
        except Exception as e:
            self.logger.error(f"Error collecting settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to collect settings: {e}")
            
    def collect_settings(self) -> Dict[str, Any]:
        """Collect all settings from the form"""
        settings = {}
        
        # Page size settings
        page_size_text = self.page_size_combo.currentText()
        if page_size_text == "Custom":
            settings['page_size'] = {
                'width': self.custom_width.value(),
                'height': self.custom_height.value()
            }
        else:
            # Use standard dimensions
            if page_size_text == "A4":
                settings['page_size'] = {'width': 8.27, 'height': 11.69}
            elif page_size_text == "Letter":
                settings['page_size'] = {'width': 8.5, 'height': 11.0}
            elif page_size_text == "Legal":
                settings['page_size'] = {'width': 8.5, 'height': 14.0}
                
        # Margin settings
        settings['margins'] = {
            'top': self.margin_top.value(),
            'bottom': self.margin_bottom.value(),
            'left': self.margin_left.value(),
            'right': self.margin_right.value()
        }
        
        # Font settings
        settings['font_settings'] = {
            'family': self.font_family_combo.currentText(),
            'size': self.font_size.value()
        }
        
        # Line spacing settings
        line_spacing_text = self.line_spacing_combo.currentText()
        if line_spacing_text == "Custom":
            settings['line_spacing'] = self.custom_line_spacing.value()
        else:
            # Extract numeric value
            if "Single" in line_spacing_text:
                settings['line_spacing'] = 1.0
            elif "1.15" in line_spacing_text:
                settings['line_spacing'] = 1.15
            elif "1.5" in line_spacing_text:
                settings['line_spacing'] = 1.5
            elif "Double" in line_spacing_text:
                settings['line_spacing'] = 2.0
                
        return settings
