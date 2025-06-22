#!/usr/bin/env python3
"""
Standalone Enemy class
"""

import pygame
import random

# Game Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
RED = (220, 20, 60)
GREEN = (34, 139, 34)

class Enemy:
    def __init__(self, x, y, enemy_type, sprites):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.enemy_type = enemy_type
        self.health = 30
        self.max_health = 30
        self.speed = 1
        self.direction = 1  # 1 for right, -1 for left
        self.patrol_distance = 100
        self.start_x = x
        self.defeated = False
        
        # Load sprite
        self.sprite = None
        if sprites and 'enemies' in sprites:
            self.sprite = sprites['enemies'].get(enemy_type)
        
        if not self.sprite:
            # Create fallback sprite
            self.sprite = self.create_fallback_sprite()
        
        # Movement AI
        self.ai_timer = 0
        self.change_direction_time = 2.0  # Change direction every 2 seconds
    
    def create_fallback_sprite(self):
        """Create a fallback enemy sprite"""
        surface = pygame.Surface((32, 32))
        if self.enemy_type == "egyptian_soldier":
            surface.fill((220, 20, 60))  # Red
        elif self.enemy_type == "wild_animal":
            surface.fill((139, 69, 19))  # Brown
        else:
            surface.fill((128, 128, 128))  # Gray
        
        # Add simple enemy design
        pygame.draw.circle(surface, (0, 0, 0), (16, 16), 4)  # Eye
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)  # Border
        return surface
    
    def update(self, dt):
        """Update enemy AI and movement"""
        if self.defeated:
            return
        
        self.ai_timer += dt
        
        # Simple patrol AI
        if self.ai_timer >= self.change_direction_time:
            self.direction *= -1  # Change direction
            self.ai_timer = 0
        
        # Move horizontally
        self.rect.x += self.speed * self.direction
        
        # Keep within patrol area
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.direction *= -1
            self.rect.x = self.start_x + (self.patrol_distance * (-1 if self.rect.x < self.start_x else 1))
    
    def take_damage(self, damage):
        """Take damage from attacks"""
        self.health -= damage
        if self.health <= 0:
            self.defeated = True
            print(f"💀 {self.enemy_type} defeated!")
            return True
        else:
            print(f"⚔️ {self.enemy_type} took {damage} damage! Health: {self.health}/{self.max_health}")
            return False
    
    def render(self, screen, camera_offset):
        """Render the enemy"""
        if self.defeated:
            return
        
        render_rect = self.rect.copy()
        render_rect.x -= camera_offset[0]
        render_rect.y -= camera_offset[1]
        
        # Only render if on screen
        if (-50 <= render_rect.x <= SCREEN_WIDTH + 50 and 
            -50 <= render_rect.y <= SCREEN_HEIGHT + 50):
            
            if self.sprite:
                screen.blit(self.sprite, render_rect)
            
            # Health bar for enemies
            if self.health < self.max_health:
                bar_width = 30
                bar_height = 4
                bar_x = render_rect.x + 1
                bar_y = render_rect.y - 8
                
                # Background
                pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
                # Health
                health_width = int((self.health / self.max_health) * bar_width)
                pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
