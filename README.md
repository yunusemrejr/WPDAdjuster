# WPDAdjuster - Word Processing Document Adjuster

A professional offline-capable Python application for modifying DOCX and RTF documents with a modern PyQt6 interface.

## Features

- **Document Support**: Process both DOCX and RTF files
- **Drag & Drop Interface**: Easy file upload with visual feedback
- **Document Overview**: View comprehensive document properties and statistics
- **Modification Tools**: Adjust page size, margins, fonts, and line spacing
- **Professional UI**: Clean, modern interface with light/dark theme support
- **Offline Capable**: No internet connection required

## Installation

### Prerequisites

- Python 3.11 or higher
- Linux (tested on Ubuntu/Debian)

### Setup

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Load Document**: Drag and drop a DOCX or RTF file onto the application window, or use File → Open
2. **Review Properties**: View document information, page settings, fonts, and content statistics
3. **Modify Settings**: Use the modification form to adjust:
   - Page size (A4, Letter, Legal, or custom)
   - Margins (top, bottom, left, right)
   - Font family and size
   - Line spacing (single, 1.15, 1.5, double, or custom)
4. **Apply Changes**: Click "Apply Modifications" to save the modified document

## Supported File Types

- **DOCX**: Microsoft Word documents (using python-docx)
- **RTF**: Rich Text Format documents (using pyrtf-ng)

## Configuration

The application supports environment variables for configuration:

- `APP_DEBUG=true`: Enable verbose logging
- `APP_THEME=dark`: Use dark theme (default: light)
- `APP_LANG=en`: Set language (default: en)

## Architecture

The application follows a modular architecture:

- `main.py`: Application entry point
- `src/gui/`: PyQt6 user interface components
- `src/processors/`: Document processing modules
- `src/utils/`: Utility functions and helpers
- `src/config/`: Configuration and settings

 

## License

This project is developed for open-source use. Please refer to the individual library licenses for dependencies.

## Dependencies

- PyQt6: GUI framework
- python-docx: DOCX document processing
- pyrtf-ng: RTF document processing
- PyInstaller: Application packaging
