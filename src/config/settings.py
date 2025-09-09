"""
Application settings and configuration
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

@dataclass
class AppSettings:
    """Application settings container"""
    debug: bool = False
    theme: str = "light"
    language: str = "en"
    temp_dir: Path = Path("/tmp/wpdadjuster")
    
    def __post_init__(self):
        """Initialize settings from environment variables"""
        self.debug = os.getenv("APP_DEBUG", "false").lower() == "true"
        self.theme = os.getenv("APP_THEME", "light")
        self.language = os.getenv("APP_LANG", "en")
        
        # Ensure temp directory exists
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    @property
    def is_dark_theme(self) -> bool:
        """Check if dark theme is enabled"""
        return self.theme == "dark"
