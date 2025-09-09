"""
File validation utilities
"""

import mimetypes
from pathlib import Path
from typing import Tuple, Optional

SUPPORTED_EXTENSIONS = {'.docx', '.rtf'}
SUPPORTED_MIME_TYPES = {
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/rtf',
    'text/rtf'
}

def validate_file(file_path: Path) -> Tuple[bool, Optional[str]]:
    """
    Validate if file is supported format
    
    Args:
        file_path: Path to file to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_path.exists():
        return False, "File does not exist"
    
    if not file_path.is_file():
        return False, "Path is not a file"
    
    # Check extension
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file extension. Only {', '.join(SUPPORTED_EXTENSIONS)} are supported"
    
    # Check MIME type
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if mime_type and mime_type not in SUPPORTED_MIME_TYPES:
        return False, f"Unsupported file type: {mime_type}"
    
    return True, None

def is_supported_extension(file_path: Path) -> bool:
    """Check if file has supported extension"""
    return file_path.suffix.lower() in SUPPORTED_EXTENSIONS
