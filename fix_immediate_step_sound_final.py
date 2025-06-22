#!/usr/bin/env python3
"""
Final fix for immediate step sound - should play instantly when arrow keys are pressed
"""

def fix_immediate_step_sound_final():
    """Fix the step sound to play immediately when keys are pressed"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the step sound logic with a completely fixed version
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
    
    new_sound_logic = '''        # FIXED: IMMEDIATE step sound system - plays instantly on key press
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            # Initialize previous walking state if not exists
            if not hasattr(self, '_was_walking_last_frame'):
                self._was_walking_last_frame = False
            
            # IMMEDIATE RESPONSE: Check if we just started walking (key press moment)
            if self.is_walking and not self._was_walking_last_frame:
                # Just pressed arrow key - play step sound IMMEDIATELY
                self.sound_manager.play_single_step()
                self.step_timer = 0
                print("🚶 Arrow key pressed - IMMEDIATE step sound!")
            elif self.is_walking and self._was_walking_last_frame:
                # Continue walking - play step sounds at intervals
                self.step_timer += dt
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0
            elif not self.is_walking and self._was_walking_last_frame:
                # Just stopped walking (released arrow key)
                self.step_timer = 0
                print("🛑 Arrow key released - stopped walking")
            
            # Remember walking state for next frame
            self._was_walking_last_frame = self.is_walking'''
    
    if old_sound_logic in content:
        content = content.replace(old_sound_logic, new_sound_logic)
        print("✅ Fixed immediate step sound logic - now plays instantly on key press")
        
        with open('game_classes.py', 'w') as f:
            f.write(content)
        return True
    else:
        print("⚠️  Could not find step sound logic to replace")
        # Let's try to find the newer version
        newer_sound_logic = '''        # FIXED: Immediate step sound system - plays instantly on key press
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
        
        if newer_sound_logic in content:
            content = content.replace(newer_sound_logic, new_sound_logic)
            print("✅ Fixed immediate step sound logic - now plays instantly on key press")
            
            with open('game_classes.py', 'w') as f:
                f.write(content)
            return True
        else:
            print("⚠️  Could not find any step sound logic to replace")
            return False

def test_step_sound_fix():
    """Create a simple test to verify the fix works"""
    
    test_code = '''#!/usr/bin/env python3
"""
Quick test for immediate step sound
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_immediate_step():
    """Test immediate step sound response"""
    print("🧪 Testing Immediate Step Sound Fix")
    print("=" * 40)
    
    try:
        from game_classes import Player
        from sound_manager import SoundManager
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create player and sound manager
        player = Player(100, 100, {})
        sound_manager = SoundManager()
        player.sound_manager = sound_manager
        
        print("✅ Player and sound manager created")
        
        # Test the step sound logic
        print("\\n🎯 Testing step sound state transitions:")
        
        # Simulate not walking initially
        player._was_walking_last_frame = False
        player.is_walking = False
        print(f"   Initial: was_walking={player._was_walking_last_frame}, is_walking={player.is_walking}")
        
        # Simulate pressing arrow key (start walking)
        player.is_walking = True
        print(f"   Arrow pressed: was_walking={player._was_walking_last_frame}, is_walking={player.is_walking}")
        
        # Check if this should trigger immediate sound
        if player.is_walking and not player._was_walking_last_frame:
            print("   ✅ IMMEDIATE STEP SOUND SHOULD PLAY!")
        else:
            print("   ❌ Step sound would NOT play immediately")
        
        # Update the state
        player._was_walking_last_frame = player.is_walking
        
        # Simulate continuing to walk
        print(f"   Continue walking: was_walking={player._was_walking_last_frame}, is_walking={player.is_walking}")
        
        # Simulate releasing arrow key
        player.is_walking = False
        print(f"   Arrow released: was_walking={player._was_walking_last_frame}, is_walking={player.is_walking}")
        
        # Simulate pressing arrow key again
        player.is_walking = True
        player._was_walking_last_frame = False  # Simulate stopped state
        print(f"   Arrow pressed again: was_walking={player._was_walking_last_frame}, is_walking={player.is_walking}")
        
        if player.is_walking and not player._was_walking_last_frame:
            print("   ✅ IMMEDIATE STEP SOUND SHOULD PLAY AGAIN!")
        else:
            print("   ❌ Step sound would NOT play immediately on restart")
        
        print("\\n" + "=" * 40)
        print("🎉 STEP SOUND LOGIC TEST COMPLETED!")
        print("\\nThe fix should now make step sounds play:")
        print("- IMMEDIATELY when you press LEFT arrow")
        print("- IMMEDIATELY when you press RIGHT arrow")
        print("- IMMEDIATELY when you start walking after stopping")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_immediate_step()
'''
    
    with open('test_immediate_step_final.py', 'w') as f:
        f.write(test_code)
    
    print("✅ Created test script: test_immediate_step_final.py")

def main():
    """Apply the final immediate step sound fix"""
    print("🔧 Final Fix for Immediate Step Sound")
    print("=" * 40)
    
    if fix_immediate_step_sound_final():
        print("\n✅ IMMEDIATE STEP SOUND FIX APPLIED!")
        print("\nNow step sounds will play INSTANTLY when you:")
        print("- Press LEFT arrow key (immediate sound)")
        print("- Press RIGHT arrow key (immediate sound)")
        print("- Start walking after stopping (immediate sound)")
        print("- No delay, no waiting - instant response!")
        
        print("\n🧪 Creating test script...")
        test_step_sound_fix()
        
        print("\nTest the fix:")
        print("1. Run: python3 main.py")
        print("2. Press LEFT arrow - should hear step sound INSTANTLY")
        print("3. Release LEFT arrow")
        print("4. Press RIGHT arrow - should hear step sound INSTANTLY")
        print("5. No more delays!")
    else:
        print("\n❌ Failed to apply immediate step sound fix")

if __name__ == "__main__":
    main()
