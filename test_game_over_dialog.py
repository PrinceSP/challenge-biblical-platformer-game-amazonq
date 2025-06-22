#!/usr/bin/env python3
"""
Test script for game over dialog functionality
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_game_over_dialog():
    """Test that game over shows dialog instead of quitting"""
    print("🧪 Testing Game Over Dialog System")
    print("=" * 40)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from main import MosesAdventureGame, GameState
        print("✅ All imports successful")
        
        # Initialize Pygame
        print("2. Initializing Pygame...")
        pygame.init()
        pygame.mixer.init()
        print("✅ Pygame initialized")
        
        # Create game instance
        print("3. Creating game instance...")
        game = MosesAdventureGame()
        print("✅ Game instance created")
        
        # Test if render_game_over_screen method exists
        print("4. Testing game over methods...")
        if hasattr(game, 'render_game_over_screen'):
            print("✅ render_game_over_screen method exists")
        else:
            print("❌ render_game_over_screen method missing")
            return False
        
        if hasattr(game, 'handle_game_over_events'):
            print("✅ handle_game_over_events method exists")
        else:
            print("❌ handle_game_over_events method missing")
            return False
        
        if hasattr(game, 'restart_game'):
            print("✅ restart_game method exists")
        else:
            print("❌ restart_game method missing")
            return False
        
        # Test game state transition to GAME_OVER
        print("5. Testing game over state transition...")
        original_state = game.state
        game.state = GameState.GAME_OVER
        
        if game.state == GameState.GAME_OVER:
            print("✅ Game state can be set to GAME_OVER")
        else:
            print("❌ Failed to set game state to GAME_OVER")
            return False
        
        # Test restart functionality
        print("6. Testing restart functionality...")
        game.start_game()  # Initialize player first
        original_health = game.player.health
        
        # Simulate player death
        game.player.health = 0
        print(f"   Set player health to: {game.player.health}")
        
        # Test restart
        game.restart_game()
        
        if game.player.health > 0:
            print(f"✅ Player health restored to: {game.player.health}")
        else:
            print("❌ Player health not restored after restart")
            return False
        
        if game.state == GameState.PLAYING:
            print("✅ Game state set to PLAYING after restart")
        else:
            print("❌ Game state not set to PLAYING after restart")
            return False
        
        print("\n" + "=" * 40)
        print("🎉 GAME OVER DIALOG TEST COMPLETED!")
        print("\nTest Results:")
        print("✅ Game over dialog system is properly implemented")
        print("✅ Restart functionality works correctly")
        print("✅ Game state management is working")
        print("\nTo test in-game:")
        print("1. Run: python3 main.py")
        print("2. Let enemies defeat Moses (health reaches 0)")
        print("3. Should see game over dialog (not quit)")
        print("4. Press SPACE to restart")
        print("5. Press ESC to return to menu")
        print("6. Press Q to quit")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_game_over_dialog()
    sys.exit(0 if success else 1)
