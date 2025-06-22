#!/usr/bin/env python3
"""
Add W key handling for staff shooting and visual staff sprite
"""

def add_w_key_staff_shooting():
    """Add W key handling for staff shooting"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the healing key handling and add W key after it
    healing_key = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return'''
    
    healing_and_staff_key = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return
            
            # Handle staff shooting
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
    
    if healing_key in content:
        content = content.replace(healing_key, healing_and_staff_key)
        print("✅ Added W key staff shooting")
    else:
        print("⚠️  Could not find healing key section to add W key")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_staff_visual_sprite():
    """Add visual staff sprite to player when staff is active"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the Player render method and enhance it
    # Look for the render method in Player class
    render_method_start = content.find("def render(self, screen, camera_offset):")
    if render_method_start != -1:
        # Find the end of the render method
        next_method = content.find("def ", render_method_start + 1)
        if next_method != -1:
            method_end = content.rfind("\n", render_method_start, next_method)
            
            # Add staff rendering code before the method ends
            staff_render_code = '''
        
        # Render staff if active
        if hasattr(self, 'staff_active') and self.staff_active:
            self.render_staff_sprite(screen, camera_offset)'''
            
            content = content[:method_end] + staff_render_code + content[method_end:]
            print("✅ Added staff sprite rendering to Player.render()")
    
    # Add the render_staff_sprite method to Player class
    staff_sprite_method = '''
    def render_staff_sprite(self, screen, camera_offset):
        """Render the staff sprite on the player"""
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Staff position based on facing direction
        if self.facing_right:
            staff_x = render_x + 25  # Right side of player
            staff_y = render_y + 10
        else:
            staff_x = render_x - 8   # Left side of player
            staff_y = render_y + 10
        
        # Draw staff as golden rod
        staff_color = (255, 215, 0)  # Gold
        staff_tip_color = (255, 255, 255)  # White
        
        # Staff body (vertical line)
        pygame.draw.line(screen, staff_color, 
                        (staff_x, staff_y), 
                        (staff_x, staff_y + 30), 3)
        
        # Staff tip (small circle)
        pygame.draw.circle(screen, staff_tip_color, 
                          (staff_x, staff_y), 4)
        pygame.draw.circle(screen, staff_color, 
                          (staff_x, staff_y), 4, 1)
        
        # Staff glow effect when active
        if hasattr(self, 'staff_timer') and self.staff_timer > 0:
            # Pulsing glow effect
            import math
            glow_alpha = int(50 + 30 * math.sin(pygame.time.get_ticks() * 0.01))
            glow_surface = pygame.Surface((16, 40))
            glow_surface.set_alpha(glow_alpha)
            glow_surface.fill(staff_color)
            screen.blit(glow_surface, (staff_x - 8, staff_y - 5))

'''
    
    # Find where to add the method (before the next class)
    player_class_end = content.find("class NPC:")
    if player_class_end == -1:
        player_class_end = content.find("class Enemy:")
    
    if player_class_end != -1:
        content = content[:player_class_end] + staff_sprite_method + content[player_class_end:]
        print("✅ Added render_staff_sprite method to Player class")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def update_controls_display():
    """Update the controls display to include W key for staff"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the controls display and add W key
    old_controls = '''        print("- H: Apply healing (after using healing items)")
        print("- A: Throw stone (when stone is ready)")'''
    
    new_controls = '''        print("- H: Apply healing (after using healing items)")
        print("- A: Throw stone (when stone is ready)")
        print("- W: Shoot staff projectile (when staff is active)")'''
    
    if old_controls in content:
        content = content.replace(old_controls, new_controls)
        print("✅ Updated controls display to include W key")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Add W key handling and visual staff sprite"""
    print("🪄 Adding Staff Controls and Visual Effects")
    print("=" * 45)
    
    print("1. Adding W key staff shooting...")
    add_w_key_staff_shooting()
    
    print("2. Adding visual staff sprite...")
    add_staff_visual_sprite()
    
    print("3. Updating controls display...")
    update_controls_display()
    
    print("\n" + "=" * 45)
    print("🎉 STAFF CONTROLS AND VISUALS ADDED!")
    print("\nNew Features:")
    print("✅ W key shoots staff projectiles")
    print("✅ Visual feedback for staff usage")
    print("✅ Staff sprite appears on player when active")
    print("✅ Glowing effect on active staff")
    print("✅ Updated controls display")
    print("\nTest the staff system:")
    print("1. Find and use a staff from inventory")
    print("2. Press W to shoot divine projectiles")
    print("3. Watch the golden staff appear on Moses")
    print("4. See the 2-minute timer countdown")

if __name__ == "__main__":
    main()
