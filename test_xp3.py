#!/usr/bin/env python3
"""
Test script for XP3 Viewer and Converter
This script tests basic functionality without requiring actual XP3 files.
"""

import unittest
import tempfile
import os
import struct
import zlib
from io import BytesIO
from xp3_viewer_converter import XP3Archive

class TestXP3Archive(unittest.TestCase):
    """Test cases for XP3Archive class"""
    
    def create_mock_xp3(self, files_data):
        """Create a mock XP3 file for testing"""
        # This is a simplified mock - real XP3 files are more complex
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xp3') as f:
            # Write XP3 signature
            f.write(b'XP3\r\n \n\x1a\x8b\x67\x01')
            
            # Write some dummy data
            f.write(b'dummy data for testing')
            
            # Write index offset at the end
            index_offset = f.tell()
            f.write(struct.pack('<Q', index_offset))
            
            return f.name
    
    def test_xp3_signature_validation(self):
        """Test XP3 file signature validation"""
        # Create a file with wrong signature
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xp3') as f:
            f.write(b'NOT_XP3_FILE')
            wrong_file = f.name
        
        archive = XP3Archive(wrong_file)
        result = archive.load()
        self.assertFalse(result, "Should reject files with wrong signature")
        
        # Clean up
        os.unlink(wrong_file)
    
    def test_nonexistent_file(self):
        """Test handling of non-existent files"""
        archive = XP3Archive("nonexistent_file.xp3")
        result = archive.load()
        self.assertFalse(result, "Should handle non-existent files gracefully")
    
    def test_empty_archive_operations(self):
        """Test operations on unloaded archive"""
        archive = XP3Archive("dummy.xp3")
        
        # Test file list on unloaded archive
        files = archive.list_files()
        self.assertEqual(files, [], "Unloaded archive should return empty file list")
        
        # Test file extraction on unloaded archive
        data = archive.extract_file("dummy.txt")
        self.assertIsNone(data, "Should return None for unloaded archive")

def run_gui_test():
    """Test GUI creation without showing window"""
    print("Testing GUI creation...")
    
    try:
        import tkinter as tk
        from xp3_viewer_converter import XP3ViewerConverter
        
        # Create root window but don't show it
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create application instance
        app = XP3ViewerConverter(root)
        
        # Test that UI elements were created
        assert hasattr(app, 'file_listbox'), "File listbox should be created"
        assert hasattr(app, 'image_label'), "Image label should be created"
        assert hasattr(app, 'format_var'), "Format variable should be created"
        
        print("✓ GUI creation test passed")
        root.destroy()
        
    except ImportError as e:
        print(f"⚠ GUI test skipped: {e}")
    except Exception as e:
        print(f"✗ GUI test failed: {e}")

def test_dependencies():
    """Test that required dependencies are available"""
    print("Testing dependencies...")
    
    try:
        import tkinter
        print("✓ tkinter available")
    except ImportError:
        print("✗ tkinter not available")
        return False
    
    try:
        from PIL import Image, ImageTk
        print("✓ Pillow (PIL) available")
    except ImportError:
        print("✗ Pillow (PIL) not available")
        return False
    
    try:
        import threading
        import struct
        import zlib
        import os
        import io
        print("✓ Standard library modules available")
    except ImportError:
        print("✗ Some standard library modules not available")
        return False
    
    return True

def main():
    """Main test function"""
    print("XP3 Viewer and Converter - Test Suite")
    print("=" * 40)
    
    # Test dependencies
    if not test_dependencies():
        print("\n❌ Dependency test failed!")
        return
    
    print("\n📦 Dependencies test passed!")
    
    # Test GUI creation
    print("\n🖼️ Testing GUI...")
    run_gui_test()
    
    # Run unit tests
    print("\n🧪 Running unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n✅ All tests completed!")
    print("\nTo run the full application:")
    print("  Windows: Double-click 'run_xp3_viewer.bat'")
    print("  Linux/Mac: python xp3_viewer_converter.py")

if __name__ == "__main__":
    main()
