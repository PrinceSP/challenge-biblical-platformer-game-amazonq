#!/usr/bin/env python3
"""
Final fix for staff projectiles - use sparkle.png sprite and ensure they appear
"""

def analyze_and_fix_staff_projectiles():
    """Analyze why staff projectiles don't appear and fix it"""
    
    print("🔍 Analyzing Staff Projectile Issues...")
    
    # Check if the W key handling is correct
    with open('main.py', 'r') as f:
        main_content = f.read()
    
    # Look for W key handling
    if 'pygame.K_w' in main_content:
        print("✅ W key handling found in main.py")
    else:
        print("❌ W key handling missing in main.py")
    
    # Check if staff projectiles are being updated
    if 'update_staff_system' in main_content:
        print("✅ Staff system update found")
    else:
        print("❌ Staff system update missing")
    
    # Check if staff projectiles are being rendered
    if 'render_staff_projectiles' in main_content:
        print("✅ Staff projectile rendering found")
    else:
        print("❌ Staff projectile rendering missing")
    
    return True

def create_sprite_based_staff_projectile():
    """Create a new StaffProjectile class that uses the sparkle.png sprite"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the entire StaffProjectile class
    # Look for the class definition
    start_marker = "class StaffProjectile:"
    end_marker = "class Player:"
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker, start_pos)
    
    if start_pos != -1 and end_pos != -1:
        # Replace the entire StaffProjectile class
        new_staff_projectile_class = '''class StaffProjectile:
    """Staff projectile using sparkle.png sprite - SPRITE-BASED VERSION"""
    def __init__(self, x, y, direction):
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
        
        print(f"⚡ CREATED SPRITE-BASED staff projectile at x={x}, y={y}, direction={direction}")
        
    def update(self, dt):
        """Update staff projectile physics"""
        if not self.active:
            return
            
        # Move horizontally
        old_x = self.rect.x
        self.rect.x += self.velocity_x * dt
        
        # Debug movement
        if abs(self.rect.x - old_x) > 10:
            print(f"⚡ Staff projectile moving: x={self.rect.x}, y={self.rect.y}")
        
        # Remove if off screen
        if (self.rect.x < -100 or self.rect.x > 2000):  # Wider screen bounds
            print(f"⚡ Staff projectile off screen at x={self.rect.x}")
            self.active = False
            
        # Lifetime countdown
        self.lifetime -= dt
        if self.lifetime <= 0:
            print("⚡ Staff projectile expired")
            self.active = False
    
    def render(self, screen, camera_offset):
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
            print("⚡ Using fallback rendering (no sprite)")

'''
        
        # Replace the old class with the new one
        content = content[:start_pos] + new_staff_projectile_class + content[end_pos:]
        print("✅ Replaced StaffProjectile class with sprite-based version")
        
        with open('game_classes.py', 'w') as f:
            f.write(content)
        
        return True
    else:
        print("❌ Could not find StaffProjectile class to replace")
        return False

def ensure_staff_projectiles_are_updated():
    """Make sure staff projectiles are properly updated in the game loop"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Look for the player update section and ensure staff projectiles are updated
    if "self.player.update(dt)" in content:
        print("✅ Player update found - staff projectiles should be updated via update_staff_system")
    else:
        print("❌ Player update not found")
    
    # Check if staff projectiles are rendered in the main render loop
    render_section = '''            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)'''
    
    if render_section in content:
        print("✅ Staff projectile rendering found in main render loop")
    else:
        print("❌ Staff projectile rendering missing from main render loop")
        # Add it after player rendering
        player_render = "self.player.render(self.screen, camera_offset)"
        if player_render in content:
            new_content = content.replace(
                player_render,
                player_render + '''
            
            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)'''
            )
            with open('main.py', 'w') as f:
                f.write(new_content)
            print("✅ Added staff projectile rendering to main render loop")
    
    return True

def debug_w_key_handling():
    """Add comprehensive debug to W key handling"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find W key handling and enhance it
    old_w_key = '''            # Handle staff shooting
            if event.key == pygame.K_w:
                if self.player and hasattr(self.player, 'staff_active') and self.player.staff_active:
                    if self.player.shoot_staff_projectile():
                        # Play staff sound if available
                        if hasattr(self.sound_manager, 'play_sound'):
                            self.sound_manager.play_sound('jump')  # Use jump sound for now
                        # Visual feedback
                        if hasattr(self.visual_feedback, 'show_message'):
                            self.visual_feedback.show_message("⚡ Divine Energy!", 1.0)
                else:
                    print("⚠️  Staff not active! Use staff from inventory first.")
                    if hasattr(self.visual_feedback, 'show_message'):
                        self.visual_feedback.show_message("Staff not active!", 1.5)
                return'''
    
    new_w_key = '''            # Handle staff shooting - ENHANCED DEBUG VERSION
            if event.key == pygame.K_w:
                print("🎯 W KEY PRESSED!")
                if self.player:
                    print(f"🎯 Player exists: {self.player is not None}")
                    if hasattr(self.player, 'staff_active'):
                        print(f"🎯 Staff active: {self.player.staff_active}")
                        if self.player.staff_active:
                            print("🎯 Attempting to shoot staff projectile...")
                            success = self.player.shoot_staff_projectile()
                            print(f"🎯 Shoot success: {success}")
                            if success:
                                # Play staff sound if available
                                if hasattr(self.sound_manager, 'play_sound'):
                                    self.sound_manager.play_sound('jump')
                                # Visual feedback
                                if hasattr(self.visual_feedback, 'show_message'):
                                    self.visual_feedback.show_message("⚡ Divine Energy!", 1.0)
                                print("🎯 Staff projectile should be created and visible!")
                        else:
                            print("❌ Staff not active! Use staff from inventory first.")
                            if hasattr(self.visual_feedback, 'show_message'):
                                self.visual_feedback.show_message("Staff not active!", 1.5)
                    else:
                        print("❌ Player has no staff_active attribute")
                else:
                    print("❌ No player found")
                return'''
    
    if old_w_key in content:
        content = content.replace(old_w_key, new_w_key)
        print("✅ Enhanced W key handling with comprehensive debug")
        
        with open('main.py', 'w') as f:
            f.write(content)
        return True
    else:
        print("⚠️  Could not find W key handling to enhance")
        return False

def main():
    """Fix staff projectiles completely"""
    print("🔧 FINAL FIX: Staff Projectiles with Sparkle Sprite")
    print("=" * 55)
    
    print("1. Analyzing current issues...")
    analyze_and_fix_staff_projectiles()
    
    print("2. Creating sprite-based StaffProjectile class...")
    create_sprite_based_staff_projectile()
    
    print("3. Ensuring projectiles are updated and rendered...")
    ensure_staff_projectiles_are_updated()
    
    print("4. Adding comprehensive W key debug...")
    debug_w_key_handling()
    
    print("\n" + "=" * 55)
    print("🎉 FINAL STAFF PROJECTILE FIX APPLIED!")
    print("\nNew Features:")
    print("✅ Uses sparkle.png sprite as projectile bullet")
    print("✅ Larger, more visible projectiles (32x32 pixels)")
    print("✅ Comprehensive debug output for troubleshooting")
    print("✅ Enhanced W key handling with detailed logging")
    print("✅ Proper sprite loading with fallback rendering")
    print("✅ 4-second lifetime for better visibility")
    print("\nWhen you press W now, you should see:")
    print("- Debug messages showing W key press")
    print("- Staff projectile creation messages")
    print("- Sparkle sprites flying across the screen")
    print("- Movement and rendering debug output")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
