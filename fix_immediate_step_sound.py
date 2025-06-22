#!/usr/bin/env python3
"""
Fix for immediate step sound - should play as soon as left/right keys are pressed
"""

def fix_immediate_step_sound():
    """Fix the step sound to play immediately when keys are pressed"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the step sound logic
    old_sound_logic = '''        # FIXED: Immediate step sound system
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
    
    new_sound_logic = '''        # FIXED: Immediate step sound system - plays instantly on key press
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            # Initialize previous walking state if not exists
            if not hasattr(self, '_was_walking_last_frame'):
                self._was_walking_last_frame = False
            
            # Check if we just started walking (transition from not walking to walking)
            if self.is_walking and not self._was_walking_last_frame:
                # Just started walking - play step sound immediately
                self.sound_manager.play_single_step()
                self.step_timer = 0
                print("🚶 Started walking - immediate step sound")
            elif self.is_walking and self._was_walking_last_frame:
                # Continue walking - play step sounds at intervals
                self.step_timer += dt
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0
            elif not self.is_walking and self._was_walking_last_frame:
                # Just stopped walking
                self.step_timer = 0
                print("🛑 Stopped walking")
            
            # Remember walking state for next frame
            self._was_walking_last_frame = self.is_walking'''
    
    if old_sound_logic in content:
        content = content.replace(old_sound_logic, new_sound_logic)
        print("✅ Fixed immediate step sound logic")
        
        with open('game_classes.py', 'w') as f:
            f.write(content)
        return True
    else:
        print("⚠️  Could not find step sound logic to replace")
        return False

def main():
    """Apply the immediate step sound fix"""
    print("🔧 Fixing Immediate Step Sound")
    print("=" * 35)
    
    if fix_immediate_step_sound():
        print("\n✅ Step sound fix applied successfully!")
        print("\nNow step sounds will play immediately when you:")
        print("- Press LEFT arrow key")
        print("- Press RIGHT arrow key") 
        print("- Start walking after stopping")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Failed to apply step sound fix")

if __name__ == "__main__":
    main()
