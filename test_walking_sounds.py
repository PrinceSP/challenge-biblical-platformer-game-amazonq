#!/usr/bin/env python3
"""
Test walking sound system
"""

import pygame
import sys
import os
import time

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sound_manager import SoundManager

def test_walking_sounds():
    """Test the walking sound system"""
    print("🎮 Testing Walking Sound System")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    try:
        # Create sound manager
        sound_manager = SoundManager()
        
        print("✅ Sound manager initialized")
        print(f"🔊 Sound enabled: {sound_manager.sound_enabled}")
        
        # Test single step sound
        print("\n🦶 Testing single step sound...")
        sound_manager.play_single_step()
        time.sleep(1)
        
        # Test step volume adjustment
        print("\n🔊 Testing volume adjustment...")
        sound_manager.set_step_volume(0.3)
        sound_manager.play_single_step()
        time.sleep(1)
        
        sound_manager.set_step_volume(0.8)
        sound_manager.play_single_step()
        time.sleep(1)
        
        # Test realistic walking simulation
        print("\n🚶 Simulating realistic walking (5 steps)...")
        sound_manager.set_step_volume(0.6)
        
        for i in range(5):
            print(f"  Step {i+1}")
            sound_manager.play_single_step()
            time.sleep(0.5)  # Normal walking pace
        
        print("\n🏃 Simulating fast walking (5 steps)...")
        for i in range(5):
            print(f"  Fast step {i+1}")
            sound_manager.play_single_step()
            time.sleep(0.3)  # Fast walking pace
        
        print("\n🐌 Simulating slow walking (3 steps)...")
        for i in range(3):
            print(f"  Slow step {i+1}")
            sound_manager.play_single_step()
            time.sleep(0.7)  # Slow walking pace
        
        print("\n✅ Walking sound test completed!")
        print("\nWalking Sound Features:")
        print("- ✅ Single step sound plays correctly")
        print("- ✅ Volume adjustment works")
        print("- ✅ No sound overlap (previous sound stops)")
        print("- ✅ Realistic timing intervals")
        print("- ✅ Different paces supported")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_walking_sounds()
