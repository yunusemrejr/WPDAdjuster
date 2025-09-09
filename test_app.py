#!/usr/bin/env python3
"""
Simple test script to verify WPDAdjuster components
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported"""
    try:
        from config.settings import AppSettings
        from utils.file_validator import validate_file, is_supported_extension
        from utils.logger import setup_logging
        from processors.document_processor import DocumentProcessor
        from processors.docx_processor import DocxProcessor
        from processors.rtf_processor import RtfProcessor
        from gui.styles import get_light_theme, get_dark_theme
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_settings():
    """Test settings configuration"""
    try:
        from config.settings import AppSettings
        settings = AppSettings()
        print(f"✓ Settings initialized - Theme: {settings.theme}, Debug: {settings.debug}")
        return True
    except Exception as e:
        print(f"✗ Settings error: {e}")
        return False

def test_file_validator():
    """Test file validation"""
    try:
        from utils.file_validator import validate_file, is_supported_extension
        
        # Test extension check
        test_docx = Path("test.docx")
        test_rtf = Path("test.rtf")
        test_txt = Path("test.txt")
        
        assert is_supported_extension(test_docx) == True
        assert is_supported_extension(test_rtf) == True
        assert is_supported_extension(test_txt) == False
        print("✓ File validator working correctly")
        return True
    except Exception as e:
        print(f"✗ File validator error: {e}")
        return False

def test_processors():
    """Test document processors"""
    try:
        from processors.document_processor import DocumentProcessor
        from processors.docx_processor import DocxProcessor
        from processors.rtf_processor import RtfProcessor
        
        processor = DocumentProcessor()
        docx_processor = DocxProcessor()
        rtf_processor = RtfProcessor()
        
        extensions = processor.get_supported_extensions()
        assert '.docx' in extensions
        assert '.rtf' in extensions
        print("✓ Document processors initialized correctly")
        return True
    except Exception as e:
        print(f"✗ Processor error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing WPDAdjuster components...")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_settings,
        test_file_validator,
        test_processors
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("✓ All tests passed! WPDAdjuster is ready to run.")
        print("\nTo start the application, run:")
        print("  python main.py")
        print("  or")
        print("  ./run.sh")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
