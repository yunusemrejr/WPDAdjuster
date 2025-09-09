"""
Logging configuration
"""

import logging
import sys
from pathlib import Path

def setup_logging():
    """Setup application logging configuration"""
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "wpdadjuster.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("PyQt6").setLevel(logging.WARNING)
    logging.getLogger("docx").setLevel(logging.WARNING)
