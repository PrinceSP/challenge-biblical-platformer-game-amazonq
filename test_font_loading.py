#!/usr/bin/env python3
"""
Test Font Loading
Test if the custom font can be loaded properly
"""

import pygame
import os
import sys

def test_font_loading():
    """Test loading the custom font"""
    print("🔤 TESTING FONT LOADING")
    print("=" * 40)
    
    # Initialize pygame
    pygame.init()
    
    font_path = "fonts/Pixeled.ttf"
    
    print(f"1. Checking font file...")
    print(f"   Font path: {font_path}")
    print(f"   File exists: {os.path.exists(font_path)}")
    
    if os.path.exists(font_path):
        print(f"   File size: {os.path.getsize(font_path)} bytes")
        print(f"   File readable: {os.access(font_path, os.R_OK)}")
    
    print(f"\n2. Testing pygame font loading...")
    
    try:
        # Test loading the font with different sizes
        test_sizes = [16, 24, 32, 48]
        
        for size in test_sizes:
            print(f"   Testing size {size}px...")
            font = pygame.font.Font(font_path, size)
            
            if font is not None:
                print(f"   ✅ Size {size}px: SUCCESS")
                
                # Test rendering text
                try:
                    test_surface = font.render("Test", True, (255, 255, 255))
                    if test_surface is not None:
                        print(f"      Text rendering: SUCCESS")
                    else:
                        print(f"      Text rendering: FAILED")
                except Exception as render_error:
                    print(f"      Text rendering: ERROR - {render_error}")
            else:
                print(f"   ❌ Size {size}px: Font loaded as None")
                
    except pygame.error as e:
        print(f"   ❌ Pygame font error: {e}")
    except Exception as e:
        print(f"   ❌ General error: {e}")
    
    print(f"\n3. Testing default font fallback...")
    try:
        default_font = pygame.font.Font(None, 24)
        if default_font is not None:
            print(f"   ✅ Default font: SUCCESS")
        else:
            print(f"   ❌ Default font: FAILED")
    except Exception as e:
        print(f"   ❌ Default font error: {e}")
    
    print(f"\n4. System font information...")
    try:
        print(f"   Available system fonts: {len(pygame.font.get_fonts())}")
        print(f"   Default font: {pygame.font.get_default_font()}")
    except Exception as e:
        print(f"   ❌ System font info error: {e}")
    
    pygame.quit()

if __name__ == "__main__":
    test_font_loading()
