#!/usr/bin/env python3
"""
Font Manager for Moses Adventure Game
Handles custom font loading with graceful fallback to default fonts
"""

import pygame
import os
from typing import Dict, Optional

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.custom_font_path = "fonts/Pixeled.ttf"
        self.custom_font_available = False
        
        # Font size definitions
        self.sizes = {
            'tiny': 16,
            'small': 24,
            'medium': 32,
            'large': 48
        }
        
        # Force disable custom font for now due to compatibility issues
        print("⚠️  Custom font disabled due to compatibility issues")
        self.custom_font_available = False
        self.load_fonts()
    
    def load_fonts(self):
        """Load custom fonts with fallback to default fonts"""
        # For now, skip custom font loading due to compatibility issues
        # Check if custom font exists
        if False and os.path.exists(self.custom_font_path):  # Disabled for now
            try:
                # Test loading the font
                test_font = pygame.font.Font(self.custom_font_path, 24)
                if test_font is not None:
                    self.custom_font_available = True
                    print(f"✅ Custom font loaded: {self.custom_font_path}")
                else:
                    raise pygame.error("Font loaded as None")
            except pygame.error as e:
                print(f"❌ Error loading custom font: {e}")
                self.custom_font_available = False
        else:
            if os.path.exists(self.custom_font_path):
                print(f"⚠️  Custom font found but disabled: {self.custom_font_path}")
            else:
                print(f"❌ Custom font not found: {self.custom_font_path}")
            self.custom_font_available = False
        
        # Load all font sizes using default fonts
        for size_name, size_value in self.sizes.items():
            try:
                # Always use default font for now
                fallback_font = pygame.font.Font(None, size_value)
                self.fonts[size_name] = fallback_font
                print(f"✅ Using default font for size '{size_name}': {size_value}px")
            except Exception as fallback_error:
                print(f"❌ Error loading fallback font for {size_name}: {fallback_error}")
                # Create a minimal font as last resort
                self.fonts[size_name] = pygame.font.Font(None, 24)
    
    def get_font(self, size: str = 'medium') -> pygame.font.Font:
        """Get font by size name"""
        try:
            if size in self.fonts and self.fonts[size] is not None:
                return self.fonts[size]
            else:
                print(f"❌ Font size '{size}' not found or None, using fallback")
                # Create fallback font
                fallback_size = self.sizes.get(size, 32)
                return pygame.font.Font(None, fallback_size)
        except Exception as e:
            print(f"Error getting font '{size}': {e}")
            return pygame.font.Font(None, 32)
    
    def get_font_by_size(self, pixel_size: int) -> pygame.font.Font:
        """Get font by exact pixel size"""
        if self.custom_font_available:
            try:
                return pygame.font.Font(self.custom_font_path, pixel_size)
            except pygame.error:
                return pygame.font.Font(None, pixel_size)
        else:
            return pygame.font.Font(None, pixel_size)
    
    def render_text(self, text: str, size: str = 'medium', color: tuple = (255, 255, 255), antialias: bool = True) -> pygame.Surface:
        """Render text with the specified font size"""
        try:
            font = self.get_font(size)
            if font is None:
                # Fallback to default font
                font = pygame.font.Font(None, self.sizes.get(size, 32))
            return font.render(str(text), antialias, color)
        except (pygame.error, TypeError) as e:
            print(f"Error rendering text '{text}' with size '{size}': {e}")
            # Emergency fallback
            try:
                fallback_font = pygame.font.Font(None, 24)
                return fallback_font.render(str(text), True, color)
            except:
                # Create empty surface as last resort
                surface = pygame.Surface((100, 20))
                surface.fill(color)
                return surface
    
    def get_text_size(self, text: str, size: str = 'medium') -> tuple:
        """Get the size of rendered text"""
        font = self.get_font(size)
        return font.size(text)
    
    def is_custom_font_available(self) -> bool:
        """Check if custom font is available"""
        return self.custom_font_available
    
    def get_font_info(self) -> dict:
        """Get information about loaded fonts"""
        return {
            'custom_font_available': self.custom_font_available,
            'custom_font_path': self.custom_font_path,
            'loaded_sizes': list(self.sizes.keys()),
            'size_values': self.sizes
        }

# Global font manager instance
font_manager = None

def initialize_font_manager():
    """Initialize the global font manager"""
    global font_manager
    if font_manager is None:
        font_manager = FontManager()
    return font_manager

def get_font_manager() -> FontManager:
    """Get the global font manager instance"""
    global font_manager
    if font_manager is None:
        font_manager = FontManager()
    return font_manager
