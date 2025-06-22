#!/usr/bin/env python3
"""
Replace sparkle sprite with diamond yellow shape for staff projectiles
"""

def create_diamond_staff_projectile():
    """Replace the sprite-based StaffProjectile with a diamond shape"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the entire StaffProjectile class
    start_marker = "class StaffProjectile:"
    end_marker = "class Player:"
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker, start_pos)
    
    if start_pos != -1 and end_pos != -1:
        # Create new diamond-based StaffProjectile class
        new_staff_projectile_class = '''class StaffProjectile:
    """Staff projectile using diamond yellow shape - SIMPLE AND RELIABLE"""
    def __init__(self, x, y, direction):
        import pygame  # Import pygame at the top
        
        self.rect = pygame.Rect(x, y, 16, 16)  # 16x16 diamond size
        self.velocity_x = direction * 450  # Fast movement
        self.velocity_y = 0  # Straight horizontal
        self.active = True
        self.lifetime = 3.0  # 3 seconds lifetime
        self.damage = 20  # 20 damage per hit
        self.direction = direction
        
        print(f"⚡ CREATED DIAMOND staff projectile at x={x}, y={y}, direction={direction}")
        
    def update(self, dt):
        """Update staff projectile physics"""
        if not self.active:
            return
            
        # Move horizontally
        old_x = self.rect.x
        self.rect.x += self.velocity_x * dt
        
        # Debug movement every 50 pixels
        if abs(self.rect.x - old_x) > 0 and int(self.rect.x) % 50 == 0:
            print(f"⚡ Diamond projectile moving: x={self.rect.x}, y={self.rect.y}")
        
        # Remove if off screen
        if (self.rect.x < -100 or self.rect.x > 2000):
            print(f"⚡ Diamond projectile off screen at x={self.rect.x}")
            self.active = False
            
        # Lifetime countdown
        self.lifetime -= dt
        if self.lifetime <= 0:
            print("⚡ Diamond projectile expired")
            self.active = False
    
    def render(self, screen, camera_offset):
        """Render the staff projectile as a bright yellow diamond"""
        import pygame  # Import pygame at the top
        
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Only render if on screen
        if render_x < -50 or render_x > 850:
            return
        
        print(f"⚡ RENDERING DIAMOND staff projectile at screen x={render_x}, y={render_y}")
        
        # Calculate diamond points (centered on the rect)
        center_x = render_x + 8  # Half of 16
        center_y = render_y + 8  # Half of 16
        
        # Diamond points (top, right, bottom, left)
        diamond_points = [
            (center_x, center_y - 8),      # Top point
            (center_x + 8, center_y),     # Right point  
            (center_x, center_y + 8),     # Bottom point
            (center_x - 8, center_y)      # Left point
        ]
        
        # Draw bright yellow diamond with glow effect
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
        pygame.draw.polygon(screen, (255, 215, 0), diamond_points, 2)  # Gold outline

'''
        
        # Replace the old class with the new one
        content = content[:start_pos] + new_staff_projectile_class + content[end_pos:]
        print("✅ Replaced StaffProjectile class with diamond shape version")
        
        with open('game_classes.py', 'w') as f:
            f.write(content)
        
        return True
    else:
        print("❌ Could not find StaffProjectile class to replace")
        return False

def main():
    """Replace sprite-based staff projectiles with diamond shapes"""
    print("🔧 Creating Diamond Yellow Staff Projectiles")
    print("=" * 45)
    
    if create_diamond_staff_projectile():
        print("\n✅ DIAMOND STAFF PROJECTILES CREATED!")
        print("\nNew Features:")
        print("✅ Bright yellow diamond shape projectiles")
        print("✅ No sprite dependencies - pure drawing")
        print("✅ 16x16 pixel diamond size")
        print("✅ White center with gold outline")
        print("✅ Glow effect around diamond")
        print("✅ 450 pixels/second speed")
        print("✅ 20 damage per hit")
        print("✅ 3-second lifetime")
        print("\nWhen you press W now:")
        print("- Bright yellow diamonds will fly across screen")
        print("- No sprite loading issues")
        print("- Highly visible and reliable")
        print("- Debug output shows diamond creation and movement")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Failed to create diamond staff projectiles")

if __name__ == "__main__":
    main()
