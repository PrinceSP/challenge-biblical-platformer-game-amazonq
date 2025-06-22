#!/usr/bin/env python3
"""
Font Manager for Moses Adventure Game
Handles custom font loading with graceful fallback to system fonts
"""

import pygame
import os
from typing import Dict, Optional

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.custom_font_path = "fonts/Pixeled.ttf"
        self.custom_font_available = False
        self.system_font_name = None
        
        # Font size definitions
        self.sizes = {
            'tiny': 16,
            'small': 24,
            'medium': 32,
            'large': 48
        }
        
        # Try to load custom font, fallback to system fonts
        self.load_fonts()
    
    def load_fonts(self):
        """Load custom fonts with fallback to system fonts"""
        # First, try to load custom font if it exists
        if os.path.exists(self.custom_font_path):
            try:
                # Test loading the font
                test_font = pygame.font.Font(self.custom_font_path, 24)
                if test_font is not None:
                    # Test if we can actually render text with it
                    try:
                        test_surface = test_font.render("Test", True, (255, 255, 255))
                        if test_surface is not None:
                            self.custom_font_available = True
                            print(f"✅ Custom font loaded successfully: {self.custom_font_path}")
                        else:
                            raise pygame.error("Font cannot render text")
                    except Exception as render_error:
                        print(f"⚠️  Custom font cannot render text: {render_error}")
                        self.custom_font_available = False
                else:
                    raise pygame.error("Font loaded as None")
            except pygame.error as e:
                print(f"⚠️  Cannot load custom font: {e}")
                self.custom_font_available = False
        else:
            print(f"ℹ️  Custom font not found: {self.custom_font_path}")
            self.custom_font_available = False
        
        # Find best system font for pixel-style games
        if not self.custom_font_available:
            self.system_font_name = self.find_best_system_font()
        
        # Load all font sizes
        for size_name, size_value in self.sizes.items():
            try:
                if self.custom_font_available:
                    # Use custom font
                    font = pygame.font.Font(self.custom_font_path, size_value)
                    self.fonts[size_name] = font
                    print(f"✅ Loaded custom font for size '{size_name}': {size_value}px")
                else:
                    # Use system font
                    if self.system_font_name:
                        font = pygame.font.SysFont(self.system_font_name, size_value)
                        self.fonts[size_name] = font
                        print(f"✅ Using system font '{self.system_font_name}' for size '{size_name}': {size_value}px")
                    else:
                        # Fallback to default font
                        font = pygame.font.Font(None, size_value)
                        self.fonts[size_name] = font
                        print(f"✅ Using default font for size '{size_name}': {size_value}px")
                        
            except Exception as fallback_error:
                print(f"⚠️  Error loading font for size '{size_name}': {fallback_error}")
                # Ultimate fallback
                try:
                    fallback_font = pygame.font.Font(None, size_value)
                    self.fonts[size_name] = fallback_font
                    print(f"✅ Using fallback font for size '{size_name}': {size_value}px")
                except Exception as ultimate_error:
                    print(f"❌ Critical font error for size '{size_name}': {ultimate_error}")
    
    def find_best_system_font(self):
        """Find the best system font for pixel-style games"""
        try:
            available_fonts = pygame.font.get_fonts()
            
            # Preferred fonts for pixel-style games (monospace)
            preferred_fonts = [
                'courier', 'couriernew', 'monaco', 'consolas', 
                'lucidaconsole', 'dejavusansmono', 'liberationmono',
                'inconsolata', 'sourcecodepro', 'robotomono'
            ]
            
            # Find the first available preferred font
            for font_name in preferred_fonts:
                if font_name in available_fonts:
                    print(f"✅ Selected system font: {font_name}")
                    return font_name
            
            # If no preferred font found, use a common monospace font
            common_fonts = ['monospace', 'fixed', 'terminal']
            for font_name in common_fonts:
                if font_name in available_fonts:
                    print(f"✅ Selected fallback font: {font_name}")
                    return font_name
            
            print(f"ℹ️  Using default system font")
            return None
            
        except Exception as e:
            print(f"⚠️  Error finding system font: {e}")
            return None
    
    def get_font_info(self) -> dict:
        """Get information about the current font configuration"""
        return {
            'custom_font_available': self.custom_font_available,
            'custom_font_path': self.custom_font_path,
            'system_font_name': self.system_font_name,
            'loaded_sizes': list(self.fonts.keys()),
            'size_values': self.sizes
        }
    
    def get_font(self, size_name: str) -> pygame.font.Font:
        """Get font by size name"""
        if size_name in self.fonts:
            return self.fonts[size_name]
        else:
            # Return medium font as fallback
            return self.fonts.get('medium', pygame.font.Font(None, 24))
    
    def render_text(self, text: str, size_name: str, color: tuple, antialias: bool = True) -> pygame.Surface:
        """Render text with specified font size and color"""
        try:
            font = self.get_font(size_name)
            # For pixel fonts, disable antialiasing for crisp pixels
            if self.system_font_name in ['courier', 'monaco', 'consolas']:
                antialias = False
            return font.render(text, antialias, color)
        except Exception as e:
            print(f"⚠️  Error rendering text '{text}': {e}")
            # Fallback rendering
            try:
                fallback_font = pygame.font.Font(None, 24)
                return fallback_font.render(text, True, color)
            except Exception as fallback_error:
                print(f"❌ Critical text rendering error: {fallback_error}")
                return None

# Global font manager instance
_font_manager = None

def initialize_font_manager():
    """Initialize the global font manager"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager

def get_font_manager() -> FontManager:
    """Get the global font manager instance"""
    global _font_manager
    if _font_manager is None:
        _font_manager = FontManager()
    return _font_manager
