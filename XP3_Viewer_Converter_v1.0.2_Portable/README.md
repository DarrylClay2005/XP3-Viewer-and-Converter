# XP3 Viewer and Converter

A powerful Windows GUI application for extracting, viewing, and converting XP3 archive files to various image formats including JPEG, PNG, BMP, and TIFF.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [XP3 Format Information](#xp3-format-information)
- [System Requirements](#system-requirements)
- [Building from Source](#building-from-source)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

XP3 Viewer and Converter is designed to work with XP3 archive files, which are commonly used by the KiriKiri visual novel engine. These archives contain various game assets including images, scripts, and audio files. This application focuses primarily on extracting and converting image files from these archives.

### What is XP3?

XP3 is a proprietary archive format developed by the KiriKiri team for packaging game resources. It supports compression and is widely used in Japanese visual novels and games. The format can contain various file types, but this application specializes in handling image files within these archives.

## ✨ Features

### Core Functionality
- **Load XP3 Archives**: Open and browse XP3 archive files
- **File Extraction**: Extract individual files or entire archives
- **Image Preview**: Real-time preview of image files within archives
- **Format Conversion**: Convert images to PNG, JPEG, BMP, or TIFF formats
- **Batch Operations**: Extract all files from an archive at once

### User Interface
- **Intuitive GUI**: Clean, modern interface built with tkinter
- **Split View**: Archive contents on the left, preview on the right
- **Progress Tracking**: Real-time status updates during operations
- **Error Handling**: Comprehensive error messages and validation

### Technical Features
- **Multi-threading**: Non-blocking operations for better user experience
- **Memory Efficient**: Handles large archives without excessive memory usage
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Format Support**: Handles various image formats commonly found in XP3 files

## 📸 Screenshots

*Note: Screenshots would be added here showing the application interface*

## 🚀 Installation

### Method 1: Quick Start (Recommended for Windows)

1. **Download the Repository**
   ```bash
   git clone https://github.com/your-username/XP3-Viewer-and-Converter.git
   cd XP3-Viewer-and-Converter
   ```

2. **Run the Application** (Windows)
   - Double-click `run_xp3_viewer.bat`
   - This will automatically install dependencies and launch the application

### Method 2: Manual Installation

1. **Prerequisites**
   - Python 3.7 or later
   - pip (Python package installer)

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python xp3_viewer_converter.py
   ```

### Method 3: Install as Package

```bash
pip install -e .
xp3-viewer-gui
```

## 📖 Usage Guide

### Getting Started

1. **Launch the Application**
   - Run `run_xp3_viewer.bat` (Windows) or `python xp3_viewer_converter.py`

2. **Open an XP3 Archive**
   - Click `File → Open XP3 Archive...`
   - Browse and select your XP3 file
   - Wait for the archive to load (progress shown in status bar)

### Interface Overview

#### Left Panel - Archive Contents
- **File List**: Shows all files in the loaded archive
- **Extract Selected**: Extract the currently selected file
- **Extract All**: Extract all files from the archive to a chosen directory

#### Right Panel - Preview and Conversion
- **Preview Area**: Displays image files when selected
- **Format Selection**: Choose output format (PNG, JPEG, BMP, TIFF)
- **Convert Selected**: Convert the selected image to chosen format

#### Status Bar
- Shows current operation status and file count

### Step-by-Step Operations

#### Viewing Files

1. Load an XP3 archive using `File → Open XP3 Archive...`
2. Click on any file in the left panel
3. If it's an image file, a preview will appear in the right panel
4. Non-image files will show "Cannot preview" message

#### Extracting Files

**Single File Extraction:**
1. Select a file from the list
2. Click "Extract Selected"
3. Choose destination directory
4. File will be saved with original name and directory structure

**Bulk Extraction:**
1. Click "Extract All"
2. Choose destination directory
3. All files will be extracted maintaining their directory structure
4. Progress shown in status bar

#### Converting Images

1. Select an image file from the list
2. Choose desired format (PNG, JPEG, BMP, TIFF) in the right panel
3. Click "Convert Selected"
4. Choose save location and filename
5. Converted image will be saved

### Format-Specific Notes

#### JPEG Conversion
- RGBA images are automatically converted to RGB with white background
- Supports quality optimization
- Smaller file sizes, some quality loss

#### PNG Conversion
- Preserves transparency (alpha channel)
- Lossless compression
- Larger file sizes but perfect quality

#### BMP Conversion
- Uncompressed format
- Large file sizes
- Perfect quality, widely compatible

#### TIFF Conversion
- Professional format with metadata support
- Various compression options
- Good for archival purposes

## 🔧 XP3 Format Information

### Technical Details

The XP3 format uses the following structure:

1. **Header**: Contains format signature and basic information
2. **Index**: Compressed directory listing with file metadata
3. **Data Segments**: Actual file data, potentially compressed

### Supported Features

- ✅ File extraction
- ✅ Directory structure preservation
- ✅ Zlib decompression
- ✅ Unicode filename support
- ✅ Large file support (64-bit offsets)

### Limitations

- Some proprietary compression methods may not be supported
- Encrypted archives are not supported
- Audio and script files are extracted as-is (no conversion)

## 💻 System Requirements

### Minimum Requirements
- **Operating System**: Windows 7/8/10/11, macOS 10.12+, or Linux
- **Python**: 3.7 or later
- **RAM**: 256 MB available memory
- **Storage**: 50 MB free space for installation
- **Display**: 800x600 minimum resolution

### Recommended Requirements
- **Operating System**: Windows 10/11
- **Python**: 3.9 or later
- **RAM**: 1 GB available memory
- **Storage**: 100 MB free space
- **Display**: 1024x768 or higher resolution

### Dependencies

The application requires the following Python packages:

- **Pillow (PIL)**: For image processing and format conversion
- **tkinter**: For GUI (included with Python)
- **threading**: For background operations (built-in)
- **struct/zlib**: For XP3 format handling (built-in)

## 🔨 Building from Source

### Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/XP3-Viewer-and-Converter.git
   cd XP3-Viewer-and-Converter
   ```

2. **Create Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run in Development Mode**
   ```bash
   python xp3_viewer_converter.py
   ```

### Creating Executable

To create a standalone executable:

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build Executable**
   ```bash
   pyinstaller --windowed --onefile --name "XP3 Viewer and Converter" xp3_viewer_converter.py
   ```

3. **Find Executable**
   - Windows: `dist/XP3 Viewer and Converter.exe`
   - Linux/macOS: `dist/XP3 Viewer and Converter`

## 🔍 Troubleshooting

### Common Issues

#### "Not a valid XP3 file" Error
- **Cause**: File is corrupted or not actually an XP3 archive
- **Solution**: Verify file integrity, try with different XP3 file

#### "Python is not installed" Error
- **Cause**: Python not installed or not in system PATH
- **Solution**: Install Python from [python.org](https://python.org) and ensure "Add to PATH" is checked

#### Application Won't Start
- **Cause**: Missing dependencies
- **Solution**: Run `pip install -r requirements.txt`

#### Images Not Displaying
- **Cause**: Pillow/PIL installation issues
- **Solution**: Reinstall Pillow: `pip uninstall Pillow && pip install Pillow`

#### Slow Performance
- **Cause**: Large archives or low system resources
- **Solution**: Close other applications, upgrade RAM, or use SSD storage

### Debug Mode

To enable debug output, modify the application:

1. Edit `xp3_viewer_converter.py`
2. Change debug flag to `True` at the top of the file
3. Run application from command line to see debug output

### Getting Help

1. Check this README for solutions
2. Look at the [Issues](https://github.com/your-username/XP3-Viewer-and-Converter/issues) page
3. Create a new issue with:
   - Operating system and Python version
   - Complete error message
   - Steps to reproduce the problem
   - Sample XP3 file (if possible)

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Reporting Bugs

1. Check existing [Issues](https://github.com/your-username/XP3-Viewer-and-Converter/issues)
2. Create detailed bug report with:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if relevant

### Suggesting Features

1. Check if feature already requested
2. Create feature request with:
   - Clear description
   - Use case examples
   - Implementation ideas (if any)

### Code Contributions

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes with tests
4. Follow existing code style
5. Submit pull request with description

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Include error handling
- Test on multiple platforms
- Update documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- **Pillow**: PIL Software License
- **Python**: Python Software Foundation License

## 🙏 Acknowledgments

- KiriKiri team for the XP3 format
- Python community for excellent libraries
- Visual novel community for feedback and testing

## 📞 Contact

- **GitHub**: [XP3-Viewer-and-Converter](https://github.com/your-username/XP3-Viewer-and-Converter)
- **Issues**: [Report a Problem](https://github.com/your-username/XP3-Viewer-and-Converter/issues)

---

**Made with ❤️ for the visual novel community**
