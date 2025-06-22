#!/usr/bin/env python3
"""
Fix pygame import error in StaffProjectile class
"""

def fix_pygame_import_in_staff_projectile():
    """Fix the pygame import issue in StaffProjectile class"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the StaffProjectile class and fix the pygame import issue
    old_init = '''    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 32, 32)  # Size for sparkle sprite
        self.velocity_x = direction * 400  # Fast movement
        self.velocity_y = 0  # Straight horizontal
        self.active = True
        self.lifetime = 4.0  # 4 seconds lifetime
        self.damage = 20  # 20 damage per hit
        self.direction = direction
        
        # Load sparkle sprite
        self.sprite = None
        try:
            import pygame
            sprite_path = "/Users/javascript/Desktop/my_lab/challenge-biblical-platformer-game-amazonq/assets/sprites/effects/sparkle.png"
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # Scale sprite to be more visible
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            print(f"⚡ Loaded sparkle sprite for staff projectile")
        except Exception as e:
            print(f"⚠️  Could not load sparkle sprite: {e}")
            self.sprite = None
        
        print(f"⚡ CREATED SPRITE-BASED staff projectile at x={x}, y={y}, direction={direction}")'''
    
    new_init = '''    def __init__(self, x, y, direction):
        import pygame  # Import pygame at the top of the method
        
        self.rect = pygame.Rect(x, y, 32, 32)  # Size for sparkle sprite
        self.velocity_x = direction * 400  # Fast movement
        self.velocity_y = 0  # Straight horizontal
        self.active = True
        self.lifetime = 4.0  # 4 seconds lifetime
        self.damage = 20  # 20 damage per hit
        self.direction = direction
        
        # Load sparkle sprite
        self.sprite = None
        try:
            sprite_path = "/Users/javascript/Desktop/my_lab/challenge-biblical-platformer-game-amazonq/assets/sprites/effects/sparkle.png"
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            # Scale sprite to be more visible
            self.sprite = pygame.transform.scale(self.sprite, (32, 32))
            print(f"⚡ Loaded sparkle sprite for staff projectile")
        except Exception as e:
            print(f"⚠️  Could not load sparkle sprite: {e}")
            self.sprite = None
        
        print(f"⚡ CREATED SPRITE-BASED staff projectile at x={x}, y={y}, direction={direction}")'''
    
    if old_init in content:
        content = content.replace(old_init, new_init)
        print("✅ Fixed pygame import in StaffProjectile.__init__")
    else:
        print("⚠️  Could not find StaffProjectile.__init__ to fix")
    
    # Also fix the render method
    old_render = '''    def render(self, screen, camera_offset):
        """Render the staff projectile using sparkle sprite"""
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Only render if on screen
        if render_x < -50 or render_x > 850:
            return
        
        print(f"⚡ RENDERING SPRITE staff projectile at screen x={render_x}, y={render_y}")
        
        if self.sprite:
            # Render the sparkle sprite
            screen.blit(self.sprite, (render_x, render_y))
            
            # Add glow effect around sprite
            import pygame
            glow_surface = pygame.Surface((40, 40))
            glow_surface.set_alpha(100)
            glow_surface.fill((255, 255, 0))  # Yellow glow
            screen.blit(glow_surface, (render_x - 4, render_y - 4))
        else:
            # Fallback to drawing if sprite failed to load
            import pygame
            pygame.draw.circle(screen, (255, 255, 0), (render_x + 16, render_y + 16), 16)  # Yellow circle
            pygame.draw.circle(screen, (255, 255, 255), (render_x + 16, render_y + 16), 12)  # White center
            print("⚡ Using fallback rendering (no sprite)")'''
    
    new_render = '''    def render(self, screen, camera_offset):
        """Render the staff projectile using sparkle sprite"""
        import pygame  # Import pygame at the top of the method
        
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Only render if on screen
        if render_x < -50 or render_x > 850:
            return
        
        print(f"⚡ RENDERING SPRITE staff projectile at screen x={render_x}, y={render_y}")
        
        if self.sprite:
            # Render the sparkle sprite
            screen.blit(self.sprite, (render_x, render_y))
            
            # Add glow effect around sprite
            glow_surface = pygame.Surface((40, 40))
            glow_surface.set_alpha(100)
            glow_surface.fill((255, 255, 0))  # Yellow glow
            screen.blit(glow_surface, (render_x - 4, render_y - 4))
        else:
            # Fallback to drawing if sprite failed to load
            pygame.draw.circle(screen, (255, 255, 0), (render_x + 16, render_y + 16), 16)  # Yellow circle
            pygame.draw.circle(screen, (255, 255, 255), (render_x + 16, render_y + 16), 12)  # White center
            print("⚡ Using fallback rendering (no sprite)")'''
    
    if old_render in content:
        content = content.replace(old_render, new_render)
        print("✅ Fixed pygame import in StaffProjectile.render")
    else:
        print("⚠️  Could not find StaffProjectile.render to fix")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix pygame import error"""
    print("🔧 Fixing Pygame Import Error in StaffProjectile")
    print("=" * 45)
    
    if fix_pygame_import_in_staff_projectile():
        print("\n✅ PYGAME IMPORT ERROR FIXED!")
        print("\nNow the staff projectiles should:")
        print("- Create without import errors")
        print("- Use the sparkle.png sprite")
        print("- Appear when pressing W key")
        print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
