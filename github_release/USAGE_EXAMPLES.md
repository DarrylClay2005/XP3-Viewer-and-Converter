# Usage Examples for XP3 Viewer and Converter

This document provides detailed examples of how to use the XP3 Viewer and Converter application.

## Table of Contents

- [Basic Usage](#basic-usage)
- [Command Line Usage](#command-line-usage)
- [Programmatic Usage](#programmatic-usage)
- [Common Use Cases](#common-use-cases)
- [Tips and Tricks](#tips-and-tricks)

## Basic Usage

### Starting the Application

#### Windows
```batch
# Method 1: Using the batch file (easiest)
run_xp3_viewer.bat

# Method 2: Direct Python execution
python xp3_viewer_converter.py
```

#### Linux/macOS
```bash
# Method 1: With virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python xp3_viewer_converter.py

# Method 2: Direct execution (if dependencies are installed)
python3 xp3_viewer_converter.py
```

### Loading an XP3 Archive

1. **Launch the application**
2. **Open File Menu**: Click `File → Open XP3 Archive...`
3. **Browse for File**: Navigate to your XP3 file and select it
4. **Wait for Loading**: The status bar will show progress
5. **Browse Contents**: Files will appear in the left panel

### Extracting Files

#### Single File Extraction
```
1. Select a file from the list on the left
2. Click "Extract Selected"
3. Choose destination folder
4. File will be saved maintaining directory structure
```

#### Bulk Extraction
```
1. Click "Extract All"
2. Choose destination folder
3. Wait for extraction to complete
4. All files will be saved with original structure
```

### Converting Images

```
1. Select an image file (will show preview on right)
2. Choose output format: PNG, JPEG, BMP, or TIFF
3. Click "Convert Selected"
4. Choose save location and filename
5. Image will be converted and saved
```

## Command Line Usage

While the application is primarily GUI-based, you can create scripts for automation:

### Python Script Example

```python
#!/usr/bin/env python3
"""
Example script for batch processing XP3 files
"""

from xp3_viewer_converter import XP3Archive
import os
from PIL import Image
import io

def extract_all_images(xp3_path, output_dir):
    """Extract all images from XP3 archive"""
    archive = XP3Archive(xp3_path)
    
    if not archive.load():
        print(f"Failed to load {xp3_path}")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff']
    
    for filename in archive.list_files():
        # Check if file might be an image
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            try:
                data = archive.extract_file(filename)
                if data:
                    # Try to open as image
                    image = Image.open(io.BytesIO(data))
                    
                    # Save as PNG
                    output_path = os.path.join(output_dir, filename + '.png')
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    image.save(output_path, 'PNG')
                    print(f"Converted: {filename} -> {output_path}")
                    
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Usage
if __name__ == "__main__":
    extract_all_images("sample.xp3", "output_images/")
```

## Programmatic Usage

### Using the XP3Archive Class

```python
from xp3_viewer_converter import XP3Archive

# Load an archive
archive = XP3Archive("path/to/your/file.xp3")
if archive.load():
    print(f"Loaded archive with {len(archive.files)} files")
    
    # List all files
    for filename in archive.list_files():
        print(f"  - {filename}")
    
    # Extract a specific file
    data = archive.extract_file("image.png")
    if data:
        with open("extracted_image.png", "wb") as f:
            f.write(data)
else:
    print("Failed to load archive")
```

### Batch Image Conversion

```python
from xp3_viewer_converter import XP3Archive
from PIL import Image
import io
import os

def convert_xp3_images(xp3_file, output_format="PNG"):
    """Convert all images in XP3 to specified format"""
    archive = XP3Archive(xp3_file)
    
    if not archive.load():
        return False
    
    converted = 0
    for filename in archive.list_files():
        try:
            data = archive.extract_file(filename)
            if not data:
                continue
                
            # Try to load as image
            image = Image.open(io.BytesIO(data))
            
            # Convert filename to new extension
            base_name = os.path.splitext(filename)[0]
            output_name = f"{base_name}.{output_format.lower()}"
            
            # Handle RGBA to RGB conversion for JPEG
            if output_format.upper() == "JPEG" and image.mode == "RGBA":
                background = Image.new("RGB", image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            
            image.save(output_name, format=output_format)
            converted += 1
            print(f"Converted: {filename} -> {output_name}")
            
        except Exception as e:
            print(f"Skipped {filename}: {e}")
    
    print(f"Converted {converted} images")
    return True

# Usage example
convert_xp3_images("game_assets.xp3", "PNG")
```

## Common Use Cases

### 1. Visual Novel Asset Extraction

Many visual novels use XP3 archives for storing character sprites, backgrounds, and UI elements.

```python
def extract_vn_assets(xp3_file):
    """Extract visual novel assets organized by type"""
    archive = XP3Archive(xp3_file)
    archive.load()
    
    # Organize by folder structure
    sprites = [f for f in archive.list_files() if "chara" in f.lower()]
    backgrounds = [f for f in archive.list_files() if "bg" in f.lower()]
    ui_elements = [f for f in archive.list_files() if "ui" in f.lower()]
    
    # Extract organized
    for category, files in [("sprites", sprites), ("backgrounds", backgrounds), ("ui", ui_elements)]:
        os.makedirs(category, exist_ok=True)
        for filename in files:
            data = archive.extract_file(filename)
            if data:
                output_path = os.path.join(category, os.path.basename(filename))
                with open(output_path, "wb") as f:
                    f.write(data)
```

### 2. Image Format Standardization

Convert all images to a consistent format for use in other tools:

```python
def standardize_images(xp3_file, target_format="PNG"):
    """Convert all images to standard format"""
    archive = XP3Archive(xp3_file)
    archive.load()
    
    for filename in archive.list_files():
        data = archive.extract_file(filename)
        if not data:
            continue
            
        try:
            image = Image.open(io.BytesIO(data))
            base_name = os.path.splitext(filename)[0]
            output_file = f"{base_name}.{target_format.lower()}"
            image.save(output_file, format=target_format)
        except:
            # Not an image file, skip
            continue
```

### 3. Quality Assessment

Check image properties before conversion:

```python
def analyze_images(xp3_file):
    """Analyze images in XP3 archive"""
    archive = XP3Archive(xp3_file)
    archive.load()
    
    stats = {"total": 0, "formats": {}, "sizes": []}
    
    for filename in archive.list_files():
        data = archive.extract_file(filename)
        if not data:
            continue
            
        try:
            image = Image.open(io.BytesIO(data))
            stats["total"] += 1
            
            # Track format
            fmt = image.format or "Unknown"
            stats["formats"][fmt] = stats["formats"].get(fmt, 0) + 1
            
            # Track size
            stats["sizes"].append(image.size)
            
            print(f"{filename}: {image.size}, {image.mode}, {fmt}")
            
        except:
            continue
    
    print(f"\nSummary: {stats['total']} images")
    print(f"Formats: {stats['formats']}")
```

## Tips and Tricks

### Performance Optimization

1. **Use SSD Storage**: XP3 files can be large; SSD improves loading speed
2. **Close Other Applications**: Free up RAM for large archives
3. **Batch Operations**: Use "Extract All" instead of individual extractions

### File Handling

1. **Check File Extensions**: Not all files in XP3 are images
2. **Preserve Directory Structure**: The application maintains original folder organization
3. **Unicode Support**: XP3 supports Unicode filenames

### Conversion Best Practices

1. **PNG for Quality**: Use PNG for images requiring transparency
2. **JPEG for Size**: Use JPEG for photographs or large images where slight quality loss is acceptable
3. **BMP for Compatibility**: Use BMP for maximum compatibility with older software
4. **TIFF for Archival**: Use TIFF for long-term storage with metadata

### Troubleshooting

#### Large Files
```python
# For very large archives, process files in chunks
def process_large_archive(xp3_file, chunk_size=100):
    archive = XP3Archive(xp3_file)
    archive.load()
    
    files = archive.list_files()
    for i in range(0, len(files), chunk_size):
        chunk = files[i:i+chunk_size]
        print(f"Processing chunk {i//chunk_size + 1}")
        
        for filename in chunk:
            # Process file
            data = archive.extract_file(filename)
            # ... handle data ...
```

#### Memory Management
```python
# Clear image data after processing to save memory
def memory_efficient_conversion(xp3_file):
    archive = XP3Archive(xp3_file)
    archive.load()
    
    for filename in archive.list_files():
        data = archive.extract_file(filename)
        if data:
            try:
                image = Image.open(io.BytesIO(data))
                # Process image
                image.save(f"converted_{filename}", "PNG")
                # Clear references
                image.close()
                del image
                del data
            except:
                continue
```

### Integration Examples

#### With Game Development
```python
# Extract assets for game development
def extract_for_unity(xp3_file):
    """Extract assets in Unity-friendly format"""
    archive = XP3Archive(xp3_file)
    archive.load()
    
    # Unity prefers PNG for sprites
    for filename in archive.list_files():
        if any(keyword in filename.lower() for keyword in ["sprite", "character", "ui"]):
            data = archive.extract_file(filename)
            if data:
                try:
                    image = Image.open(io.BytesIO(data))
                    # Unity naming convention
                    clean_name = filename.replace(" ", "_").replace("-", "_")
                    image.save(f"Assets/Sprites/{clean_name}.png", "PNG")
                except:
                    continue
```

#### With Web Development
```python
# Optimize images for web use
def extract_for_web(xp3_file):
    """Extract and optimize images for web"""
    archive = XP3Archive(xp3_file)
    archive.load()
    
    for filename in archive.list_files():
        data = archive.extract_file(filename)
        if data:
            try:
                image = Image.open(io.BytesIO(data))
                
                # Optimize for web
                if image.size[0] > 1920 or image.size[1] > 1080:
                    image.thumbnail((1920, 1080), Image.Resampling.LANCZOS)
                
                # Save as optimized JPEG or PNG
                if image.mode == "RGBA":
                    image.save(f"web_{filename}.png", "PNG", optimize=True)
                else:
                    image.save(f"web_{filename}.jpg", "JPEG", quality=85, optimize=True)
            except:
                continue
```

This comprehensive guide should help you make the most of the XP3 Viewer and Converter application!
