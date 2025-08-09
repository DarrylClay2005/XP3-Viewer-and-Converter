#!/usr/bin/env python3
"""
Create a Windows XP style icon for the XP3 Viewer
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_xp_icon(size=(64, 64)):
    """Create a Windows XP style icon"""
    # Create a new image with transparency
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Windows XP blue colors
    light_blue = (121, 180, 255)
    dark_blue = (49, 106, 197)
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Draw the main window shape
    margin = 4
    window_rect = (margin, margin, size[0] - margin, size[1] - margin)
    
    # Draw window background with gradient effect
    for i in range(margin, size[1] - margin):
        alpha = 1.0 - (i - margin) / (size[1] - 2 * margin)
        color = tuple(int(light_blue[j] * alpha + white[j] * (1 - alpha)) for j in range(3))
        draw.rectangle((margin, i, size[0] - margin, i + 1), fill=color + (255,))
    
    # Draw window border
    draw.rectangle(window_rect, outline=dark_blue, width=2)
    
    # Draw title bar
    title_height = 16
    draw.rectangle((margin + 2, margin + 2, size[0] - margin - 2, margin + title_height), 
                   fill=dark_blue)
    
    # Draw some window content (representing files)
    content_y = margin + title_height + 4
    for i in range(3):
        y = content_y + i * 8
        if y < size[1] - margin - 4:
            draw.rectangle((margin + 6, y, size[0] - margin - 6, y + 4), 
                          fill=(200, 200, 200), outline=(150, 150, 150))
    
    # Draw a small "XP3" text if space allows
    if size[0] >= 64:
        try:
            # Try to load a font, fallback to default
            font = ImageFont.load_default()
            draw.text((margin + 4, size[1] - 16), "XP3", fill=black, font=font)
        except:
            # Fallback if font loading fails
            draw.text((margin + 4, size[1] - 16), "XP3", fill=black)
    
    return icon

def create_loading_icon(size=(32, 32)):
    """Create a small loading icon"""
    icon = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Create a spinning circle effect
    center = (size[0] // 2, size[1] // 2)
    radius = min(size) // 3
    
    # Draw spinning segments
    for i in range(8):
        angle_start = i * 45
        angle_end = angle_start + 30
        opacity = int(255 * (i + 1) / 8)
        color = (0, 100, 200, opacity)
        
        # Draw arc segments to simulate spinning
        for r in range(radius - 3, radius + 1):
            for angle in range(angle_start, angle_end, 2):
                import math
                x = center[0] + r * math.cos(math.radians(angle))
                y = center[1] + r * math.sin(math.radians(angle))
                if 0 <= x < size[0] and 0 <= y < size[1]:
                    draw.point((int(x), int(y)), fill=color)
    
    return icon

if __name__ == "__main__":
    # Create main application icon
    icon = create_xp_icon((64, 64))
    icon.save("xp3_icon.ico", format='ICO', sizes=[(64, 64), (32, 32), (16, 16)])
    icon.save("xp3_icon.png", format='PNG')
    
    # Create loading icon
    loading_icon = create_loading_icon((32, 32))
    loading_icon.save("loading_icon.png", format='PNG')
    
    print("Created xp3_icon.ico, xp3_icon.png, and loading_icon.png")
