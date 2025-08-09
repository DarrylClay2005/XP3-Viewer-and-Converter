#!/usr/bin/env python3
"""
XP3 Viewer and Converter v1.0.2 - Enhanced Edition
A Windows GUI application for extracting, viewing, and converting XP3 archive files
to different image formats (JPEG, PNG, etc.)

XP3 is an archive format used by KiriKiri visual novel engine.

Enhanced version with Windows XP styling, loading screen, and proper attribution.
Made by Darryl Clay
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import struct
import zlib
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont
import io
from pathlib import Path
import sys
import traceback
import gc
from concurrent.futures import ThreadPoolExecutor
import time
import math

# Version info
__version__ = "1.0.2"
__author__ = "Darryl Clay"

# Configuration constants
MAX_PREVIEW_SIZE = (500, 400)
MAX_THREADS = 4
CHUNK_SIZE = 8192

class LoadingSplash:
    """Loading splash screen with XP styling"""
    
    def __init__(self):
        self.splash = tk.Toplevel()
        self.splash.title("XP3 Viewer - Loading")
        self.splash.geometry("600x400")
        self.splash.configure(bg='#ECE9D8')  # Windows XP background color
        self.splash.resizable(False, False)
        
        # Center the window
        self.splash.transient()
        self.splash.grab_set()
        
        # Remove window decorations for splash effect
        self.splash.overrideredirect(True)
        
        # Center on screen
        self.center_window()
        
        self.setup_splash_ui()
        self.animate_loading()
        
    def center_window(self):
        """Center the splash window on screen"""
        self.splash.update_idletasks()
        width = 600
        height = 400
        x = (self.splash.winfo_screenwidth() // 2) - (width // 2)
        y = (self.splash.winfo_screenheight() // 2) - (height // 2)
        self.splash.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_splash_ui(self):
        """Setup the splash screen UI"""
        # Main frame
        main_frame = tk.Frame(self.splash, bg='#ECE9D8', relief='raised', bd=2)
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Title area
        title_frame = tk.Frame(main_frame, bg='#ECE9D8', height=60)
        title_frame.pack(fill='x', pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="Welcome to the first Iteration of XP3 Viewer/Converter",
                              bg='#ECE9D8', fg='#003366', font=('Arial', 14, 'bold'))
        title_label.pack(expand=True)
        
        # Logo/Icon area (create a simple XP-style icon)
        icon_frame = tk.Frame(main_frame, bg='#ECE9D8')
        icon_frame.pack(expand=True)
        
        # Create loading icon canvas
        self.icon_canvas = tk.Canvas(icon_frame, width=128, height=128, 
                                    bg='#ECE9D8', highlightthickness=0)
        self.icon_canvas.pack(pady=20)
        
        # Draw initial XP3 icon
        self.draw_xp_icon()
        
        # Progress area
        progress_frame = tk.Frame(main_frame, bg='#ECE9D8')
        progress_frame.pack(fill='x', padx=40, pady=20)
        
        self.progress_label = tk.Label(progress_frame, text="Loading application...",
                                      bg='#ECE9D8', fg='#003366', font=('Arial', 10))
        self.progress_label.pack()
        
        # Progress bar
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        
        # Bottom frame with attribution and loading icon
        bottom_frame = tk.Frame(main_frame, bg='#ECE9D8')
        bottom_frame.pack(fill='x', side='bottom', padx=10, pady=10)
        
        # Attribution on the left
        attribution_label = tk.Label(bottom_frame, text="Made by Darryl Clay",
                                    bg='#ECE9D8', fg='#666666', font=('Arial', 9))
        attribution_label.pack(side='left')
        
        # Loading icon on the right
        self.loading_canvas = tk.Canvas(bottom_frame, width=24, height=24,
                                       bg='#ECE9D8', highlightthickness=0)
        self.loading_canvas.pack(side='right')
        
        # Animation variables
        self.loading_angle = 0
        self.icon_pulse = 0
        
    def draw_xp_icon(self):
        """Draw Windows XP style icon"""
        self.icon_canvas.delete("all")
        
        # Create a pulsing effect
        pulse_factor = 0.9 + 0.1 * math.sin(self.icon_pulse)
        base_size = 100
        size = int(base_size * pulse_factor)
        offset = (128 - size) // 2
        
        # Windows XP blue gradient colors
        colors = ['#4A90E2', '#357ABD', '#2E5F8E', '#1F4788']
        
        # Draw layered icon effect
        for i, color in enumerate(colors):
            layer_size = size - i * 3
            layer_offset = offset + i * 1.5
            if layer_size > 0:
                self.icon_canvas.create_rectangle(
                    layer_offset, layer_offset,
                    layer_offset + layer_size, layer_offset + layer_size,
                    fill=color, outline='', width=0
                )
        
        # Draw XP3 text
        if size > 60:
            text_y = offset + size // 2
            self.icon_canvas.create_text(64, text_y, text="XP3",
                                        fill='white', font=('Arial', 16, 'bold'))
        
    def draw_loading_spinner(self):
        """Draw animated loading spinner"""
        self.loading_canvas.delete("all")
        
        center_x, center_y = 12, 12
        radius = 8
        
        # Draw spinning segments
        for i in range(8):
            angle = (self.loading_angle + i * 45) % 360
            angle_rad = math.radians(angle)
            
            # Calculate segment position
            x1 = center_x + (radius - 3) * math.cos(angle_rad)
            y1 = center_y + (radius - 3) * math.sin(angle_rad)
            x2 = center_x + radius * math.cos(angle_rad)
            y2 = center_y + radius * math.sin(angle_rad)
            
            # Fade effect based on segment age
            opacity = int(255 * (i + 1) / 8)
            color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            
            self.loading_canvas.create_line(x1, y1, x2, y2, 
                                           fill='#4A90E2', width=2, capstyle='round')
    
    def animate_loading(self):
        """Animate the loading elements"""
        # Update progress bar
        self.progress.step(2)
        
        # Update icon pulse
        self.icon_pulse += 0.1
        self.draw_xp_icon()
        
        # Update loading spinner
        self.loading_angle += 15
        self.draw_loading_spinner()
        
        # Continue animation
        self.splash.after(50, self.animate_loading)
        
    def destroy(self):
        """Close the splash screen"""
        self.splash.destroy()

class XP3Archive:
    """Optimized XP3 archive format handler with improved error handling"""
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.files = {}
        self.loaded = False
        self.file_size = 0
    
    def load(self):
        """Load and parse XP3 archive with enhanced error handling"""
        try:
            if not self.filepath.exists():
                raise FileNotFoundError(f"XP3 file not found: {self.filepath}")
            
            self.file_size = self.filepath.stat().st_size
            if self.file_size < 32:  # Minimum XP3 file size
                raise ValueError("File too small to be a valid XP3 archive")
            
            with open(self.filepath, 'rb') as f:
                # Check XP3 signature
                signature = f.read(11)
                if signature != b'XP3\r\n \n\x1a\x8b\x67\x01':
                    raise ValueError("Not a valid XP3 file - invalid signature")
                
                # Read index offset
                f.seek(-8, 2)  # Go to end of file minus 8 bytes
                index_offset_data = f.read(8)
                if len(index_offset_data) != 8:
                    raise ValueError("Corrupted XP3 file - cannot read index offset")
                
                index_offset = struct.unpack('<Q', index_offset_data)[0]
                
                # Validate index offset
                if index_offset >= self.file_size or index_offset < 11:
                    raise ValueError("Invalid index offset in XP3 file")
                
                # Read index
                f.seek(index_offset)
                self._read_index(f)
                
                self.loaded = True
                return True
                
        except Exception as e:
            error_msg = f"Error loading XP3 file {self.filepath.name}: {str(e)}"
            print(error_msg)
            if hasattr(e, '__traceback__'):
                traceback.print_exc()
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
    """Enhanced XP3 Viewer with Windows XP styling and attribution"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"XP3 Viewer and Converter v{__version__}")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)
        
        # Windows XP styling
        self.root.configure(bg='#ECE9D8')
        
        # Try to set icon if available
        try:
            if os.path.exists('xp3_icon.ico'):
                self.root.iconbitmap('xp3_icon.ico')
        except:
            pass
        
        self.current_archive = None
        self.current_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface with XP styling"""
        # Create main menu
        menubar = tk.Menu(self.root, bg='#ECE9D8')
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0, bg='#ECE9D8')
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open XP3 Archive...", command=self.open_archive)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0, bg='#ECE9D8')
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Create main frame with XP styling
        main_frame = tk.Frame(self.root, bg='#ECE9D8')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create paned window for left/right split
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - file list with XP styling
        left_frame = tk.Frame(paned, bg='#ECE9D8')
        paned.add(left_frame, weight=1)
        
        tk.Label(left_frame, text="Archive Contents:", bg='#ECE9D8', 
                font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=2)
        
        # File listbox with scrollbar
        listbox_frame = tk.Frame(left_frame, bg='#ECE9D8')
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.file_listbox = tk.Listbox(listbox_frame, bg='white', fg='black',
                                      selectbackground='#316AC5', selectforeground='white')
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Buttons frame with XP styling
        button_frame = tk.Frame(left_frame, bg='#ECE9D8')
        button_frame.pack(fill=tk.X, pady=5)
        
        extract_btn = tk.Button(button_frame, text="Extract Selected", 
                               command=self.extract_selected, bg='#E1E1E1',
                               relief='raised', font=('Arial', 9))
        extract_btn.pack(side=tk.LEFT, padx=2)
        
        extract_all_btn = tk.Button(button_frame, text="Extract All", 
                                   command=self.extract_all, bg='#E1E1E1',
                                   relief='raised', font=('Arial', 9))
        extract_all_btn.pack(side=tk.LEFT, padx=2)
        
        # Right panel - preview and conversion with XP styling
        right_frame = tk.Frame(paned, bg='#ECE9D8')
        paned.add(right_frame, weight=2)
        
        # Preview area
        preview_label = tk.Label(right_frame, text="Preview:", bg='#ECE9D8',
                               font=('Arial', 10, 'bold'))
        preview_label.pack(anchor=tk.W, pady=2)
        
        self.preview_frame = tk.Frame(right_frame, relief=tk.SUNKEN, borderwidth=2,
                                     bg='white')
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=2)
        
        self.image_label = tk.Label(self.preview_frame, text="Select a file to preview",
                                   bg='white', fg='gray')
        self.image_label.pack(expand=True)
        
        # Conversion controls with XP styling
        conv_frame = tk.LabelFrame(right_frame, text="Convert to:", bg='#ECE9D8',
                                  font=('Arial', 10, 'bold'))
        conv_frame.pack(fill=tk.X, pady=5)
        
        format_frame = tk.Frame(conv_frame, bg='#ECE9D8')
        format_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.format_var = tk.StringVar(value="PNG")
        tk.Radiobutton(format_frame, text="PNG", variable=self.format_var, 
                      value="PNG", bg='#ECE9D8').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_frame, text="JPEG", variable=self.format_var, 
                      value="JPEG", bg='#ECE9D8').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_frame, text="BMP", variable=self.format_var, 
                      value="BMP", bg='#ECE9D8').pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(format_frame, text="TIFF", variable=self.format_var, 
                      value="TIFF", bg='#ECE9D8').pack(side=tk.LEFT, padx=5)
        
        convert_btn = tk.Button(conv_frame, text="Convert Selected", 
                               command=self.convert_selected, bg='#E1E1E1',
                               relief='raised', font=('Arial', 9))
        convert_btn.pack(pady=5)
        
        # Bottom frame for attribution and loading icon
        bottom_frame = tk.Frame(self.root, bg='#ECE9D8', relief='sunken', bd=1)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(bottom_frame, textvariable=self.status_var,
                             anchor=tk.W, bg='#ECE9D8', font=('Arial', 9))
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)
        
        # Attribution label
        attribution_label = tk.Label(bottom_frame, text="Made by Darryl Clay",
                                    bg='#ECE9D8', fg='#666666', font=('Arial', 8))
        attribution_label.pack(side=tk.RIGHT, padx=10, pady=2)
        
        # Small loading icon space
        self.loading_canvas = tk.Canvas(bottom_frame, width=20, height=20,
                                       bg='#ECE9D8', highlightthickness=0)
        self.loading_canvas.pack(side=tk.RIGHT, padx=5, pady=2)
        
    def show_loading_icon(self, show=True):
        """Show or hide loading animation"""
        self.loading_canvas.delete("all")
        if show:
            # Simple loading animation
            self.animate_loading_icon()
    
    def animate_loading_icon(self):
        """Animate the small loading icon"""
        if hasattr(self, '_loading_angle'):
            self._loading_angle = (self._loading_angle + 15) % 360
        else:
            self._loading_angle = 0
            
        self.loading_canvas.delete("all")
        
        center_x, center_y = 10, 10
        radius = 6
        
        # Draw spinning segments
        for i in range(6):
            angle = (self._loading_angle + i * 60) % 360
            angle_rad = math.radians(angle)
            
            x = center_x + radius * math.cos(angle_rad)
            y = center_y + radius * math.sin(angle_rad)
            
            # Fade effect
            opacity = int(150 + 105 * i / 6)
            color = f"#{opacity:02x}{opacity:02x}{opacity:02x}"
            
            self.loading_canvas.create_oval(x-1, y-1, x+1, y+1, 
                                           fill='#4A90E2', outline='')
        
        if hasattr(self, '_loading_active') and self._loading_active:
            self.root.after(100, self.animate_loading_icon)
    
    def open_archive(self):
        """Open XP3 archive file"""
        filepath = filedialog.askopenfilename(
            title="Open XP3 Archive",
            filetypes=[("XP3 Archives", "*.xp3"), ("All files", "*.*")]
        )
        
        if filepath:
            self.load_archive(filepath)
    
    def load_archive(self, filepath):
        """Load archive in background thread with loading animation"""
        def load_worker():
            self._loading_active = True
            self.show_loading_icon(True)
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
            
            self._loading_active = False
            self.root.after(0, lambda: self.show_loading_icon(False))
        
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
                self._loading_active = True
                self.root.after(0, lambda: self.show_loading_icon(True))
                
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
            finally:
                self._loading_active = False
                self.root.after(0, lambda: self.show_loading_icon(False))
        
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
            self._loading_active = True
            self.root.after(0, lambda: self.show_loading_icon(True))
            
            files = self.current_archive.list_files()
            total = len(files)
            
            for i, filename in enumerate(files):
                self.root.after(0, lambda i=i, total=total: 
                    self.status_var.set(f"Extracting {i+1}/{total}..."))
                
                try:
                    self.extract_file_to_directory(filename, output_dir)
                except Exception as e:
                    print(f"Error extracting {filename}: {e}")
            
            self._loading_active = False
            self.root.after(0, lambda: self.show_loading_icon(False))
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
                self._loading_active = True
                self.root.after(0, lambda: self.show_loading_icon(True))
                
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
            finally:
                self._loading_active = False
                self.root.after(0, lambda: self.show_loading_icon(False))
        
        threading.Thread(target=convert_worker, daemon=True).start()
    
    def show_about(self):
        """Show about dialog with proper attribution"""
        about_text = f"""XP3 Viewer and Converter v{__version__}
First Iteration of XP3 Viewer/Converter

A tool for extracting, viewing, and converting files from XP3 archives.
XP3 is an archive format used by the KiriKiri visual novel engine.

Features:
• Extract individual files or entire archives
• Preview image files with optimized rendering
• Convert images to PNG, JPEG, BMP, or TIFF formats
• Enhanced error handling and performance
• Windows XP styling and theming
• Loading animations and status indicators

Made by {__author__}
Created with Python and tkinter.

Thank you for using XP3 Viewer and Converter!"""
        
        messagebox.showinfo("About XP3 Viewer and Converter", about_text)

def main():
    """Main application entry point with loading splash"""
    # Create root window (hidden initially)
    root = tk.Tk()
    root.withdraw()
    
    # Show loading splash
    splash = LoadingSplash()
    
    # Simulate loading time
    def finish_loading():
        splash.destroy()
        root.deiconify()  # Show main window
        app = XP3ViewerConverter(root)
        root.mainloop()
    
    # Wait for loading to complete (simulate 3 seconds of loading)
    root.after(3000, finish_loading)
    root.mainloop()

if __name__ == "__main__":
    main()
