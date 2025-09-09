"""
Document overview widget showing document properties
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QScrollArea, QFrame
)
from PyQt6.QtCore import Qt
from typing import Dict, Any

class DocumentOverview(QWidget):
    """Widget displaying document overview and properties"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the document overview UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        
        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
        
        # Initially show placeholder
        self.show_placeholder()
        
    def show_placeholder(self):
        """Show placeholder when no document is loaded"""
        # Clear existing content
        self.clear_content()
        
        placeholder = QLabel("No document loaded")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setStyleSheet("color: #757575; font-style: italic;")
        self.content_layout.addWidget(placeholder)
        
    def clear_content(self):
        """Clear all content from the layout"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def update_document(self, document_data: Dict[str, Any]):
        """Update the overview with document data"""
        self.clear_content()
        
        # Document info section
        self.add_document_info(document_data)
        
        # Page settings section
        self.add_page_settings(document_data)
        
        # Font information section
        self.add_font_info(document_data)
        
        # Content statistics section
        self.add_content_stats(document_data)
        
    def add_document_info(self, data: Dict[str, Any]):
        """Add document information section"""
        group = QGroupBox("📄 Document Information")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Title
        title_label = QLabel(f"<b>Title:</b> {data.get('title', 'Untitled')}")
        title_label.setObjectName("documentValue")
        layout.addWidget(title_label)
        
        # Author
        author_label = QLabel(f"<b>Author:</b> {data.get('author', 'Unknown')}")
        author_label.setObjectName("documentValue")
        layout.addWidget(author_label)
        
        # File type
        file_type_label = QLabel(f"<b>Type:</b> {data.get('file_type', 'Unknown').upper()}")
        file_type_label.setObjectName("documentValue")
        layout.addWidget(file_type_label)
        
        # Filename
        filename_label = QLabel(f"<b>File:</b> {data.get('filename', 'Unknown')}")
        filename_label.setObjectName("documentValue")
        layout.addWidget(filename_label)
        
        self.content_layout.addWidget(group)
        
    def add_page_settings(self, data: Dict[str, Any]):
        """Add page settings section"""
        group = QGroupBox("📏 Page Settings")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)
        
        # Page dimensions
        dimensions = data.get('page_dimensions', {})
        width = dimensions.get('width', 0)
        height = dimensions.get('height', 0)
        dim_label = QLabel(f"<b>Size:</b> {width:.1f}″ × {height:.1f}″ <span style='color: #757575; font-style: italic;'>(inches)</span>")
        dim_label.setObjectName("documentValue")
        layout.addWidget(dim_label)
        
        # Margins
        margins = data.get('margins', {})
        margin_text = f"<b>Margins:</b><br/>" \
                     f"• Top: {margins.get('top', 0):.1f}″<br/>" \
                     f"• Bottom: {margins.get('bottom', 0):.1f}″<br/>" \
                     f"• Left: {margins.get('left', 0):.1f}″<br/>" \
                     f"• Right: {margins.get('right', 0):.1f}″<br/>" \
                     f"<span style='color: #757575; font-style: italic; font-size: 11px;'>(all measurements in inches)</span>"
        margin_label = QLabel(margin_text)
        margin_label.setObjectName("documentValue")
        layout.addWidget(margin_label)
        
        self.content_layout.addWidget(group)
        
    def add_font_info(self, data: Dict[str, Any]):
        """Add font information section"""
        group = QGroupBox("🔤 Fonts Used")
        layout = QVBoxLayout(group)
        layout.setSpacing(6)
        
        fonts = data.get('fonts_used', {})
        if fonts:
            for font_name, count in sorted(fonts.items(), key=lambda x: x[1], reverse=True):
                font_label = QLabel(f"<b>{font_name}:</b> {count} occurrences")
                font_label.setObjectName("documentValue")
                layout.addWidget(font_label)
        else:
            no_fonts_label = QLabel("No font information available")
            no_fonts_label.setObjectName("measurementUnit")
            layout.addWidget(no_fonts_label)
            
        self.content_layout.addWidget(group)
        
    def add_content_stats(self, data: Dict[str, Any]):
        """Add content statistics section"""
        group = QGroupBox("📊 Content Statistics")
        layout = QVBoxLayout(group)
        layout.setSpacing(6)
        
        # Word count
        word_count = data.get('word_count', 0)
        word_label = QLabel(f"<b>Words:</b> {word_count:,}")
        word_label.setObjectName("documentValue")
        layout.addWidget(word_label)
        
        # Paragraph count
        para_count = data.get('paragraph_count', 0)
        para_label = QLabel(f"<b>Paragraphs:</b> {para_count:,}")
        para_label.setObjectName("documentValue")
        layout.addWidget(para_label)
        
        # Page count
        page_count = data.get('page_count', 0)
        page_label = QLabel(f"<b>Pages:</b> {page_count:,}")
        page_label.setObjectName("documentValue")
        layout.addWidget(page_label)
        
        # Table count
        table_count = data.get('table_count', 0)
        table_label = QLabel(f"<b>Tables:</b> {table_count:,}")
        table_label.setObjectName("documentValue")
        layout.addWidget(table_label)
        
        # Heading counts
        headings = data.get('heading_counts', {})
        if any(headings.values()):
            heading_label = QLabel("<b>Headings:</b>")
            heading_label.setObjectName("documentInfo")
            layout.addWidget(heading_label)
            
            for level, count in headings.items():
                if count > 0:
                    level_label = QLabel(f"  • {level}: {count}")
                    level_label.setObjectName("documentValue")
                    level_label.setIndent(20)
                    layout.addWidget(level_label)
        
        self.content_layout.addWidget(group)
