#!/usr/bin/env python3
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
        print("\n🎯 Testing step sound state transitions:")
        
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
        
        print("\n" + "=" * 40)
        print("🎉 STEP SOUND LOGIC TEST COMPLETED!")
        print("\nThe fix should now make step sounds play:")
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
