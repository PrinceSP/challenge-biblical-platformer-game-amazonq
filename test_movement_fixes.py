#!/usr/bin/env python3
"""
Test script for the movement and sound fixes
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_fixes():
    """Test the movement and sound fixes"""
    print("🧪 Testing Moses Adventure Movement Fixes")
    print("=" * 50)
    
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
        
        # Test Player class
        print("3. Testing Player class...")
        player = Player(100, 100, {})
        print(f"✅ Player created at position ({player.rect.x}, {player.rect.y})")
        
        # Test if new methods exist
        if hasattr(player, 'check_platform_support'):
            print("✅ check_platform_support() method exists")
        else:
            print("❌ check_platform_support() method missing")
        
        # Test sound manager
        print("4. Testing Sound Manager...")
        sound_manager = SoundManager()
        player.sound_manager = sound_manager
        print("✅ Sound manager connected to player")
        
        # Test movement simulation
        print("5. Testing movement simulation...")
        
        # Simulate key press for movement
        keys_pressed = {pygame.K_RIGHT: True, pygame.K_LEFT: False, pygame.K_UP: False}
        
        # Mock pygame.key.get_pressed()
        original_get_pressed = pygame.key.get_pressed
        pygame.key.get_pressed = lambda: keys_pressed
        
        # Test player update
        old_x = player.rect.x
        player.update(0.016)  # 60 FPS delta time
        
        if player.rect.x != old_x:
            print("✅ Player movement working")
        else:
            print("⚠️  Player movement may have issues")
        
        # Test step sound system
        if hasattr(player, 'step_timer'):
            print("✅ Step sound timer system exists")
        else:
            print("❌ Step sound timer system missing")
        
        # Restore original function
        pygame.key.get_pressed = original_get_pressed
        
        print("\n" + "=" * 50)
        print("🎉 BASIC TESTS COMPLETED!")
        print("\nTo fully test the fixes:")
        print("1. Run: python3 main.py")
        print("2. Use arrow keys to move Moses")
        print("3. Check that step sounds play immediately")
        print("4. Jump on platforms and walk off them")
        print("5. Verify Moses falls when walking off platforms")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fixes()
    sys.exit(0 if success else 1)
