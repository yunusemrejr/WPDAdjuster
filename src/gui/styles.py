"""
Centralized PyQt6 stylesheet definitions
"""

def get_light_theme() -> str:
    """Get light theme stylesheet"""
    return """
    QMainWindow {
        background-color: #ffffff;
        color: #212121;
    }
    
    QWidget {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 12px;
        color: #212121;
    }
    
    QPushButton {
        background-color: #1976d2;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
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
        border: 2px solid #e0e0e0;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #ffffff;
        color: #212121;
        font-size: 12px;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #1976d2;
        background-color: #f8f9ff;
    }
    
    QLabel {
        color: #424242;
        font-weight: 500;
    }
    
    QGroupBox {
        font-weight: 700;
        font-size: 13px;
        color: #1976d2;
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 12px;
        background-color: #fafafa;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px 0 8px;
        background-color: #fafafa;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QProgressBar {
        border: 2px solid #e0e0e0;
        border-radius: 6px;
        text-align: center;
        background-color: #f5f5f5;
        color: #212121;
    }
    
    QProgressBar::chunk {
        background-color: #1976d2;
        border-radius: 4px;
    }
    
    /* Document overview specific styles */
    QLabel#documentInfo {
        color: #1976d2;
        font-weight: 600;
        font-size: 13px;
    }
    
    QLabel#documentValue {
        color: #424242;
        font-weight: 500;
    }
    
    QLabel#measurementUnit {
        color: #757575;
        font-style: italic;
        font-size: 11px;
    }
    """

def get_dark_theme() -> str:
    """Get dark theme stylesheet"""
    return """
    QMainWindow {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    QWidget {
        font-family: system-ui, -apple-system, sans-serif;
        font-size: 12px;
        color: #ffffff;
    }
    
    QPushButton {
        background-color: #1976d2;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
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
        border: 2px solid #424242;
        border-radius: 6px;
        padding: 8px 12px;
        background-color: #2d2d2d;
        color: #ffffff;
        font-size: 12px;
    }
    
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border-color: #1976d2;
        background-color: #1a1f2e;
    }
    
    QLabel {
        color: #e0e0e0;
        font-weight: 500;
    }
    
    QGroupBox {
        font-weight: 700;
        font-size: 13px;
        color: #64b5f6;
        border: 2px solid #424242;
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 12px;
        background-color: #2d2d2d;
    }
    
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px 0 8px;
        background-color: #2d2d2d;
    }
    
    QScrollArea {
        border: none;
        background-color: transparent;
    }
    
    QProgressBar {
        border: 2px solid #424242;
        border-radius: 6px;
        text-align: center;
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    QProgressBar::chunk {
        background-color: #1976d2;
        border-radius: 4px;
    }
    
    /* Document overview specific styles */
    QLabel#documentInfo {
        color: #64b5f6;
        font-weight: 600;
        font-size: 13px;
    }
    
    QLabel#documentValue {
        color: #e0e0e0;
        font-weight: 500;
    }
    
    QLabel#measurementUnit {
        color: #bdbdbd;
        font-style: italic;
        font-size: 11px;
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
