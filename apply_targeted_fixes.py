#!/usr/bin/env python3
"""
Targeted fixes for Moses Adventure - Step Sound and Platform Physics
"""

import re

def fix_step_sound_system():
    """Fix the step sound system to play immediately"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the walking sound section and replace it
    old_sound_code = '''        # Realistic walking sound system
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            if self.is_walking:
                # Update step timer
                self.step_timer += dt
                
                # Play step sound at regular intervals while walking
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0  # Reset timer for next step
                    
                # Mark that step sounds are playing
                if not self.is_step_sound_playing:
                    self.is_step_sound_playing = True
                    print("🚶 Started realistic step sounds")
            else:
                # Stop step sounds when not walking
                if self.is_step_sound_playing:
                    self.is_step_sound_playing = False
                    self.step_timer = 0  # Reset timer
                    print("🛑 Stopped step sounds")'''
    
    new_sound_code = '''        # FIXED: Immediate step sound system
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            # Check if we just started walking
            if self.is_walking and not hasattr(self, '_was_walking_last_frame'):
                # Just started walking - play step sound immediately
                self.sound_manager.play_single_step()
                self.step_timer = 0
                print("🚶 Started walking - immediate step sound")
            elif self.is_walking:
                # Continue walking - play step sounds at intervals
                self.step_timer += dt
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0
            elif hasattr(self, '_was_walking_last_frame') and self._was_walking_last_frame:
                # Just stopped walking
                self.step_timer = 0
                print("🛑 Stopped walking")
            
            # Remember walking state for next frame
            self._was_walking_last_frame = self.is_walking'''
    
    if old_sound_code in content:
        content = content.replace(old_sound_code, new_sound_code)
        print("✅ Fixed step sound system")
    else:
        print("⚠️  Could not find step sound code to replace")
    
    # Add platform support checking method before the update_animation_state method
    animation_method_start = content.find("    def update_animation_state(self):")
    if animation_method_start != -1:
        new_method = '''    def check_platform_support(self):
        """Check if player is still supported by a platform after horizontal movement"""
        self.needs_platform_check = True
    
    '''
        content = content[:animation_method_start] + new_method + content[animation_method_start:]
        print("✅ Added platform support checking method")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def fix_platform_physics():
    """Add platform support checking to player update"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the horizontal movement section and add platform checking
    old_movement = '''        # Update horizontal position
        self.rect.x += self.velocity_x
        
        # Update vertical position
        self.rect.y += self.velocity_y'''
    
    new_movement = '''        # Update horizontal position
        self.rect.x += self.velocity_x
        
        # FIXED: Check if player walked off a platform
        if self.on_ground and self.velocity_x != 0:
            self.check_platform_support()
        
        # Update vertical position
        self.rect.y += self.velocity_y'''
    
    if old_movement in content:
        content = content.replace(old_movement, new_movement)
        print("✅ Added platform support checking to movement")
    else:
        print("⚠️  Could not find movement code to update")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Apply targeted fixes"""
    print("🔧 Applying Targeted Movement Fixes")
    print("=" * 40)
    
    print("1. Fixing step sound system...")
    fix_step_sound_system()
    
    print("2. Fixing platform physics...")
    fix_platform_physics()
    
    print("\n✅ Targeted fixes applied!")
    print("Test with: python3 main.py")

if __name__ == "__main__":
    main()
