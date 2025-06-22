#!/usr/bin/env python3
"""
Test script for Moses Adventure new features
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_classes import *
from game_systems import *

def test_item_effects():
    """Test item effects system"""
    print("🧪 Testing Item Effects System...")
    
    # Create a mock player
    class MockPlayer:
        def __init__(self):
            self.health = 50
            self.max_health = 100
        
        def heal(self, amount):
            old_health = self.health
            self.health = min(self.max_health, self.health + amount)
            print(f"  Healed: {old_health} → {self.health}")
    
    player = MockPlayer()
    inventory = Inventory()
    
    # Add items to inventory
    inventory.add_item("meat", 2)
    inventory.add_item("bread", 3)
    inventory.add_item("water", 5)
    inventory.add_item("scroll", 1)
    inventory.add_item("stone", 2)
    
    print(f"  Initial health: {player.health}")
    
    # Test meat (should heal 10)
    print("  Testing meat...")
    inventory.use_item("meat", player)
    
    # Test bread (should heal 5)
    print("  Testing bread...")
    inventory.use_item("bread", player)
    
    # Test water (should heal 1)
    print("  Testing water...")
    inventory.use_item("water", player)
    
    # Test scroll (should not be consumed)
    print("  Testing scroll...")
    scroll_count_before = inventory.items.get("scroll", 0)
    inventory.use_item("scroll", player)
    scroll_count_after = inventory.items.get("scroll", 0)
    print(f"  Scroll count: {scroll_count_before} → {scroll_count_after} (should be same)")
    
    # Test stone
    print("  Testing stone...")
    stone_count_before = inventory.items.get("stone", 0)
    inventory.use_item("stone", player)
    stone_count_after = inventory.items.get("stone", 0)
    print(f"  Stone count: {stone_count_before} → {stone_count_after} (should decrease)")
    
    print(f"  Final health: {player.health}")
    print("✅ Item effects test completed!")

def test_enemy_system():
    """Test enemy system"""
    print("\n🧪 Testing Enemy System...")
    
    # Create enemies
    enemy1 = Enemy(100, 100, "egyptian_soldier", {})
    enemy2 = Enemy(200, 100, "wild_animal", {})
    
    print(f"  Enemy 1: {enemy1.enemy_type}, Health: {enemy1.health}")
    print(f"  Enemy 2: {enemy2.enemy_type}, Health: {enemy2.health}")
    
    # Test enemy movement
    print("  Testing enemy movement...")
    old_x1 = enemy1.rect.x
    enemy1.update(1.0)  # 1 second update
    new_x1 = enemy1.rect.x
    print(f"  Enemy 1 moved: {old_x1} → {new_x1}")
    
    # Test enemy damage
    print("  Testing enemy damage...")
    enemy1.take_damage(15)
    enemy1.take_damage(20)  # Should defeat the enemy
    
    print("✅ Enemy system test completed!")

def test_level_enemies():
    """Test that enemies are properly added to levels"""
    print("\n🧪 Testing Level Enemy Integration...")
    
    level_manager = LevelManager()
    level_manager.load_level(Location.PALACE, {'enemies': {}})
    
    enemies = level_manager.get_enemies()
    print(f"  Palace level has {len(enemies)} enemies")
    
    for i, enemy in enumerate(enemies):
        print(f"  Enemy {i+1}: {enemy.enemy_type} at ({enemy.rect.x}, {enemy.rect.y})")
    
    print("✅ Level enemy integration test completed!")

if __name__ == "__main__":
    pygame.init()
    
    print("🎮 Moses Adventure - Feature Testing")
    print("=" * 50)
    
    test_item_effects()
    test_enemy_system()
    test_level_enemies()
    
    print("\n🎉 All tests completed!")
    print("\nNew Features Summary:")
    print("✅ Item Effects:")
    print("   - Meat: +10 health")
    print("   - Bread: +5 health") 
    print("   - Water: +1 health")
    print("   - Scroll: Shows scripture (unlimited use)")
    print("   - Stone: Throw at enemies (single use)")
    print("✅ Moving Enemies:")
    print("   - Egyptian soldiers patrol areas")
    print("   - Wild animals move around")
    print("   - Enemies can be damaged by stones")
    print("   - Health bars show enemy status")
    print("✅ Enhanced Inventory:")
    print("   - Press 1-9 to use items")
    print("   - Item effects descriptions shown")
    print("   - Usage instructions displayed")
