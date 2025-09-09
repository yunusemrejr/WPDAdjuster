"""
RTF document processor using striprtf
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
from striprtf.striprtf import rtf_to_text
import tempfile
import re

class RtfProcessor:
    """Processor for RTF documents"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def process_document(self, file_path: Path) -> Dict[str, Any]:
        """
        Process RTF document and extract properties
        
        Args:
            file_path: Path to RTF file
            
        Returns:
            Dictionary containing document properties
        """
        try:
            # Read RTF file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                rtf_content = f.read()
                
            # Convert RTF to plain text for analysis
            plain_text = rtf_to_text(rtf_content)
            
            # Extract basic metadata
            title = self._extract_rtf_property(rtf_content, 'title') or 'Untitled'
            author = self._extract_rtf_property(rtf_content, 'author') or 'Unknown'
            
            # Extract page settings (RTF doesn't have standard page size info)
            page_dimensions = {'width': 8.5, 'height': 11.0}  # Default to Letter
            
            # Extract margins (basic parsing)
            margins = self._extract_margins(rtf_content)
            
            # Extract font information
            fonts_used = self._extract_rtf_fonts(rtf_content)
            
            # Count paragraphs and words from plain text
            paragraphs = [p.strip() for p in plain_text.split('\n') if p.strip()]
            paragraph_count = len(paragraphs)
            word_count = len(plain_text.split())
            
            # Count tables (basic detection)
            table_count = self._count_tables(rtf_content)
            
            return {
                'file_path': str(file_path),
                'filename': file_path.name,
                'file_type': 'rtf',
                'title': title,
                'author': author,
                'page_count': 1,  # RTF doesn't have clear page breaks
                'word_count': word_count,
                'paragraph_count': paragraph_count,
                'page_dimensions': page_dimensions,
                'margins': margins,
                'fonts_used': fonts_used,
                'heading_counts': {'Heading 1': 0, 'Heading 2': 0, 'Heading 3': 0, 
                                 'Heading 4': 0, 'Heading 5': 0, 'Heading 6': 0},
                'table_count': table_count,
                'rtf_content': rtf_content  # Keep content for modifications
            }
            
        except Exception as e:
            self.logger.error(f"Error processing RTF document: {e}")
            raise ValueError(f"Failed to process RTF document: {e}")
            
    def apply_modifications(self, document_data: Dict[str, Any], settings: Dict[str, Any]) -> Path:
        """
        Apply modification settings to RTF document while preserving original formatting
        
        Args:
            document_data: Original document data
            settings: Modification settings
            
        Returns:
            Path to modified document
        """
        try:
            rtf_content = document_data['rtf_content']
            
            # For RTF, we'll be very conservative and only add minimal formatting
            # RTF files are complex and we want to preserve all existing formatting
            
            # Start with original content - don't modify anything
            modified_content = rtf_content
            
            # Only add document-level formatting if absolutely necessary
            # and only if the original document doesn't already have it
            
            # Check if we need to add any formatting
            needs_modification = False
            
            # Check margins
            if 'margins' in settings:
                margins = settings['margins']
                # Convert inches to twips (1 inch = 1440 twips)
                if 'left' in margins and '\\margl' not in rtf_content:
                    left_twips = int(margins['left'] * 1440)
                    # Add left margin command
                    modified_content = modified_content.replace('\\rtf1', f'\\rtf1\\margl{left_twips}')
                    needs_modification = True
                    
                if 'right' in margins and '\\margr' not in rtf_content:
                    right_twips = int(margins['right'] * 1440)
                    modified_content = modified_content.replace('\\rtf1', f'\\rtf1\\margr{right_twips}')
                    needs_modification = True
                    
                if 'top' in margins and '\\margt' not in rtf_content:
                    top_twips = int(margins['top'] * 1440)
                    modified_content = modified_content.replace('\\rtf1', f'\\rtf1\\margt{top_twips}')
                    needs_modification = True
                    
                if 'bottom' in margins and '\\margb' not in rtf_content:
                    bottom_twips = int(margins['bottom'] * 1440)
                    modified_content = modified_content.replace('\\rtf1', f'\\rtf1\\margb{bottom_twips}')
                    needs_modification = True
            
            # Save modified document (even if no changes were made)
            output_path = self._get_output_path(document_data['file_path'])
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            
            self.logger.info(f"Modified RTF saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error applying modifications to RTF: {e}")
            raise ValueError(f"Failed to apply modifications: {e}")
            
    def _parse_rtf_content(self, content: str, doc):
        """Basic RTF content parsing - simplified for striprtf"""
        # striprtf handles the conversion, so this is just a placeholder
        pass
        
    def _extract_rtf_property(self, content: str, property_name: str) -> str:
        """Extract RTF document properties"""
        pattern = r'\\' + property_name + r'\s*([^\\}]+)'
        match = re.search(pattern, content, re.IGNORECASE)
        return match.group(1).strip() if match else None
        
    def _extract_margins(self, content: str) -> Dict[str, float]:
        """Extract margin information from RTF"""
        # RTF margin parsing is complex, return defaults
        return {
            'top': 1.0,
            'bottom': 1.0,
            'left': 1.0,
            'right': 1.0
        }
        
    def _extract_rtf_fonts(self, content: str) -> Dict[str, int]:
        """Extract font usage from RTF content"""
        fonts = {}
        
        # Look for font table
        font_table_match = re.search(r'\\fonttbl\s*\{([^}]+)\}', content)
        if font_table_match:
            font_table = font_table_match.group(1)
            font_matches = re.findall(r'\\f(\d+)\s*([^;]+);', font_table)
            for font_id, font_name in font_matches:
                fonts[font_name.strip()] = 0
                
        # Count font usage
        for font_name in fonts.keys():
            pattern = r'\\f\d+\s*[^\\]*' + re.escape(font_name)
            fonts[font_name] = len(re.findall(pattern, content, re.IGNORECASE))
            
        return fonts
        
    def _count_words(self, content: str) -> int:
        """Count words in RTF content"""
        # Remove RTF control codes
        clean_content = re.sub(r'\\[a-z]+\d*\s*', ' ', content)
        clean_content = re.sub(r'[{}]', ' ', clean_content)
        words = clean_content.split()
        return len([w for w in words if w.strip()])
        
    def _count_tables(self, content: str) -> int:
        """Count tables in RTF content"""
        return len(re.findall(r'\\trowd', content))
        
    # Removed problematic methods that were adding zeros to document text
    # New approach only adds formatting commands at document level
        
    def _get_output_path(self, original_path: str) -> Path:
        """Generate output path for modified document"""
        original = Path(original_path)
        output_name = f"{original.stem}_modified{original.suffix}"
        return original.parent / output_name
