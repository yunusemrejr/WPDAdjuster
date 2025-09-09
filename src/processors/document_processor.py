"""
Main document processor that handles both DOCX and RTF files
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional

from .docx_processor import DocxProcessor
from .rtf_processor import RtfProcessor
from ..utils.file_validator import validate_file

class DocumentProcessor:
    """Main document processor that delegates to specific processors"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.docx_processor = DocxProcessor()
        self.rtf_processor = RtfProcessor()
        
    def process_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Process a document and extract its properties
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing document properties and metadata
        """
        # Validate file first
        is_valid, error_msg = validate_file(file_path)
        if not is_valid:
            raise ValueError(f"Invalid file: {error_msg}")
            
        self.logger.info(f"Processing document: {file_path}")
        
        # Determine processor based on file extension
        if file_path.suffix.lower() == '.docx':
            return self.docx_processor.process_document(file_path)
        elif file_path.suffix.lower() == '.rtf':
            return self.rtf_processor.process_document(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
            
    def apply_modifications(self, document_data: Dict[str, Any], settings: Dict[str, Any]) -> Path:
        """
        Apply modification settings to a document
        
        Args:
            document_data: Original document data
            settings: Modification settings to apply
            
        Returns:
            Path to the modified document
        """
        file_path = Path(document_data['file_path'])
        
        self.logger.info(f"Applying modifications to: {file_path}")
        
        # Determine processor based on file extension
        if file_path.suffix.lower() == '.docx':
            return self.docx_processor.apply_modifications(document_data, settings)
        elif file_path.suffix.lower() == '.rtf':
            return self.rtf_processor.apply_modifications(document_data, settings)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
            
    def get_supported_extensions(self) -> list:
        """Get list of supported file extensions"""
        return ['.docx', '.rtf']
