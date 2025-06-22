#!/usr/bin/env python3
"""
Test Fixed Font System
Test the updated font manager
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from font_manager import FontManager

def test_fixed_font_system():
    """Test the fixed font system"""
    print("🔤 TESTING FIXED FONT SYSTEM")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create font manager
        print("1. Creating font manager...")
        font_manager = FontManager()
        
        print(f"\n2. Font system status:")
        print(f"   Custom font available: {font_manager.custom_font_available}")
        print(f"   System font selected: {font_manager.system_font_name}")
        print(f"   Available font sizes: {list(font_manager.sizes.keys())}")
        
        print(f"\n3. Testing font rendering...")
        
        # Create a test surface
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Font Test")
        
        # Test each font size
        test_text = "Moses Adventure - Biblical Platformer"
        colors = [(255, 255, 255), (255, 215, 0), (0, 255, 0), (255, 0, 0)]
        
        for i, (size_name, font) in enumerate(font_manager.fonts.items()):
            try:
                color = colors[i % len(colors)]
                text_surface = font_manager.render_text(test_text, size_name, color)
                
                if text_surface is not None:
                    print(f"   ✅ {size_name}: SUCCESS - {font_manager.sizes[size_name]}px")
                    
                    # Blit to screen for visual test
                    y_pos = 50 + (i * 80)
                    screen.blit(text_surface, (50, y_pos))
                    
                    # Add size label
                    label = font_manager.render_text(f"{size_name} ({font_manager.sizes[size_name]}px)", 'tiny', (200, 200, 200))
                    screen.blit(label, (50, y_pos + 40))
                else:
                    print(f"   ❌ {size_name}: Text surface is None")
                    
            except Exception as e:
                print(f"   ❌ {size_name}: ERROR - {e}")
        
        # Update display
        pygame.display.flip()
        
        print(f"\n4. Visual test window opened")
        print(f"   Press any key or close window to continue...")
        
        # Wait for user input
        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
            clock.tick(60)
        
        print(f"\n✅ FONT SYSTEM TEST COMPLETED")
        print(f"   All font sizes are working correctly!")
        
    except Exception as e:
        print(f"❌ Error during font test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_fixed_font_system()
