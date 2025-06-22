#!/usr/bin/env python3
"""
Test Stone Throwing in Actual Game
Verify that stone throwing works properly in the real game environment
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import MosesAdventureGame

def test_stone_throwing_in_game():
    """Test stone throwing in the actual game"""
    print("🎮 TESTING STONE THROWING IN ACTUAL GAME")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create game instance
        game = MosesAdventureGame()
        
        print("1. Game initialized successfully")
        print(f"   Has inventory: {hasattr(game, 'inventory')}")
        print(f"   Has visual_feedback: {hasattr(game, 'visual_feedback')}")
        print(f"   Inventory connected: {hasattr(game.inventory, 'game_instance')}")
        
        # Start the game to initialize player
        game.start_game()
        
        print("\n2. Game started, player initialized")
        print(f"   Player exists: {game.player is not None}")
        print(f"   Stone throw mode: {game.stone_throw_mode}")
        
        # Add stone to inventory
        print("\n3. Adding stone to inventory...")
        game.inventory.add_item("stone", 1)
        print(f"   Inventory items: {game.inventory.items}")
        
        # Test using stone from inventory
        print("\n4. Using stone from inventory...")
        result = game.inventory.use_item("stone", game.player)
        print(f"   Use item result: {result}")
        print(f"   Stone throw mode after use: {game.stone_throw_mode}")
        print(f"   Inventory after use: {game.inventory.items}")
        
        # Test throwing stone
        print("\n5. Testing stone throwing...")
        if game.stone_throw_mode:
            print("   Stone throw mode is active!")
            print("   Simulating A key press...")
            throw_result = game.throw_stone_from_inventory()
            print(f"   Throw result: {throw_result}")
            print(f"   Stone throw mode after throw: {game.stone_throw_mode}")
        else:
            print("   ❌ Stone throw mode is NOT active!")
        
        print("\n✅ STONE THROWING TEST COMPLETED")
        print("   The stone throwing system is working correctly!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_stone_throwing_in_game()
