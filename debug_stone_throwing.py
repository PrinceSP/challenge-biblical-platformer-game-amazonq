#!/usr/bin/env python3
"""
Debug Stone Throwing System
Test the stone throwing functionality step by step
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_classes import Player
from game_systems import Inventory

def test_stone_throwing():
    """Test stone throwing system step by step"""
    print("🔧 DEBUGGING STONE THROWING SYSTEM")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    # Create mock game instance
    class MockGame:
        def __init__(self):
            self.stone_throw_mode = False
            self.player = Player(100, 500, {})
            
        def activate_stone_throw_mode(self):
            """Activate stone throwing mode"""
            self.stone_throw_mode = True
            print("🎯 STONE THROW MODE ACTIVATED!")
            print("🪨 Stone ready! Press A to throw or ESC to cancel.")
            
        def throw_stone_from_inventory(self):
            """Throw stone when in stone throw mode"""
            if self.stone_throw_mode:
                print("🪨 STONE THROWN SUCCESSFULLY!")
                self.stone_throw_mode = False
                return True
            else:
                print("❌ NOT IN STONE THROW MODE!")
                return False
    
    # Create game instance and inventory
    game = MockGame()
    inventory = Inventory()
    inventory.game_instance = game  # Connect inventory to game
    
    print("1. Testing inventory connection...")
    print(f"   Inventory has game_instance: {hasattr(inventory, 'game_instance')}")
    print(f"   Game instance exists: {inventory.game_instance is not None}")
    
    print("\n2. Adding stone to inventory...")
    inventory.add_item("stone", 1)
    print(f"   Inventory items: {inventory.items}")
    
    print("\n3. Testing stone usage from inventory...")
    print("   Simulating pressing number key 1...")
    
    # Simulate using stone from inventory
    if "stone" in inventory.items:
        print("   Stone found in inventory!")
        result = inventory.use_item("stone", game.player)
        print(f"   Use item result: {result}")
        print(f"   Stone throw mode after use: {game.stone_throw_mode}")
    else:
        print("   ❌ No stone in inventory!")
    
    print("\n4. Testing stone throwing...")
    if game.stone_throw_mode:
        print("   Stone throw mode is active - testing throw...")
        game.throw_stone_from_inventory()
    else:
        print("   ❌ Stone throw mode is NOT active!")
    
    print("\n5. Final state:")
    print(f"   Stone throw mode: {game.stone_throw_mode}")
    print(f"   Inventory items: {inventory.items}")
    
    pygame.quit()

if __name__ == "__main__":
    test_stone_throwing()
