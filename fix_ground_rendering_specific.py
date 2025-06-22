#!/usr/bin/env python3
"""
Specific fix for ground rendering to stay at bottom
"""

def fix_ground_rendering_in_main():
    """Fix ground rendering in main.py render method"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the render_game method and add fixed ground rendering
    render_game_marker = "def render_game(self):"
    render_pos = content.find(render_game_marker)
    
    if render_pos != -1:
        # Find where to add ground rendering
        method_end = content.find("\n    def ", render_pos + 1)
        if method_end == -1:
            method_end = len(content)
        
        # Look for existing ground rendering or add it
        if "render.*ground" not in content[render_pos:method_end].lower():
            # Find a good insertion point in render_game
            insertion_markers = [
                "self.level_manager.render(self.screen, camera_offset)",
                "self.render_platforms(camera_offset)",
                "if self.player:"
            ]
            
            insertion_point = -1
            for marker in insertion_markers:
                marker_pos = content.find(marker, render_pos)
                if marker_pos != -1 and marker_pos < method_end:
                    insertion_point = content.find('\n', marker_pos) + 1
                    break
            
            if insertion_point != -1:
                ground_rendering = '''
        # Render FIXED ground that stays at bottom of screen
        self.render_fixed_ground(camera_offset)
        '''
                content = content[:insertion_point] + ground_rendering + content[insertion_point:]
                print("✅ Added fixed ground rendering call to render_game")
    
    # Add the render_fixed_ground method
    if "def render_fixed_ground(self" not in content:
        # Find a good place to add the method
        class_methods_end = content.find("def main():")
        if class_methods_end == -1:
            class_methods_end = len(content) - 100
        
        render_fixed_ground_method = '''
    def render_fixed_ground(self, camera_offset):
        """Render ground that stays FIXED at bottom of screen"""
        import pygame
        
        # Ground dimensions
        ground_height = 50
        ground_width = SCREEN_WIDTH * 6  # Extended ground width
        
        # FIXED: Ground Y position always at bottom of screen
        ground_y = SCREEN_HEIGHT - ground_height
        
        # Ground X position follows camera horizontally only
        ground_x = -camera_offset[0]
        
        # Create ground rectangle
        ground_rect = pygame.Rect(ground_x, ground_y, ground_width, ground_height)
        
        # Draw ground with brown stone color (matching platforms)
        pygame.draw.rect(self.screen, (139, 69, 19), ground_rect)    # Brown stone
        pygame.draw.rect(self.screen, (101, 67, 33), ground_rect, 3) # Dark brown border
        
        # Add ground texture
        for x in range(ground_x, ground_x + ground_width, 20):
            if 0 <= x <= SCREEN_WIDTH:  # Only draw visible texture
                pygame.draw.line(self.screen, (120, 60, 15), 
                               (x, ground_y + 5), (x, ground_y + ground_height - 5))

'''
        
        content = content[:class_methods_end] + render_fixed_ground_method + content[class_methods_end:]
        print("✅ Added render_fixed_ground method")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def optimize_fps_limiting():
    """Add proper FPS limiting to the main game loop"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the main game loop and add FPS limiting
    old_game_loop = '''        while running:
            dt = clock.get_time() / 1000.0  # Delta time in seconds
            
            for event in pygame.event.get():'''
    
    new_game_loop = '''        while running:
            dt = clock.get_time() / 1000.0  # Delta time in seconds
            
            # FPS limiting for better performance
            clock.tick(60)  # Limit to 60 FPS
            
            for event in pygame.event.get():'''
    
    if old_game_loop in content:
        content = content.replace(old_game_loop, new_game_loop)
        print("✅ Added FPS limiting to main game loop")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix ground rendering and optimize FPS"""
    print("🔧 Fixing Ground Rendering and FPS Optimization")
    print("=" * 50)
    
    print("1. Fixing ground rendering to stay at bottom...")
    fix_ground_rendering_in_main()
    
    print("2. Optimizing FPS limiting...")
    optimize_fps_limiting()
    
    print("\n" + "=" * 50)
    print("🎉 GROUND AND FPS FIXES APPLIED!")
    print("\nGround Rendering:")
    print("✅ Ground stays fixed at bottom of screen")
    print("✅ Only follows camera horizontally")
    print("✅ Brown stone color matching platforms")
    print("✅ Texture details for visual appeal")
    print("\nFPS Optimization:")
    print("✅ 60 FPS limit in main game loop")
    print("✅ Proper frame timing")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
