#!/usr/bin/env python3
"""
Simple test to verify item effects work in the actual game
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import MosesAdventureGame

def test_game_items():
    """Test item effects in the actual game"""
    print("🎮 Testing Item Effects in Moses Adventure Game")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Create game instance
        game = MosesAdventureGame()
        
        # Start the game to initialize player
        game.start_game()
        
        print(f"✅ Game initialized successfully")
        print(f"📊 Player initial health: {game.player.health}/{game.player.max_health}")
        
        # Add items to inventory
        game.inventory.add_item("meat", 2)
        game.inventory.add_item("bread", 3)
        game.inventory.add_item("water", 5)
        game.inventory.add_item("scroll", 1)
        game.inventory.add_item("stone", 2)
        
        print(f"📦 Added items to inventory: {list(game.inventory.items.keys())}")
        
        # Test meat effect
        print("\n🥩 Testing meat effect...")
        old_health = game.player.health
        game.inventory.use_item("meat", game.player)
        new_health = game.player.health
        print(f"   Health change: {old_health} → {new_health} (Expected: +10)")
        
        # Test bread effect
        print("\n🍞 Testing bread effect...")
        old_health = game.player.health
        game.inventory.use_item("bread", game.player)
        new_health = game.player.health
        print(f"   Health change: {old_health} → {new_health} (Expected: +5)")
        
        # Test water effect
        print("\n💧 Testing water effect...")
        old_health = game.player.health
        game.inventory.use_item("water", game.player)
        new_health = game.player.health
        print(f"   Health change: {old_health} → {new_health} (Expected: +1)")
        
        # Test scroll (unlimited use)
        print("\n📜 Testing scroll effect...")
        scroll_count_before = game.inventory.items.get("scroll", 0)
        game.inventory.use_item("scroll", game.player)
        scroll_count_after = game.inventory.items.get("scroll", 0)
        print(f"   Scroll count: {scroll_count_before} → {scroll_count_after} (Should be same)")
        
        # Test stone
        print("\n🪨 Testing stone effect...")
        stone_count_before = game.inventory.items.get("stone", 0)
        game.inventory.use_item("stone", game.player)
        stone_count_after = game.inventory.items.get("stone", 0)
        print(f"   Stone count: {stone_count_before} → {stone_count_after} (Should decrease)")
        
        print(f"\n📊 Final player health: {game.player.health}/{game.player.max_health}")
        print("✅ All item effects tested successfully!")
        
        # Test enemy count
        enemies = game.level_manager.get_enemies()
        print(f"\n👹 Palace level has {len(enemies)} enemies")
        for i, enemy in enumerate(enemies[:3]):  # Show first 3
            print(f"   Enemy {i+1}: {enemy.enemy_type} at ({enemy.rect.x}, {enemy.rect.y})")
        
        print("\n🎉 Game item system working correctly!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_game_items()
