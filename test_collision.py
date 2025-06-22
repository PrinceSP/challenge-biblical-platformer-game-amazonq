#!/usr/bin/env python3
"""
Test collision detection for Moses Adventure
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_classes import *

# Initialize Pygame
pygame.init()

# Test collision detection
def test_collision():
    print("Testing collision detection...")
    
    # Create a player at the expected position
    player = Player(150, 670, {})
    print(f"Player created at: x={player.rect.x}, y={player.rect.y}, bottom={player.rect.bottom}")
    print(f"Player on_ground: {player.on_ground}")
    
    # Create level manager and load palace level
    level_manager = LevelManager()
    level_manager.load_level(Location.PALACE, {})
    
    platforms = level_manager.get_platforms()
    print(f"Loaded {len(platforms)} platforms")
    
    for i, platform in enumerate(platforms):
        print(f"Platform {i}: x={platform.rect.x}, y={platform.rect.y}, width={platform.rect.width}, height={platform.rect.height}")
        print(f"  Platform top: {platform.rect.top}, bottom: {platform.rect.bottom}")
        
        # Check if player collides with this platform
        if player.rect.colliderect(platform.rect):
            print(f"  ✅ Player collides with platform {i}")
            
            # Check if player is on top
            if player.rect.bottom <= platform.rect.top + 5:
                print(f"  🏠 Player is ON TOP of platform {i}")
            else:
                print(f"  ⚠️  Player is INSIDE platform {i}")
        else:
            print(f"  ❌ No collision with platform {i}")
    
    # Test ground level
    ground_level = SCREEN_HEIGHT - 50  # 718
    print(f"\nGround level: {ground_level}")
    print(f"Player bottom: {player.rect.bottom}")
    print(f"Player should be on ground: {player.rect.bottom >= ground_level}")

if __name__ == "__main__":
    test_collision()
