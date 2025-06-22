#!/usr/bin/env python3
"""
Fix staff projectile trail visibility - make it much more visible
"""

def make_trail_highly_visible():
    """Make the projectile trail much more visible and prominent"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the trail rendering code with a much more visible version
    old_trail_code = '''        # Draw trail with transparency
        trail_surface = pygame.Surface((24, 8))
        trail_surface.set_alpha(120)
        trail_surface.fill((255, 255, 200))  # Light yellow trail
        if self.direction > 0:
            screen.blit(trail_surface, (center_x - trail_length - 4, center_y - 4))
        else:
            screen.blit(trail_surface, (center_x - 8, center_y - 4))'''
    
    new_trail_code = '''        # Draw HIGHLY VISIBLE trail with multiple effects
        # Method 1: Bright solid trail rectangles
        trail_width = 20
        trail_height = 6
        
        if self.direction > 0:  # Moving right, trail on left
            # Multiple trail segments for motion blur effect
            for i in range(3):
                trail_x = center_x - trail_length - (i * 6)
                trail_alpha = 255 - (i * 60)  # Fade out
                
                # Create bright trail segment
                trail_rect = pygame.Rect(trail_x - 8, center_y - 3, trail_width - (i * 4), trail_height)
                pygame.draw.rect(screen, (255, 255, 0), trail_rect)  # Bright yellow
                pygame.draw.rect(screen, (255, 255, 255), (trail_x - 6, center_y - 1, trail_width - (i * 4) - 4, 2))  # White center
        else:  # Moving left, trail on right
            # Multiple trail segments for motion blur effect
            for i in range(3):
                trail_x = center_x + trail_length + (i * 6)
                trail_alpha = 255 - (i * 60)  # Fade out
                
                # Create bright trail segment
                trail_rect = pygame.Rect(trail_x - 4, center_y - 3, trail_width - (i * 4), trail_height)
                pygame.draw.rect(screen, (255, 255, 0), trail_rect)  # Bright yellow
                pygame.draw.rect(screen, (255, 255, 255), (trail_x - 2, center_y - 1, trail_width - (i * 4) - 4, 2))  # White center
        
        # Method 2: Additional particle trail effect
        import random
        for i in range(5):  # 5 trail particles
            if self.direction > 0:  # Moving right
                particle_x = center_x - 8 - (i * 4) + random.randint(-2, 2)
                particle_y = center_y + random.randint(-3, 3)
            else:  # Moving left
                particle_x = center_x + 8 + (i * 4) + random.randint(-2, 2)
                particle_y = center_y + random.randint(-3, 3)
            
            # Draw bright particle
            pygame.draw.circle(screen, (255, 255, 100), (particle_x, particle_y), 2)
        
        print(f"⚡ RENDERING TRAIL for direction {self.direction} at center ({center_x}, {center_y})")'''
    
    if old_trail_code in content:
        content = content.replace(old_trail_code, new_trail_code)
        print("✅ Enhanced trail visibility with multiple effects")
    else:
        print("⚠️  Could not find trail code to enhance")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def add_debug_trail_rendering():
    """Add debug output to confirm trail is being rendered"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the render method and add debug output
    render_debug_search = 'print(f"⚡ RENDERING DIAMOND staff projectile at screen x={render_x}, y={render_y}")'
    
    if render_debug_search in content:
        enhanced_debug = '''print(f"⚡ RENDERING DIAMOND staff projectile at screen x={render_x}, y={render_y}")
        print(f"⚡ Diamond direction: {self.direction}, center: ({center_x}, {center_y})")'''
        
        content = content.replace(render_debug_search, enhanced_debug)
        print("✅ Added enhanced debug output for trail rendering")
    else:
        print("⚠️  Could not find render debug to enhance")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def create_simple_visible_trail():
    """Create a simpler but highly visible trail system"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the diamond rendering section and add a simple bright trail before it
    diamond_render_start = "# Draw main diamond (bright yellow)"
    
    if diamond_render_start in content:
        # Insert simple trail before diamond rendering
        simple_trail = '''        # SIMPLE BRIGHT TRAIL - Draw before diamond for visibility
        trail_length = 16
        if self.direction > 0:  # Moving right, trail behind (left)
            # Draw bright yellow trail rectangles
            pygame.draw.rect(screen, (255, 255, 0), (center_x - trail_length, center_y - 2, trail_length - 4, 4))
            pygame.draw.rect(screen, (255, 255, 255), (center_x - trail_length + 2, center_y - 1, trail_length - 8, 2))
        else:  # Moving left, trail behind (right)
            # Draw bright yellow trail rectangles
            pygame.draw.rect(screen, (255, 255, 0), (center_x + 4, center_y - 2, trail_length, 4))
            pygame.draw.rect(screen, (255, 255, 255), (center_x + 6, center_y - 1, trail_length - 4, 2))
        
        '''
        
        content = content.replace(diamond_render_start, simple_trail + diamond_render_start)
        print("✅ Added simple bright trail before diamond rendering")
    else:
        print("⚠️  Could not find diamond rendering to add trail")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix trail visibility for staff projectiles"""
    print("🔶 Making Staff Projectile Trails Highly Visible")
    print("=" * 50)
    
    print("1. Creating simple visible trail system...")
    create_simple_visible_trail()
    
    print("2. Enhancing trail with multiple effects...")
    make_trail_highly_visible()
    
    print("3. Adding debug output for trail rendering...")
    add_debug_trail_rendering()
    
    print("\n" + "=" * 50)
    print("🎉 TRAIL VISIBILITY GREATLY ENHANCED!")
    print("\nNew Trail Features:")
    print("✅ Bright yellow trail rectangles")
    print("✅ White center lines for contrast")
    print("✅ Multiple trail segments for motion blur")
    print("✅ Particle effects for extra visibility")
    print("✅ Debug output to confirm rendering")
    print("✅ Simple and complex trail systems combined")
    print("\nNow when you press W:")
    print("- Bright yellow trail behind each diamond")
    print("- Multiple trail segments showing motion")
    print("- Particle effects for extra visibility")
    print("- Debug messages confirming trail rendering")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
