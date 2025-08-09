#!/usr/bin/env python3
"""
XP3 Viewer and Converter
A Windows GUI application for extracting, viewing, and converting XP3 archive files
to different image formats (JPEG, PNG, etc.)

XP3 is an archive format used by KiriKiri visual novel engine.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import struct
import zlib
import threading
from PIL import Image, ImageTk
import io
from pathlib import Path
import json

class XP3Archive:
    """Handle XP3 archive format operations"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.files = {}
        self.loaded = False
    
    def load(self):
        """Load and parse XP3 archive"""
        try:
            with open(self.filepath, 'rb') as f:
                # Check XP3 signature
                signature = f.read(11)
                if signature != b'XP3\r\n \n\x1a\x8b\x67\x01':
                    raise ValueError("Not a valid XP3 file")
                
                # Read index offset
                f.seek(-8, 2)  # Go to end of file minus 8 bytes
                index_offset = struct.unpack('<Q', f.read(8))[0]
                
                # Read index
                f.seek(index_offset)
                self._read_index(f)
                
                self.loaded = True
                return True
                
        except Exception as e:
            print(f"Error loading XP3 file: {e}")
            return False
    
    def _read_index(self, f):
        """Read the file index from XP3 archive"""
        # Skip index header
        f.read(1)  # Skip compressed flag
        index_size = struct.unpack('<Q', f.read(8))[0]
        
        # Read and decompress index if needed
        index_data = f.read(index_size)
        if index_data[0:2] == b'\x78\x9c':  # zlib compressed
            index_data = zlib.decompress(index_data)
        
        # Parse index entries
        pos = 0
        while pos < len(index_data):
            if pos + 4 > len(index_data):
                break
                
            entry_size = struct.unpack('<I', index_data[pos:pos+4])[0]
            if entry_size == 0:
                break
                
            entry_data = index_data[pos+4:pos+4+entry_size]
            self._parse_file_entry(entry_data)
            pos += 4 + entry_size
    
    def _parse_file_entry(self, entry_data):
        """Parse individual file entry from index"""
        pos = 0
        file_info = {}
        
        # Read filename
        filename_len = struct.unpack('<H', entry_data[pos:pos+2])[0]
        pos += 2
        filename = entry_data[pos:pos+filename_len*2].decode('utf-16le')
        pos += filename_len * 2
        
        # Read file segments
        segments = []
        while pos < len(entry_data):
            if pos + 4 > len(entry_data):
                break
                
            segment_type = entry_data[pos:pos+4]
            pos += 4
            
            if segment_type == b'file':
                # File segment
                pos += 8  # Skip size
                offset = struct.unpack('<Q', entry_data[pos:pos+8])[0]
                pos += 8
                size = struct.unpack('<Q', entry_data[pos:pos+8])[0]
                pos += 8
                segments.append(('file', offset, size))
                
            elif segment_type == b'info':
                # Info segment  
                pos += 8  # Skip size
                flags = struct.unpack('<I', entry_data[pos:pos+4])[0]
                pos += 4
                orig_size = struct.unpack('<Q', entry_data[pos:pos+8])[0]
                pos += 8
                file_info['compressed'] = (flags & 7) != 0
                file_info['original_size'] = orig_size
                
            else:
                # Unknown segment, skip
                if pos + 8 <= len(entry_data):
                    segment_size = struct.unpack('<Q', entry_data[pos:pos+8])[0]
                    pos += 8 + segment_size
                else:
                    break
        
        if segments:
            file_info['segments'] = segments
            self.files[filename] = file_info
    
    def extract_file(self, filename):
        """Extract a single file from the archive"""
        if not self.loaded or filename not in self.files:
            return None
            
        file_info = self.files[filename]
        data = b''
        
        with open(self.filepath, 'rb') as f:
            for segment_type, offset, size in file_info['segments']:
                if segment_type == 'file':
                    f.seek(offset)
                    data += f.read(size)
        
        # Decompress if needed
        if file_info.get('compressed', False):
            try:
                data = zlib.decompress(data)
            except:
                pass  # If decompression fails, return raw data
                
        return data
    
    def list_files(self):
        """Return list of files in archive"""
        return list(self.files.keys()) if self.loaded else []

class XP3ViewerConverter:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("XP3 Viewer and Converter")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        self.current_archive = None
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Create main menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open XP3 Archive...", command=self.open_archive)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create paned window for left/right split
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - file list
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Archive Contents:").pack(anchor=tk.W, pady=2)
        
        # File listbox with scrollbar
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Buttons frame
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Extract Selected", 
                  command=self.extract_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Extract All", 
                  command=self.extract_all).pack(side=tk.LEFT, padx=2)
        
        # Right panel - preview and conversion
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # Preview area
        preview_label = ttk.Label(right_frame, text="Preview:")
        preview_label.pack(anchor=tk.W, pady=2)
        
        self.preview_frame = ttk.Frame(right_frame, relief=tk.SUNKEN, borderwidth=2)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.image_label = ttk.Label(self.preview_frame, text="Select a file to preview")
        self.image_label.pack(expand=True)
        
        # Conversion controls
        conv_frame = ttk.LabelFrame(right_frame, text="Convert to:")
        conv_frame.pack(fill=tk.X, pady=5)
        
        format_frame = ttk.Frame(conv_frame)
        format_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.format_var = tk.StringVar(value="PNG")
        ttk.Radiobutton(format_frame, text="PNG", variable=self.format_var, 
                       value="PNG").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, 
                       value="JPEG").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="BMP", variable=self.format_var, 
                       value="BMP").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="TIFF", variable=self.format_var, 
                       value="TIFF").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(conv_frame, text="Convert Selected", 
                  command=self.convert_selected).pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def open_archive(self):
        """Open XP3 archive file"""
        filepath = filedialog.askopenfilename(
            title="Open XP3 Archive",
            filetypes=[("XP3 Archives", "*.xp3"), ("All files", "*.*")]
        )
        
        if filepath:
            self.load_archive(filepath)
    
    def load_archive(self, filepath):
        """Load archive in background thread"""
        def load_worker():
            self.status_var.set("Loading archive...")
            self.current_archive = XP3Archive(filepath)
            
            if self.current_archive.load():
                # Update UI in main thread
                self.root.after(0, self.update_file_list)
                self.root.after(0, lambda: self.status_var.set(
                    f"Loaded {len(self.current_archive.files)} files from {os.path.basename(filepath)}"))
            else:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", "Failed to load XP3 archive. File may be corrupted or not a valid XP3 file."))
                self.root.after(0, lambda: self.status_var.set("Failed to load archive"))
        
        threading.Thread(target=load_worker, daemon=True).start()
    
    def update_file_list(self):
        """Update the file listbox with archive contents"""
        self.file_listbox.delete(0, tk.END)
        if self.current_archive:
            files = sorted(self.current_archive.list_files())
            for filename in files:
                self.file_listbox.insert(tk.END, filename)
    
    def on_file_select(self, event):
        """Handle file selection in listbox"""
        selection = self.file_listbox.curselection()
        if not selection or not self.current_archive:
            return
            
        filename = self.file_listbox.get(selection[0])
        self.preview_file(filename)
    
    def preview_file(self, filename):
        """Preview selected file if it's an image"""
        def preview_worker():
            try:
                data = self.current_archive.extract_file(filename)
                if not data:
                    return
                
                # Try to load as image
                try:
                    image = Image.open(io.BytesIO(data))
                    self.current_image = image
                    
                    # Resize for preview
                    preview_size = (400, 300)
                    image.thumbnail(preview_size, Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(image)
                    
                    # Update UI in main thread
                    def update_preview():
                        self.image_label.config(image=photo, text="")
                        self.image_label.image = photo  # Keep reference
                        
                    self.root.after(0, update_preview)
                    
                except Exception:
                    # Not an image file
                    self.root.after(0, lambda: self.image_label.config(
                        image="", text=f"Cannot preview {filename}\n(Not an image file)"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.image_label.config(
                    image="", text=f"Error previewing file:\n{str(e)}"))
        
        threading.Thread(target=preview_worker, daemon=True).start()
    
    def extract_selected(self):
        """Extract selected file"""
        selection = self.file_listbox.curselection()
        if not selection or not self.current_archive:
            messagebox.showwarning("Warning", "Please select a file to extract")
            return
            
        filename = self.file_listbox.get(selection[0])
        
        # Choose output directory
        output_dir = filedialog.askdirectory(title="Choose output directory")
        if not output_dir:
            return
            
        self.extract_file_to_directory(filename, output_dir)
    
    def extract_all(self):
        """Extract all files from archive"""
        if not self.current_archive:
            messagebox.showwarning("Warning", "No archive loaded")
            return
            
        # Choose output directory
        output_dir = filedialog.askdirectory(title="Choose output directory")
        if not output_dir:
            return
            
        def extract_worker():
            files = self.current_archive.list_files()
            total = len(files)
            
            for i, filename in enumerate(files):
                self.root.after(0, lambda i=i, total=total: 
                    self.status_var.set(f"Extracting {i+1}/{total}..."))
                
                try:
                    self.extract_file_to_directory(filename, output_dir)
                except Exception as e:
                    print(f"Error extracting {filename}: {e}")
            
            self.root.after(0, lambda: self.status_var.set(f"Extracted {total} files"))
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                f"Successfully extracted {total} files to {output_dir}"))
        
        threading.Thread(target=extract_worker, daemon=True).start()
    
    def extract_file_to_directory(self, filename, output_dir):
        """Extract single file to directory"""
        data = self.current_archive.extract_file(filename)
        if data:
            output_path = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(data)
    
    def convert_selected(self):
        """Convert selected image file to chosen format"""
        selection = self.file_listbox.curselection()
        if not selection or not self.current_archive:
            messagebox.showwarning("Warning", "Please select a file to convert")
            return
            
        filename = self.file_listbox.get(selection[0])
        
        # Get output file path
        format_ext = self.format_var.get().lower()
        output_file = filedialog.asksaveasfilename(
            title="Save converted image as",
            defaultextension=f".{format_ext}",
            filetypes=[(f"{self.format_var.get()} files", f"*.{format_ext}")]
        )
        
        if not output_file:
            return
            
        def convert_worker():
            try:
                data = self.current_archive.extract_file(filename)
                if not data:
                    raise Exception("Failed to extract file")
                
                # Load as image
                image = Image.open(io.BytesIO(data))
                
                # Convert and save
                if self.format_var.get() == "JPEG" and image.mode == "RGBA":
                    # Convert RGBA to RGB for JPEG
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
                    image = background
                
                image.save(output_file, format=self.format_var.get())
                
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Image converted and saved to {output_file}"))
                self.root.after(0, lambda: self.status_var.set("Conversion completed"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    f"Failed to convert image: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Conversion failed"))
        
        threading.Thread(target=convert_worker, daemon=True).start()
    
    def show_about(self):
        """Show about dialog"""
        about_text = """XP3 Viewer and Converter v1.0

A tool for extracting, viewing, and converting files from XP3 archives.
XP3 is an archive format used by the KiriKiri visual novel engine.

Features:
• Extract individual files or entire archives
• Preview image files
• Convert images to PNG, JPEG, BMP, or TIFF formats
• Cross-platform support

Created with Python and tkinter."""
        
        messagebox.showinfo("About XP3 Viewer and Converter", about_text)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = XP3ViewerConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
