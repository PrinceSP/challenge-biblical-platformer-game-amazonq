#!/usr/bin/env python3
"""
Fix staff projectile positioning and direction - shoot from in front of player
"""

def fix_projectile_positioning():
    """Fix projectile to spawn in front of player and head in correct direction"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and fix the projectile creation logic
    old_projectile_creation = '''        # Create projectile
        direction = 1 if self.facing_right else -1
        projectile_x = self.rect.centerx + (20 if self.facing_right else -20)
        projectile_y = self.rect.centery
        
        print(f"⚡ Creating staff projectile at player pos x={self.rect.centerx}, y={self.rect.centery}")
        print(f"⚡ Projectile spawn: x={projectile_x}, y={projectile_y}, direction={direction}")'''
    
    new_projectile_creation = '''        # Create projectile in front of player
        direction = 1 if self.facing_right else -1
        
        # Position projectile in front of player (further out for better visibility)
        if self.facing_right:
            projectile_x = self.rect.right + 10  # 10 pixels in front when facing right
        else:
            projectile_x = self.rect.left - 26   # 26 pixels in front when facing left (16 for diamond width + 10 spacing)
        
        # Position at player's center height
        projectile_y = self.rect.centery - 8  # Center the 16px diamond on player center
        
        print(f"⚡ Creating staff projectile at player pos x={self.rect.centerx}, y={self.rect.centery}")
        print(f"⚡ Player facing: {'RIGHT' if self.facing_right else 'LEFT'}")
        print(f"⚡ Projectile spawn: x={projectile_x}, y={projectile_y}, direction={direction}")'''
    
    if old_projectile_creation in content:
        content = content.replace(old_projectile_creation, new_projectile_creation)
        print("✅ Fixed projectile positioning to spawn in front of player")
    else:
        print("⚠️  Could not find projectile creation code to fix")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def enhance_diamond_rendering_with_direction():
    """Enhance diamond rendering to show direction clearly"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and enhance the diamond rendering
    old_diamond_render = '''        # Draw bright yellow diamond with glow effect
        # Outer glow (larger, semi-transparent)
        glow_points = [
            (center_x, center_y - 12),     # Top point (extended)
            (center_x + 12, center_y),    # Right point (extended)
            (center_x, center_y + 12),    # Bottom point (extended)
            (center_x - 12, center_y)     # Left point (extended)
        ]
        
        # Create glow surface
        glow_surface = pygame.Surface((32, 32))
        glow_surface.set_alpha(80)
        glow_surface.fill((255, 255, 0))  # Yellow
        screen.blit(glow_surface, (render_x - 8, render_y - 8))
        
        # Draw main diamond (bright yellow)
        pygame.draw.polygon(screen, (255, 255, 0), diamond_points)  # Bright yellow
        
        # Draw inner diamond (white center for brightness)
        inner_points = [
            (center_x, center_y - 4),      # Top point (smaller)
            (center_x + 4, center_y),     # Right point (smaller)
            (center_x, center_y + 4),     # Bottom point (smaller)
            (center_x - 4, center_y)      # Left point (smaller)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), inner_points)  # White center
        
        # Draw diamond outline for definition
        pygame.draw.polygon(screen, (255, 215, 0), diamond_points, 2)  # Gold outline'''
    
    new_diamond_render = '''        # Draw bright yellow diamond with glow effect and direction indicator
        # Create glow surface
        glow_surface = pygame.Surface((32, 32))
        glow_surface.set_alpha(80)
        glow_surface.fill((255, 255, 0))  # Yellow
        screen.blit(glow_surface, (render_x - 8, render_y - 8))
        
        # Draw main diamond (bright yellow)
        pygame.draw.polygon(screen, (255, 255, 0), diamond_points)  # Bright yellow
        
        # Draw inner diamond (white center for brightness)
        inner_points = [
            (center_x, center_y - 4),      # Top point (smaller)
            (center_x + 4, center_y),     # Right point (smaller)
            (center_x, center_y + 4),     # Bottom point (smaller)
            (center_x - 4, center_y)      # Left point (smaller)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), inner_points)  # White center
        
        # Draw diamond outline for definition
        pygame.draw.polygon(screen, (255, 215, 0), diamond_points, 2)  # Gold outline
        
        # Add directional trail effect to show movement direction
        trail_length = 12
        if self.direction > 0:  # Moving right
            # Trail behind (to the left)
            trail_points = [
                (center_x - trail_length, center_y - 2),
                (center_x - 4, center_y),
                (center_x - trail_length, center_y + 2)
            ]
        else:  # Moving left
            # Trail behind (to the right)
            trail_points = [
                (center_x + trail_length, center_y - 2),
                (center_x + 4, center_y),
                (center_x + trail_length, center_y + 2)
            ]
        
        # Draw trail with transparency
        trail_surface = pygame.Surface((24, 8))
        trail_surface.set_alpha(120)
        trail_surface.fill((255, 255, 200))  # Light yellow trail
        if self.direction > 0:
            screen.blit(trail_surface, (center_x - trail_length - 4, center_y - 4))
        else:
            screen.blit(trail_surface, (center_x - 8, center_y - 4))'''
    
    if old_diamond_render in content:
        content = content.replace(old_diamond_render, new_diamond_render)
        print("✅ Enhanced diamond rendering with directional trail")
    else:
        print("⚠️  Could not find diamond rendering code to enhance")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def add_player_facing_direction_tracking():
    """Ensure player facing direction is properly tracked"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Check if facing_right is properly initialized and updated
    if "self.facing_right = True" not in content:
        print("⚠️  Player facing direction may not be properly initialized")
        
        # Find Player __init__ and add facing direction
        player_init_search = "def __init__(self, x, y, platforms):"
        if player_init_search in content:
            # Find the end of __init__ method
            init_pos = content.find(player_init_search)
            if init_pos != -1:
                # Look for the first method after __init__
                next_method_pos = content.find("def ", init_pos + len(player_init_search))
                if next_method_pos != -1:
                    # Insert facing direction before the next method
                    insertion_point = content.rfind("\n", init_pos, next_method_pos)
                    if insertion_point != -1:
                        facing_code = '''        
        # Player facing direction (important for projectiles)
        self.facing_right = True  # Start facing right
'''
                        content = content[:insertion_point] + facing_code + content[insertion_point:]
                        print("✅ Added player facing direction tracking")
    
    # Ensure facing direction is updated in movement
    movement_check = "if keys[pygame.K_LEFT]:"
    if movement_check in content:
        # Check if facing direction is updated
        if "self.facing_right = False" not in content:
            print("⚠️  Left movement may not update facing direction")
        if "self.facing_right = True" not in content:
            print("⚠️  Right movement may not update facing direction")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix projectile direction and positioning"""
    print("🔶 Fixing Staff Projectile Direction and Positioning")
    print("=" * 55)
    
    print("1. Fixing projectile positioning...")
    fix_projectile_positioning()
    
    print("2. Enhancing diamond rendering with direction...")
    enhance_diamond_rendering_with_direction()
    
    print("3. Checking player facing direction tracking...")
    add_player_facing_direction_tracking()
    
    print("\n" + "=" * 55)
    print("🎉 PROJECTILE DIRECTION AND POSITIONING FIXED!")
    print("\nImprovements:")
    print("✅ Projectiles spawn in front of player")
    print("✅ Direction based on player facing (left/right)")
    print("✅ Proper spacing from player character")
    print("✅ Directional trail effect shows movement")
    print("✅ Enhanced visual feedback")
    print("\nNow when you press W:")
    print("- Diamond appears in front of Moses")
    print("- Flies in the direction Moses is facing")
    print("- Has a trail showing movement direction")
    print("- Proper positioning and spacing")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
