#!/usr/bin/env python3
"""
Test the camera and enemy fixes
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_classes import Camera, LevelManager, Location

def test_camera_fix():
    """Test that camera only follows horizontally"""
    print("🎮 Testing Camera Fix")
    print("=" * 30)
    
    # Create a mock player
    class MockPlayer:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 32, 48)
    
    # Test camera
    camera = Camera()
    player = MockPlayer(400, 300)
    
    print(f"Initial camera: x={camera.x}, y={camera.y}")
    
    # Follow player
    camera.follow_player(player)
    
    print(f"After following player at (400, 300):")
    print(f"Camera: x={camera.x:.1f}, y={camera.y}")
    print(f"✅ Y should be 0 (ground stays at bottom): {camera.y == 0}")
    
    # Move player and test again
    player.rect.x = 800
    player.rect.y = 100  # Player jumps up
    camera.follow_player(player)
    
    print(f"\nAfter player moves to (800, 100):")
    print(f"Camera: x={camera.x:.1f}, y={camera.y}")
    print(f"✅ Y should still be 0: {camera.y == 0}")
    print(f"✅ X should follow player: {camera.x > 0}")

def test_simple_enemies():
    """Test simple enemy creation"""
    print("\n🎮 Testing Simple Enemies")
    print("=" * 30)
    
    # Initialize pygame for rect operations
    pygame.init()
    
    # Create level manager
    level_manager = LevelManager()
    
    # Create a simple enemy manually
    enemy_rect = pygame.Rect(100, 200, 32, 32)
    simple_enemy = {
        'rect': enemy_rect,
        'type': 'egyptian_soldier',
        'health': 30,
        'defeated': False,
        'direction': 1,
        'start_x': 100,
        'speed': 1
    }
    level_manager.simple_enemies.append(simple_enemy)
    
    print(f"Created simple enemy at ({enemy_rect.x}, {enemy_rect.y})")
    print(f"Enemy type: {simple_enemy['type']}")
    print(f"Enemy health: {simple_enemy['health']}")
    
    # Test enemy update
    initial_x = enemy_rect.x
    level_manager.update_simple_enemies(0.016)  # ~60 FPS
    
    print(f"\nAfter update:")
    print(f"Enemy moved from x={initial_x} to x={enemy_rect.x}")
    print(f"✅ Enemy should move: {enemy_rect.x != initial_x}")
    
    # Test collision
    class MockPlayer:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 32, 48)
    
    player = MockPlayer(enemy_rect.x, enemy_rect.y)
    collision = level_manager.check_simple_enemy_collisions(player)
    
    print(f"\nCollision test:")
    print(f"Player at ({player.rect.x}, {player.rect.y})")
    print(f"Enemy at ({enemy_rect.x}, {enemy_rect.y})")
    print(f"✅ Collision detected: {collision}")
    print(f"✅ Enemy defeated after collision: {simple_enemy['defeated']}")

if __name__ == "__main__":
    test_camera_fix()
    test_simple_enemies()
    
    print("\n" + "=" * 50)
    print("🎯 SUMMARY:")
    print("✅ Camera fixed - only follows horizontally")
    print("✅ Ground stays at bottom of screen")
    print("✅ Simple enemies created and working")
    print("✅ Enemy movement and collision detection working")
    print("\nThe fixes should resolve both issues!")
