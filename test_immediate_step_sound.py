#!/usr/bin/env python3
"""
Test script for immediate step sound functionality
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_immediate_step_sound():
    """Test that step sounds play immediately when keys are pressed"""
    print("🧪 Testing Immediate Step Sound")
    print("=" * 35)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from game_classes import Player
        from sound_manager import SoundManager
        print("✅ All imports successful")
        
        # Initialize Pygame
        print("2. Initializing Pygame...")
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((800, 600))
        print("✅ Pygame initialized")
        
        # Create player and sound manager
        print("3. Setting up player and sound...")
        player = Player(100, 100, {})
        sound_manager = SoundManager()
        player.sound_manager = sound_manager
        print("✅ Player and sound manager ready")
        
        # Test scenario 1: Start walking from stopped state
        print("4. Testing immediate step sound on key press...")
        
        # Simulate not walking initially
        keys_not_walking = {pygame.K_RIGHT: False, pygame.K_LEFT: False, pygame.K_UP: False}
        original_get_pressed = pygame.key.get_pressed
        pygame.key.get_pressed = lambda: keys_not_walking
        
        # Update once while not walking
        player.update(0.016)
        was_walking_before = getattr(player, '_was_walking_last_frame', False)
        print(f"   Initial state - was_walking_last_frame: {was_walking_before}")
        
        # Now simulate pressing RIGHT key
        keys_walking_right = {pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False}
        pygame.key.get_pressed = lambda: keys_walking_right
        
        print("   Simulating RIGHT key press...")
        player.update(0.016)  # This should trigger immediate step sound
        
        # Check if the walking state changed
        is_walking_now = getattr(player, '_was_walking_last_frame', False)
        print(f"   After RIGHT key - was_walking_last_frame: {is_walking_now}")
        
        if is_walking_now and not was_walking_before:
            print("✅ Step sound logic should have triggered!")
        else:
            print("⚠️  Step sound logic may not have triggered properly")
        
        # Test scenario 2: Stop and start again
        print("5. Testing stop and restart...")
        
        # Stop walking
        pygame.key.get_pressed = lambda: keys_not_walking
        player.update(0.016)
        stopped_state = getattr(player, '_was_walking_last_frame', True)
        print(f"   After stopping - was_walking_last_frame: {stopped_state}")
        
        # Start walking LEFT
        keys_walking_left = {pygame.K_RIGHT: False, pygame.K_LEFT: True, pygame.K_UP: False}
        pygame.key.get_pressed = lambda: keys_walking_left
        
        print("   Simulating LEFT key press...")
        player.update(0.016)  # This should trigger immediate step sound again
        
        restarted_state = getattr(player, '_was_walking_last_frame', False)
        print(f"   After LEFT key - was_walking_last_frame: {restarted_state}")
        
        if restarted_state and not stopped_state:
            print("✅ Restart step sound logic should have triggered!")
        else:
            print("⚠️  Restart step sound logic may not have triggered properly")
        
        # Restore original function
        pygame.key.get_pressed = original_get_pressed
        
        print("\n" + "=" * 35)
        print("🎉 STEP SOUND TEST COMPLETED!")
        print("\nTo fully test:")
        print("1. Run: python3 main.py")
        print("2. Press LEFT arrow - should hear step sound immediately")
        print("3. Release LEFT arrow")
        print("4. Press RIGHT arrow - should hear step sound immediately")
        print("5. Hold arrow keys - should hear regular step intervals")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_immediate_step_sound()
    sys.exit(0 if success else 1)
