#!/usr/bin/env python3
"""
WPDAdjuster - Word Processing Document Adjuster
Main application entry point
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from src.gui.main_window import MainWindow
from src.utils.logger import setup_logging
from src.config.settings import AppSettings

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("WPDAdjuster")
    app.setApplicationVersion("1.0.0")
    
    # Load settings
    settings = AppSettings()
    
    # Create and show main window
    main_window = MainWindow(settings)
    main_window.show()
    
    logger.info("WPDAdjuster started successfully")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
