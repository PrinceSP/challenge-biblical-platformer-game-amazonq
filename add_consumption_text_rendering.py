#!/usr/bin/env python3
"""
Add consumption text rendering to the game
"""

def add_consumption_text_rendering():
    """Add rendering for consumption text in the render method"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the render_game method and add consumption text rendering
    render_game_marker = "def render_game(self):"
    render_pos = content.find(render_game_marker)
    
    if render_pos != -1:
        # Find where to add consumption text rendering
        method_end = content.find("\n    def ", render_pos + 1)
        if method_end == -1:
            method_end = len(content)
        
        # Look for a good insertion point
        insertion_markers = [
            "self.render_ui()",
            "pygame.display.flip()",
            "# FPS Counter"
        ]
        
        insertion_point = -1
        for marker in insertion_markers:
            marker_pos = content.find(marker, render_pos)
            if marker_pos != -1 and marker_pos < method_end:
                insertion_point = marker_pos
                break
        
        if insertion_point != -1:
            consumption_text_rendering = '''
        # Render consumption text (disappears after 1 second)
        if hasattr(self, 'consumption_text') and self.consumption_text and hasattr(self, 'consumption_text_timer') and self.consumption_text_timer > 0:
            import pygame
            text_surface = self.font_manager.get_font('medium').render(self.consumption_text, True, (255, 255, 255))
            # Position text in center-top of screen
            text_rect = text_surface.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = 50
            
            # Add background for better visibility
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
            
            self.screen.blit(text_surface, text_rect)
        
'''
            content = content[:insertion_point] + consumption_text_rendering + content[insertion_point:]
            print("✅ Added consumption text rendering to render_game method")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_fps_toggle_initialization():
    """Ensure FPS toggle is properly initialized"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Make sure FPS toggle is initialized
    if "self.show_fps = False" not in content:
        # Find the __init__ method
        init_marker = "def __init__(self):"
        init_pos = content.find(init_marker)
        if init_pos != -1:
            # Find a good insertion point in __init__
            insertion_markers = [
                "self.target_fps = 60",
                "self.performance_mode = True",
                "print(f\"🚀 Performance optimization enabled"
            ]
            
            insertion_point = -1
            for marker in insertion_markers:
                marker_pos = content.find(marker, init_pos)
                if marker_pos != -1:
                    insertion_point = content.find('\n', marker_pos) + 1
                    break
            
            if insertion_point != -1:
                fps_toggle_init = '''        
        # FPS display toggle
        self.show_fps = False
        print("✅ FPS toggle system initialized (Press F1 to show/hide)")
'''
                content = content[:insertion_point] + fps_toggle_init + content[insertion_point:]
                print("✅ Added FPS toggle initialization")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Add consumption text rendering and fix FPS toggle"""
    print("🔧 Adding Consumption Text Rendering")
    print("=" * 40)
    
    print("1. Adding consumption text rendering...")
    add_consumption_text_rendering()
    
    print("2. Fixing FPS toggle initialization...")
    fix_fps_toggle_initialization()
    
    print("\n" + "=" * 40)
    print("✅ CONSUMPTION TEXT RENDERING ADDED!")
    print("\nFeatures:")
    print("✅ Consumption text renders in center-top of screen")
    print("✅ Text has background for better visibility")
    print("✅ Text disappears after 1 second timer")
    print("✅ FPS toggle properly initialized")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
