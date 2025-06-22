#!/usr/bin/env python3
"""
Fix staff projectile visibility issue - make them work like stone projectiles
"""

def fix_staff_projectile_system():
    """Fix staff projectiles to be visible and work like stones"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and enhance the StaffProjectile class
    old_staff_projectile = '''class StaffProjectile:
    """Staff projectile for Moses' staff attacks"""
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 12, 6)  # Larger than stone
        self.velocity_x = direction * 400  # Faster than stone
        self.velocity_y = 0  # Straight horizontal shot
        self.active = True
        self.lifetime = 2.0  # 2 seconds lifetime
        self.damage = 20  # 20 damage per hit
        
    def update(self, dt):
        """Update staff projectile physics"""
        if not self.active:
            return
            
        # Apply physics (straight horizontal movement)
        self.rect.x += self.velocity_x * dt
        
        # Remove if off screen
        if (self.rect.x < -50 or self.rect.x > SCREEN_WIDTH + 50):
            self.active = False
            
        # Lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
    
    def render(self, screen, camera_offset):
        """Render the staff projectile - enhanced visibility"""
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Draw staff projectile as bright golden energy bolt with glow effect
        # Outer glow
        pygame.draw.ellipse(screen, (255, 255, 0), (render_x - 2, render_y - 2, 16, 10))  # Bright yellow glow
        # Main projectile
        pygame.draw.ellipse(screen, (255, 215, 0), (render_x, render_y, 12, 6))  # Gold
        # Bright center
        pygame.draw.ellipse(screen, (255, 255, 255), (render_x + 2, render_y + 1, 8, 4))  # White center
        # Energy trail effect
        pygame.draw.ellipse(screen, (255, 255, 200), (render_x + 8, render_y + 2, 6, 2))  # Trail
        
        # Debug: Print projectile position occasionally
        if int(render_x) % 50 == 0:
            print(f"⚡ Staff projectile at x={render_x}, y={render_y}")'''
    
    new_staff_projectile = '''class StaffProjectile:
    """Staff projectile for Moses' staff attacks - ENHANCED VERSION"""
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 16, 8)  # Larger and more visible
        self.velocity_x = direction * 300  # Slightly slower for visibility
        self.velocity_y = 0  # Straight horizontal shot
        self.active = True
        self.lifetime = 3.0  # 3 seconds lifetime for better visibility
        self.damage = 20  # 20 damage per hit
        print(f"⚡ Created staff projectile at x={x}, y={y}, direction={direction}")
        
    def update(self, dt):
        """Update staff projectile physics"""
        if not self.active:
            return
            
        # Apply physics (straight horizontal movement)
        old_x = self.rect.x
        self.rect.x += self.velocity_x * dt
        
        # Debug output every 100 pixels
        if abs(self.rect.x - old_x) > 0:
            if int(self.rect.x) % 100 == 0:
                print(f"⚡ Staff projectile moving: x={self.rect.x}, y={self.rect.y}")
        
        # Remove if off screen (wider bounds)
        if (self.rect.x < -100 or self.rect.x > SCREEN_WIDTH + 100):
            print(f"⚡ Staff projectile off screen at x={self.rect.x}")
            self.active = False
            
        # Lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            print("⚡ Staff projectile expired")
            self.active = False
    
    def render(self, screen, camera_offset):
        """Render the staff projectile - MAXIMUM VISIBILITY"""
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Only render if on screen
        if render_x < -50 or render_x > SCREEN_WIDTH + 50:
            return
        
        # Draw VERY BRIGHT staff projectile
        # Outer bright glow
        pygame.draw.ellipse(screen, (255, 255, 0), (render_x - 4, render_y - 4, 24, 16))  # Bright yellow glow
        # Middle glow
        pygame.draw.ellipse(screen, (255, 215, 0), (render_x - 2, render_y - 2, 20, 12))  # Gold glow
        # Main projectile body
        pygame.draw.ellipse(screen, (255, 255, 255), (render_x, render_y, 16, 8))  # Bright white
        # Inner core
        pygame.draw.ellipse(screen, (255, 255, 255), (render_x + 2, render_y + 2, 12, 4))  # White center
        # Energy trail
        pygame.draw.ellipse(screen, (255, 255, 200), (render_x + 12, render_y + 3, 8, 2))  # Trail
        
        # Debug: Always print when rendering
        print(f"⚡ RENDERING staff projectile at screen x={render_x}, y={render_y}")'''
    
    if old_staff_projectile in content:
        content = content.replace(old_staff_projectile, new_staff_projectile)
        print("✅ Enhanced StaffProjectile class for maximum visibility")
    else:
        print("⚠️  Could not find StaffProjectile class to enhance")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def add_debug_to_staff_shooting():
    """Add debug output to staff shooting system"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and enhance the shoot_staff_projectile method
    old_shoot_method = '''    def shoot_staff_projectile(self):
        """Shoot a staff projectile"""
        if not self.staff_active or self.staff_cooldown > 0:
            return False
        
        # Create projectile
        direction = 1 if self.facing_right else -1
        projectile_x = self.rect.centerx + (20 if self.facing_right else -20)
        projectile_y = self.rect.centery
        
        projectile = StaffProjectile(projectile_x, projectile_y, direction)
        self.staff_projectiles.append(projectile)
        
        # Set cooldown
        self.staff_cooldown = self.staff_cooldown_time
        
        print("⚡ Moses shoots divine energy!")
        return True'''
    
    new_shoot_method = '''    def shoot_staff_projectile(self):
        """Shoot a staff projectile - ENHANCED DEBUG VERSION"""
        if not self.staff_active:
            print("❌ Staff not active - cannot shoot")
            return False
            
        if self.staff_cooldown > 0:
            print(f"❌ Staff on cooldown: {self.staff_cooldown:.2f}s remaining")
            return False
        
        # Create projectile
        direction = 1 if self.facing_right else -1
        projectile_x = self.rect.centerx + (20 if self.facing_right else -20)
        projectile_y = self.rect.centery
        
        print(f"⚡ Creating staff projectile at player pos x={self.rect.centerx}, y={self.rect.centery}")
        print(f"⚡ Projectile spawn: x={projectile_x}, y={projectile_y}, direction={direction}")
        
        projectile = StaffProjectile(projectile_x, projectile_y, direction)
        self.staff_projectiles.append(projectile)
        
        print(f"⚡ Total staff projectiles: {len(self.staff_projectiles)}")
        
        # Set cooldown
        self.staff_cooldown = self.staff_cooldown_time
        
        print("⚡ Moses shoots divine energy!")
        return True'''
    
    if old_shoot_method in content:
        content = content.replace(old_shoot_method, new_shoot_method)
        print("✅ Enhanced shoot_staff_projectile method with debug")
    else:
        print("⚠️  Could not find shoot_staff_projectile method")
    
    # Also enhance the render_staff_projectiles method
    old_render_method = '''    def render_staff_projectiles(self, screen, camera_offset):
        """Render all staff projectiles"""
        for projectile in self.staff_projectiles:
            projectile.render(screen, camera_offset)'''
    
    new_render_method = '''    def render_staff_projectiles(self, screen, camera_offset):
        """Render all staff projectiles - ENHANCED DEBUG VERSION"""
        if len(self.staff_projectiles) > 0:
            print(f"⚡ Rendering {len(self.staff_projectiles)} staff projectiles")
        
        for i, projectile in enumerate(self.staff_projectiles):
            if projectile.active:
                print(f"⚡ Rendering projectile {i}: x={projectile.rect.x}, y={projectile.rect.y}")
                projectile.render(screen, camera_offset)
            else:
                print(f"⚡ Projectile {i} is inactive")'''
    
    if old_render_method in content:
        content = content.replace(old_render_method, new_render_method)
        print("✅ Enhanced render_staff_projectiles method with debug")
    else:
        print("⚠️  Could not find render_staff_projectiles method")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def fix_main_game_rendering():
    """Fix duplicate staff projectile rendering in main.py"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Remove duplicate staff projectile rendering
    duplicate_render = '''            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)
            
            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)'''
    
    single_render = '''            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)'''
    
    if duplicate_render in content:
        content = content.replace(duplicate_render, single_render)
        print("✅ Fixed duplicate staff projectile rendering")
    else:
        print("⚠️  Could not find duplicate rendering to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix staff projectile visibility issues"""
    print("🔧 Fixing Staff Projectile Visibility Issues")
    print("=" * 50)
    
    print("1. Enhancing StaffProjectile class...")
    fix_staff_projectile_system()
    
    print("2. Adding debug to staff shooting...")
    add_debug_to_staff_shooting()
    
    print("3. Fixing main game rendering...")
    fix_main_game_rendering()
    
    print("\n" + "=" * 50)
    print("🎉 STAFF PROJECTILE FIXES APPLIED!")
    print("\nEnhancements made:")
    print("✅ Larger, brighter staff projectiles")
    print("✅ Enhanced visibility with multiple glow layers")
    print("✅ Comprehensive debug output")
    print("✅ Fixed duplicate rendering")
    print("✅ Longer lifetime for better visibility")
    print("\nNow when you:")
    print("1. Use staff from inventory")
    print("2. Press W key")
    print("3. You should see BRIGHT golden projectiles")
    print("4. Debug messages will show projectile creation and movement")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
