#!/usr/bin/env python3
"""
Interactive test for game mechanics
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_classes import Player, Stone
from game_systems import Inventory

def test_game_mechanics():
    """Test the game mechanics interactively"""
    print("🎮 Testing Game Mechanics")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Mechanics Test")
    clock = pygame.time.Clock()
    
    try:
        # Create game objects
        player = Player(100, 500, {})
        inventory = Inventory()
        stones = []
        
        # Mock game instance
        class MockGame:
            def __init__(self):
                self.healing_ready = False
                self.healing_item = None
                self.healing_amount = 0
                self.stone_throw_mode = False
                self.visual_feedback = MockVisualFeedback()
                self.player = player
            
            def prepare_healing(self, item_name, heal_amount):
                self.healing_ready = True
                self.healing_item = item_name
                self.healing_amount = heal_amount
                print(f"💊 {item_name.title()} ready! Press H to heal +{heal_amount}")
            
            def apply_healing(self):
                if self.healing_ready and self.healing_amount > 0:
                    if self.player.health >= self.player.max_health:
                        print("💚 Already at full health!")
                        self.healing_ready = False
                        self.healing_item = None
                        self.healing_amount = 0
                        return True
                    
                    old_health = self.player.health
                    self.player.heal(self.healing_amount)
                    print(f"✅ Healed! {old_health} → {self.player.health}")
                    
                    self.healing_ready = False
                    self.healing_item = None
                    self.healing_amount = 0
                    return True
                else:
                    print("❌ No healing ready!")
                    return False
            
            def activate_stone_throw_mode(self):
                self.stone_throw_mode = True
                print("🎯 Stone ready! Press A to throw!")
            
            def throw_stone(self):
                if self.stone_throw_mode:
                    stone = Stone(self.player.rect.centerx + 20, self.player.rect.centery, 1)
                    stones.append(stone)
                    self.stone_throw_mode = False
                    print("🪨 Stone thrown!")
                    return True
                return False
        
        class MockVisualFeedback:
            def show_message(self, message, duration):
                print(f"💬 {message}")
        
        mock_game = MockGame()
        inventory.game_instance = mock_game
        
        # Add test items
        inventory.add_item("meat", 2)
        inventory.add_item("bread", 2)
        inventory.add_item("water", 3)
        inventory.add_item("stone", 3)
        
        # Damage player for testing
        player.take_damage(40)  # Health = 60
        
        print(f"\n🎮 Interactive Test Started!")
        print(f"Player Health: {player.health}/100")
        print(f"Inventory: {inventory.items}")
        print(f"\nControls:")
        print(f"1 = Use Meat (+10 health)")
        print(f"2 = Use Bread (+5 health)")
        print(f"3 = Use Water (+1 health)")
        print(f"4 = Use Stone (throw mode)")
        print(f"H = Apply Healing")
        print(f"A = Throw Stone")
        print(f"ESC = Quit")
        
        running = True
        font = pygame.font.Font(None, 36)
        
        while running:
            dt = clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_1:  # Meat
                        print(f"\n🥩 Using meat...")
                        inventory.use_item("meat", player)
                    
                    elif event.key == pygame.K_2:  # Bread
                        print(f"\n🍞 Using bread...")
                        inventory.use_item("bread", player)
                    
                    elif event.key == pygame.K_3:  # Water
                        print(f"\n💧 Using water...")
                        inventory.use_item("water", player)
                    
                    elif event.key == pygame.K_4:  # Stone
                        print(f"\n🪨 Using stone...")
                        inventory.use_item("stone", player)
                    
                    elif event.key == pygame.K_h:  # Apply healing
                        print(f"\n💊 Applying healing...")
                        mock_game.apply_healing()
                    
                    elif event.key == pygame.K_a:  # Throw stone
                        print(f"\n🎯 Throwing stone...")
                        mock_game.throw_stone()
            
            # Update
            player.update(dt)
            for stone in stones[:]:
                stone.update(dt)
                if not stone.active:
                    stones.remove(stone)
            
            # Render
            screen.fill((50, 50, 100))  # Dark blue background
            
            # Draw player
            pygame.draw.rect(screen, (255, 255, 0), player.rect)  # Yellow player
            
            # Draw stones
            for stone in stones:
                pygame.draw.circle(screen, (128, 128, 128), stone.rect.center, 4)
            
            # Draw UI
            health_text = font.render(f"Health: {player.health}/100", True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            
            inventory_text = font.render(f"Inventory: {inventory.items}", True, (255, 255, 255))
            screen.blit(inventory_text, (10, 50))
            
            if mock_game.healing_ready:
                healing_text = font.render(f"HEALING READY! Press H (+{mock_game.healing_amount})", True, (0, 255, 0))
                screen.blit(healing_text, (10, 90))
            
            if mock_game.stone_throw_mode:
                stone_text = font.render("STONE READY! Press A to throw", True, (255, 255, 0))
                screen.blit(stone_text, (10, 130))
            
            controls_text = font.render("1=Meat 2=Bread 3=Water 4=Stone H=Heal A=Throw ESC=Quit", True, (200, 200, 200))
            screen.blit(controls_text, (10, 550))
            
            pygame.display.flip()
        
        print(f"\n✅ Test Results:")
        print(f"Final Health: {player.health}/100")
        print(f"Final Inventory: {inventory.items}")
        print(f"Stones Thrown: {len([s for s in stones if not s.active])}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        pygame.quit()

if __name__ == "__main__":
    test_game_mechanics()
