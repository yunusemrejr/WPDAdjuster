"""
Centralized PyQt6 stylesheet definitions
"""

def get_light_theme() -> str:
    """Get light theme stylesheet"""
    return """
    QMainWindow {
        background-color: #f5f5f5;
        color: #212121;
    }
    
    QWidget {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 12px;
    }
    
    QPushButton {
        background-color: #1976d2;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #1565c0;
    }
    
    QPushButton:pressed {
        background-color: #0d47a1;
    }
    
    QPushButton:disabled {
        background-color: #bdbdbd;
        color: #757575;
    }
    
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
        border: 1px solid #bdbdbd;
        border-radius: 4px;
        padding: 6px 8px;
        background-color: white;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #1976d2;
    }
    
    QLabel {
        color: #424242;
    }
    
    QGroupBox {
        font-weight: 600;
        border: 1px solid #bdbdbd;
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px 0 4px;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QProgressBar {
        border: 1px solid #bdbdbd;
        border-radius: 4px;
        text-align: center;
        background-color: #f5f5f5;
    }
    
    QProgressBar::chunk {
        background-color: #1976d2;
        border-radius: 3px;
    }
    """

def get_dark_theme() -> str:
    """Get dark theme stylesheet"""
    return """
    QMainWindow {
        background-color: #212121;
        color: #f5f5f5;
    }
    
    QWidget {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 12px;
    }
    
    QPushButton {
        background-color: #1976d2;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    QPushButton:hover {
        background-color: #1565c0;
    }
    
    QPushButton:pressed {
        background-color: #0d47a1;
    }
    
    QPushButton:disabled {
        background-color: #424242;
        color: #757575;
    }
    
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
        border: 1px solid #424242;
        border-radius: 4px;
        padding: 6px 8px;
        background-color: #303030;
        color: #f5f5f5;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #1976d2;
    }
    
    QLabel {
        color: #e0e0e0;
    }
    
    QGroupBox {
        font-weight: 600;
        border: 1px solid #424242;
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px 0 4px;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QProgressBar {
        border: 1px solid #424242;
        border-radius: 4px;
        text-align: center;
        background-color: #303030;
    }
    
    QProgressBar::chunk {
        background-color: #1976d2;
        border-radius: 3px;
    }
    """

def get_drag_drop_styles() -> str:
    """Get drag and drop specific styles"""
    return """
    QWidget#dragDropArea {
        border: 2px dashed #1976d2;
        border-radius: 8px;
        background-color: rgba(25, 118, 210, 0.1);
    }
    
    QWidget#dragDropArea:hover {
        background-color: rgba(25, 118, 210, 0.2);
        border-color: #1565c0;
    }
    
    QWidget#dragDropArea[dropActive="true"] {
        background-color: rgba(25, 118, 210, 0.3);
        border-color: #0d47a1;
    }
    
    QLabel#dragDropLabel {
        color: #1976d2;
        font-size: 14px;
        font-weight: 500;
    }
    
    QLabel#dragDropSubLabel {
        color: #757575;
        font-size: 11px;
    }
    """
