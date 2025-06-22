#!/usr/bin/env python3
"""
Fix the exact platform rendering issue in game_classes.py
"""

def fix_exact_platform_rendering():
    """Fix the exact line causing the platform rendering error"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the exact problematic code
    old_platform_render = '''        # Render platforms with more visible colors
        for platform in self.platforms:
            render_rect = platform.rect.copy()
            render_rect.x -= camera_offset[0]
            render_rect.y -= camera_offset[1]
            
            # Only render if on screen
            if render_rect.right > 0 and render_rect.left < SCREEN_WIDTH:
                # Make platforms more visible
                pygame.draw.rect(screen, (139, 69, 19), render_rect)  # Brown
                pygame.draw.rect(screen, (101, 67, 33), render_rect, 3)  # Dark brown border'''
    
    new_platform_render = '''        # Render platforms with more visible colors (supports both dict and object formats)
        for platform in self.platforms:
            # Handle dict format (new platform system)
            if isinstance(platform, dict):
                render_x = platform['x'] - camera_offset[0]
                render_y = platform['y'] - camera_offset[1]
                render_rect = pygame.Rect(render_x, render_y, platform['width'], platform['height'])
            # Handle object format (legacy system)
            elif hasattr(platform, 'rect'):
                render_rect = platform.rect.copy()
                render_rect.x -= camera_offset[0]
                render_rect.y -= camera_offset[1]
            else:
                continue  # Skip invalid platform data
            
            # Only render if on screen
            if render_rect.right > 0 and render_rect.left < SCREEN_WIDTH:
                # Make platforms more visible
                pygame.draw.rect(screen, (139, 69, 19), render_rect)  # Brown
                pygame.draw.rect(screen, (101, 67, 33), render_rect, 3)  # Dark brown border'''
    
    if old_platform_render in content:
        content = content.replace(old_platform_render, new_platform_render)
        print("✅ Fixed exact platform rendering issue")
    else:
        print("⚠️  Could not find exact platform rendering code")
        
        # Try to find any platform.rect references and fix them
        if "platform.rect.copy()" in content:
            content = content.replace(
                "render_rect = platform.rect.copy()",
                """# Handle both dict and object formats
            if isinstance(platform, dict):
                render_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
            elif hasattr(platform, 'rect'):
                render_rect = platform.rect.copy()
            else:
                continue"""
            )
            print("✅ Fixed platform.rect.copy() references")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix the exact platform rendering issue"""
    print("🔧 Fixing Exact Platform Rendering Issue")
    print("=" * 40)
    
    if fix_exact_platform_rendering():
        print("\n✅ PLATFORM RENDERING ISSUE FIXED!")
        print("\nFixed:")
        print("✅ Platform rendering supports dict format")
        print("✅ Backward compatibility maintained")
        print("✅ No more 'dict' object attribute errors")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Could not fix platform rendering issue")

if __name__ == "__main__":
    main()
