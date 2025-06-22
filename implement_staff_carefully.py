#!/usr/bin/env python3
"""
Carefully implement staff system without breaking existing code
"""

def add_staff_projectile_class():
    """Add StaffProjectile class after Stone class"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the end of Stone class
    stone_class_start = content.find("class Stone:")
    if stone_class_start != -1:
        # Find the next class after Stone
        next_class = content.find("class Player:", stone_class_start)
        if next_class != -1:
            # Insert StaffProjectile class before Player class
            staff_class = '''
class StaffProjectile:
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
        """Render the staff projectile"""
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Draw staff projectile as golden energy bolt
        pygame.draw.ellipse(screen, (255, 215, 0), (render_x, render_y, 12, 6))  # Gold
        pygame.draw.ellipse(screen, (255, 255, 255), (render_x + 2, render_y + 1, 8, 4))  # White center
        pygame.draw.ellipse(screen, (255, 215, 0), (render_x, render_y, 12, 6), 1)  # Gold outline

'''
            content = content[:next_class] + staff_class + content[next_class:]
            print("✅ Added StaffProjectile class")
            
            with open('game_classes.py', 'w') as f:
                f.write(content)
            return True
    
    print("⚠️  Could not find insertion point for StaffProjectile class")
    return False

def add_staff_attributes_to_player():
    """Add staff attributes to Player __init__"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the Player __init__ method and add staff attributes at the end
    init_method = content.find("def __init__(self, x, y, sprites):")
    if init_method != -1:
        # Find the end of __init__ method (look for next method definition)
        next_method_start = content.find("def ", init_method + 1)
        if next_method_start != -1:
            # Find the last line of __init__ before next method
            init_end = content.rfind("\n", init_method, next_method_start)
            
            staff_attributes = '''        
        # Staff system
        self.has_staff = False
        self.staff_active = False
        self.staff_duration = 120.0  # 2 minutes in seconds
        self.staff_timer = 0.0
        self.staff_cooldown = 0.0
        self.staff_cooldown_time = 0.3  # 0.3 seconds between staff shots
        self.staff_projectiles = []
'''
            
            content = content[:init_end] + staff_attributes + content[init_end:]
            print("✅ Added staff attributes to Player __init__")
            
            with open('game_classes.py', 'w') as f:
                f.write(content)
            return True
    
    print("⚠️  Could not find Player __init__ method")
    return False

def add_staff_methods_to_player():
    """Add staff methods to Player class"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the end of Player class (before next class)
    player_class_start = content.find("class Player:")
    if player_class_start != -1:
        # Find the next class after Player
        next_class = content.find("class ", player_class_start + 1)
        if next_class != -1:
            # Add staff methods before the next class
            staff_methods = '''
    def activate_staff(self):
        """Activate the staff buff"""
        self.has_staff = True
        self.staff_active = True
        self.staff_timer = self.staff_duration
        print("🪄 Moses' Staff activated! Press W to shoot divine projectiles!")
        print(f"⏰ Staff will last for {self.staff_duration/60:.1f} minutes")
    
    def deactivate_staff(self):
        """Deactivate the staff buff"""
        self.staff_active = False
        self.staff_timer = 0.0
        print("⏰ Moses' Staff power has expired")
    
    def shoot_staff_projectile(self):
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
        return True
    
    def update_staff_system(self, dt):
        """Update staff system timers and projectiles"""
        # Update staff duration
        if self.staff_active:
            self.staff_timer -= dt
            if self.staff_timer <= 0:
                self.deactivate_staff()
        
        # Update staff cooldown
        if self.staff_cooldown > 0:
            self.staff_cooldown -= dt
        
        # Update staff projectiles
        for projectile in self.staff_projectiles[:]:
            projectile.update(dt)
            if not projectile.active:
                self.staff_projectiles.remove(projectile)
    
    def render_staff_projectiles(self, screen, camera_offset):
        """Render all staff projectiles"""
        for projectile in self.staff_projectiles:
            projectile.render(screen, camera_offset)
    
    def get_staff_time_remaining(self):
        """Get remaining staff time in seconds"""
        return max(0, self.staff_timer) if self.staff_active else 0

'''
            content = content[:next_class] + staff_methods + content[next_class:]
            print("✅ Added staff methods to Player class")
            
            with open('game_classes.py', 'w') as f:
                f.write(content)
            return True
    
    print("⚠️  Could not find Player class end")
    return False

def update_player_update_method():
    """Add staff system update to Player.update method"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the end of Player.update method and add staff system update
    update_method_end = '''        # Keep player within reasonable bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH * 5:
            self.rect.right = SCREEN_WIDTH * 5'''
    
    update_with_staff = '''        # Keep player within reasonable bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH * 5:
            self.rect.right = SCREEN_WIDTH * 5
        
        # Update staff system
        if hasattr(self, 'update_staff_system'):
            self.update_staff_system(dt)'''
    
    if update_method_end in content:
        content = content.replace(update_method_end, update_with_staff)
        print("✅ Added staff system update to Player.update()")
        
        with open('game_classes.py', 'w') as f:
            f.write(content)
        return True
    
    print("⚠️  Could not find Player.update method end")
    return False

def main():
    """Carefully implement staff system"""
    print("🪄 Carefully Implementing Staff System")
    print("=" * 40)
    
    print("1. Adding StaffProjectile class...")
    if not add_staff_projectile_class():
        return
    
    print("2. Adding staff attributes to Player...")
    if not add_staff_attributes_to_player():
        return
    
    print("3. Adding staff methods to Player...")
    if not add_staff_methods_to_player():
        return
    
    print("4. Updating Player.update method...")
    if not update_player_update_method():
        return
    
    print("\n" + "=" * 40)
    print("🎉 STAFF SYSTEM CORE IMPLEMENTED!")
    print("\nNext steps:")
    print("- Run the previous fixes for movement and sound")
    print("- Add W key handling")
    print("- Update inventory system")
    print("- Test the complete system")

if __name__ == "__main__":
    main()
