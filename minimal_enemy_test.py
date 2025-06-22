#!/usr/bin/env python3
"""
Minimal Enemy test
"""

import pygame
pygame.init()

# Define Enemy class directly here to test
class Enemy:
    def __init__(self, x, y, enemy_type, sprites):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.enemy_type = enemy_type
        self.health = 30
        self.max_health = 30
        self.speed = 1
        self.direction = 1
        self.patrol_distance = 100
        self.start_x = x
        self.defeated = False
        print(f"✅ Enemy created: {enemy_type} at ({x}, {y})")
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.defeated = True
            print(f"💀 {self.enemy_type} defeated!")
            return True
        else:
            print(f"⚔️ {self.enemy_type} took {damage} damage! Health: {self.health}/{self.max_health}")
            return False

# Test the Enemy class
print("Testing Enemy class...")
enemy = Enemy(100, 100, "egyptian_soldier", {})
enemy.take_damage(15)
enemy.take_damage(20)
print("✅ Enemy test completed!")
