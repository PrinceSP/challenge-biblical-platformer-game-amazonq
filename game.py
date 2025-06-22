#!/usr/bin/env python3
"""
Moses Adventure - Biblical Platformer Game
A classic platformer-style adventure game featuring Moses' journey from Egypt to Jerusalem
"""

import pygame
import sys
import json
import os
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    DIALOGUE = "dialogue"
    INVENTORY = "inventory"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class Location(Enum):
    PALACE = "palace"
    EGYPT_CITY = "egypt_city"
    DESERT = "desert"
    RED_SEA = "red_sea"
    WILDERNESS = "wilderness"
    MOUNT_SINAI = "mount_sinai"
    JERUSALEM = "jerusalem"

@dataclass
class Item:
    name: str
    description: str
    sprite_path: str
    quantity: int = 1

@dataclass
class DialogueNode:
    speaker: str
    text: str
    choices: List[Tuple[str, str]] = None  # (choice_text, next_node_id)
    moral_impact: int = 0  # -1 to 1 scale

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moses Adventure - Biblical Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Game systems
        self.player = None
        self.camera = Camera()
        self.level_manager = LevelManager()
        self.inventory = Inventory()
        self.dialogue_system = DialogueSystem()
        self.sound_manager = SoundManager()
        self.moral_system = MoralSystem()
        self.visual_feedback = VisualFeedback()
        
        # Load sprites
        self.sprites = self.load_sprites()
        
        # Game state
        self.paused = False
        self.show_fps = False
        
    def load_sprites(self):
        """Load all game sprites"""
        sprites = {}
        
        # Load player sprites
        sprites['player'] = {}
        player_path = "assets/sprites/player/"
        if os.path.exists(player_path):
            sprites['player']['idle'] = self.load_sprite(f"{player_path}moses_idle.png")
            sprites['player']['jump'] = self.load_sprite(f"{player_path}moses_jump.png")
            sprites['player']['walk'] = []
            for i in range(4):
                walk_sprite = self.load_sprite(f"{player_path}moses_walk_{i}.png")
                if walk_sprite:
                    sprites['player']['walk'].append(walk_sprite)
        
        # Load NPC sprites
        sprites['npcs'] = {}
        npc_path = "assets/sprites/npcs/"
        npc_types = ['palace_guard', 'egyptian_citizen', 'hebrew_slave', 'priest']
        for npc_type in npc_types:
            sprites['npcs'][npc_type] = self.load_sprite(f"{npc_path}{npc_type}.png")
        
        # Load item sprites
        sprites['items'] = {}
        item_path = "assets/items/"
        item_types = ['stone', 'meat', 'water', 'armor_of_god', 'staff', 'bread', 'scroll']
        for item_type in item_types:
            sprites['items'][item_type] = self.load_sprite(f"{item_path}{item_type}.png")
        
        # Load UI sprites
        sprites['ui'] = {}
        ui_path = "assets/ui/"
        ui_elements = ['health_bar_bg', 'health_bar_fill', 'dialogue_box', 'inventory_slot', 'button']
        for ui_element in ui_elements:
            sprites['ui'][ui_element] = self.load_sprite(f"{ui_path}{ui_element}.png")
        
        # Load background sprites
        sprites['backgrounds'] = {}
        bg_path = "assets/backgrounds/"
        bg_types = ['palace', 'desert', 'red_sea']
        for bg_type in bg_types:
            sprites['backgrounds'][bg_type] = self.load_sprite(f"{bg_path}{bg_type}.png")
        
        return sprites
    
    def load_sprite(self, path):
        """Load a single sprite with error handling"""
        try:
            if os.path.exists(path):
                return pygame.image.load(path).convert_alpha()
            else:
                print(f"Warning: Sprite not found: {path}")
                return None
        except pygame.error as e:
            print(f"Error loading sprite {path}: {e}")
            return None
    
    def run(self):
        """Main game loop with 60 FPS optimization"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.render()
            
            # Optional FPS display
            if self.show_fps:
                fps = self.clock.get_fps()
                fps_text = pygame.font.Font(None, 24).render(f"FPS: {fps:.1f}", True, WHITE)
                self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
            
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.show_fps = not self.show_fps
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
            
            # State-specific events
            if self.state == GameState.MENU:
                self.handle_menu_events(event)
            elif self.state == GameState.PLAYING:
                self.handle_game_events(event)
            elif self.state == GameState.DIALOGUE:
                self.dialogue_system.handle_event(event)
                if not self.dialogue_system.active:
                    self.state = GameState.PLAYING
            elif self.state == GameState.INVENTORY:
                self.inventory.handle_event(event)
                if not self.inventory.active:
                    self.state = GameState.PLAYING
            elif self.state == GameState.PAUSED:
                self.handle_pause_events(event)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        pygame.display.toggle_fullscreen()
    
    def handle_menu_events(self, event):
        """Handle menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False
    
    def handle_game_events(self, event):
        """Handle gameplay events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.inventory.active = True
                self.state = GameState.INVENTORY
            elif event.key == pygame.K_ESCAPE:
                self.paused = True
                self.state = GameState.PAUSED
            elif event.key == pygame.K_m:
                self.sound_manager.toggle_music()
            elif event.key == pygame.K_s:
                self.sound_manager.toggle_sound()
    
    def handle_pause_events(self, event):
        """Handle pause menu events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                self.paused = False
                self.state = GameState.PLAYING
            elif event.key == pygame.K_q:
                self.state = GameState.MENU
                self.paused = False
    
    def start_game(self):
        """Initialize and start the game"""
        self.player = Player(100, 500, self.sprites.get('player', {}))
        self.level_manager.load_level(Location.PALACE, self.sprites)
        self.state = GameState.PLAYING
        self.sound_manager.play_background_music("palace")
        
        # Show opening dialogue
        self.dialogue_system.start_dialogue("opening")
        self.state = GameState.DIALOGUE
    
    def update(self, dt):
        """Update game state with delta time for smooth 60 FPS"""
        if self.state == GameState.PLAYING:
            if self.player:
                self.player.update(dt)
                self.camera.follow_player(self.player)
                self.check_collisions()
                self.check_interactions()
                self.check_level_transitions()
            
            self.level_manager.update(dt)
            self.visual_feedback.update(dt)
        
        elif self.state == GameState.DIALOGUE:
            self.dialogue_system.update(dt)
    
    def check_collisions(self):
        """Check for collisions with realistic physics effects"""
        if not self.player:
            return
        
        # Platform collisions with realistic physics
        platforms = self.level_manager.get_platforms()
        for platform in platforms:
            if self.player.rect.colliderect(platform.rect):
                self.handle_platform_collision(platform)
        
        # Item collisions
        items = self.level_manager.get_items()
        for item in items[:]:  # Use slice to avoid modification during iteration
            if self.player.rect.colliderect(item.rect):
                self.collect_item(item)
        
        # Enemy collisions
        enemies = self.level_manager.get_enemies()
        for enemy in enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.handle_enemy_collision(enemy)
    
    def handle_platform_collision(self, platform):
        """Handle collision with platforms with realistic physics"""
        player = self.player
        
        # Calculate overlap
        overlap_x = min(player.rect.right - platform.rect.left, 
                       platform.rect.right - player.rect.left)
        overlap_y = min(player.rect.bottom - platform.rect.top, 
                       platform.rect.bottom - player.rect.top)
        
        # Resolve collision based on smallest overlap
        if overlap_x < overlap_y:
            # Horizontal collision
            if player.rect.centerx < platform.rect.centerx:
                player.rect.right = platform.rect.left
            else:
                player.rect.left = platform.rect.right
            player.velocity_x = 0
        else:
            # Vertical collision
            if player.rect.centery < platform.rect.centery:
                # Landing on top
                player.rect.bottom = platform.rect.top
                player.velocity_y = 0
                player.on_ground = True
                # Create dust effect
                self.visual_feedback.create_dust_effect(player.rect.centerx, player.rect.bottom)
            else:
                # Hitting from below
                player.rect.top = platform.rect.bottom
                player.velocity_y = 0
    
    def collect_item(self, item):
        """Collect an item and add to inventory"""
        self.inventory.add_item(item.item_type)
        self.level_manager.remove_item(item)
        self.sound_manager.play_sound("item_collect")
        self.visual_feedback.show_item_collected(item.item_type, item.rect.center)
    
    def handle_enemy_collision(self, enemy):
        """Handle collision with enemies"""
        if self.player.velocity_y > 0 and self.player.rect.bottom <= enemy.rect.top + 10:
            # Player jumped on enemy
            enemy.defeated = True
            self.player.velocity_y = JUMP_STRENGTH // 2  # Small bounce
            self.sound_manager.play_sound("enemy_defeat")
            self.visual_feedback.create_sparkle_effect(enemy.rect.center)
        else:
            # Player takes damage
            self.player.take_damage(10)
            self.sound_manager.play_sound("player_hurt")
            self.visual_feedback.create_damage_effect(self.player.rect.center)
    
    def check_interactions(self):
        """Check for NPC interactions"""
        if not self.player:
            return
            
        npcs = self.level_manager.get_npcs()
        keys = pygame.key.get_pressed()
        
        for npc in npcs:
            if self.player.rect.colliderect(npc.interaction_rect):
                # Show interaction prompt
                self.visual_feedback.show_interaction_prompt(npc.rect.centerx, npc.rect.top - 20)
                
                if keys[pygame.K_e]:  # Interact key
                    self.start_dialogue(npc)
                    break
    
    def start_dialogue(self, npc):
        """Start dialogue with an NPC"""
        self.dialogue_system.start_dialogue(npc.dialogue_id)
        self.state = GameState.DIALOGUE
    
    def check_level_transitions(self):
        """Check if player should transition to next level"""
        if not self.player:
            return
            
        # Check if player reached the exit
        exit_zones = self.level_manager.get_exit_zones()
        for exit_zone in exit_zones:
            if self.player.rect.colliderect(exit_zone.rect):
                self.transition_to_level(exit_zone.destination)
    
    def transition_to_level(self, destination):
        """Transition to a new level"""
        self.level_manager.load_level(destination, self.sprites)
        self.sound_manager.play_background_music(destination.value)
        
        # Reset player position
        if self.player:
            self.player.rect.x = 100
            self.player.rect.y = 500
            self.player.velocity_x = 0
            self.player.velocity_y = 0
        
        # Show location text
        self.visual_feedback.show_location_text(destination.value.replace('_', ' ').title())
        
        # Check for victory condition
        if destination == Location.JERUSALEM:
            self.state = GameState.VICTORY
    
    def render(self):
        """Render the game with visual feedback"""
        self.screen.fill(BLACK)
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state in [GameState.PLAYING, GameState.DIALOGUE, GameState.INVENTORY, GameState.PAUSED]:
            self.render_game()
            
            if self.state == GameState.DIALOGUE:
                self.dialogue_system.render(self.screen)
            elif self.state == GameState.INVENTORY:
                self.inventory.render(self.screen, self.sprites.get('ui', {}))
            elif self.state == GameState.PAUSED:
                self.render_pause_menu()
        elif self.state == GameState.VICTORY:
            self.render_victory_screen()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over_screen()
        
        # Always render visual feedback on top
        self.visual_feedback.render(self.screen)
        
        pygame.display.flip()
    
    def render_menu(self):
        """Render the main menu"""
        # Background
        bg = self.sprites.get('backgrounds', {}).get('palace')
        if bg:
            # Darken the background
            dark_bg = bg.copy()
            dark_overlay = pygame.Surface(bg.get_size())
            dark_overlay.set_alpha(128)
            dark_overlay.fill(BLACK)
            dark_bg.blit(dark_overlay, (0, 0))
            
            # Scale to fit screen
            scaled_bg = pygame.transform.scale(dark_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        
        # Title
        title_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 36)
        instruction_font = pygame.font.Font(None, 24)
        
        title = title_font.render("Moses Adventure", True, GOLD)
        subtitle = subtitle_font.render("A Biblical Platformer Journey", True, WHITE)
        
        # Instructions
        instructions = [
            "Press SPACE or ENTER to Start",
            "Arrow Keys: Move",
            "E: Interact with NPCs",
            "I: Open Inventory",
            "M: Toggle Music",
            "S: Toggle Sound Effects",
            "ESC: Pause/Menu",
            "F1: Show FPS",
            "F11: Toggle Fullscreen"
        ]
        
        # Center title and subtitle
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Instructions
        y_offset = SCREEN_HEIGHT//2 - 20
        for instruction in instructions:
            text = instruction_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25
    
    def render_game(self):
        """Render the main game"""
        # Apply camera offset
        camera_offset = self.camera.get_offset()
        
        # Render background
        self.level_manager.render_background(self.screen, camera_offset)
        
        # Render level
        self.level_manager.render(self.screen, camera_offset)
        
        # Render player
        if self.player:
            self.player.render(self.screen, camera_offset)
        
        # Render UI
        self.render_ui()
    
    def render_ui(self):
        """Render UI elements"""
        font = pygame.font.Font(None, 24)
        
        if self.player:
            # Health bar
            health_bg_sprite = self.sprites.get('ui', {}).get('health_bar_bg')
            health_fill_sprite = self.sprites.get('ui', {}).get('health_bar_fill')
            
            if health_bg_sprite and health_fill_sprite:
                self.screen.blit(health_bg_sprite, (10, 10))
                
                # Scale health fill based on current health
                health_percent = self.player.health / self.player.max_health
                fill_width = int(health_fill_sprite.get_width() * health_percent)
                if fill_width > 0:
                    fill_rect = pygame.Rect(0, 0, fill_width, health_fill_sprite.get_height())
                    partial_fill = health_fill_sprite.subsurface(fill_rect)
                    self.screen.blit(partial_fill, (12, 12))
            
            # Health text
            health_text = font.render(f"Health: {self.player.health}/{self.player.max_health}", True, WHITE)
            self.screen.blit(health_text, (120, 15))
        
        # Current location
        location_text = font.render(f"Location: {self.level_manager.current_location.value.replace('_', ' ').title()}", True, WHITE)
        self.screen.blit(location_text, (10, 40))
        
        # Moral standing
        moral_standing = self.moral_system.get_moral_standing()
        moral_color = GREEN if moral_standing in ["Righteous", "Good"] else WHITE if moral_standing == "Neutral" else RED
        moral_text = font.render(f"Standing: {moral_standing}", True, moral_color)
        self.screen.blit(moral_text, (10, 65))
        
        # Instructions
        instruction_text = font.render("Arrow Keys: Move | E: Interact | I: Inventory | ESC: Pause", True, WHITE)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
        
        # Audio status
        audio_status = []
        if not self.sound_manager.music_enabled:
            audio_status.append("Music: OFF")
        if not self.sound_manager.sound_enabled:
            audio_status.append("Sound: OFF")
        
        if audio_status:
            audio_text = font.render(" | ".join(audio_status), True, RED)
            self.screen.blit(audio_text, (SCREEN_WIDTH - 200, 10))
    
    def render_pause_menu(self):
        """Render pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause menu
        font = pygame.font.Font(None, 48)
        small_font = pygame.font.Font(None, 24)
        
        pause_text = font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        instructions = [
            "ESC or SPACE: Resume",
            "Q: Return to Main Menu"
        ]
        
        y_offset = SCREEN_HEIGHT//2 + 20
        for instruction in instructions:
            text = small_font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def render_victory_screen(self):
        """Render victory screen"""
        # Background
        bg = self.sprites.get('backgrounds', {}).get('desert')  # Jerusalem background
        if bg:
            scaled_bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(scaled_bg, (0, 0))
        
        # Victory overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(64)
        overlay.fill(GOLD)
        self.screen.blit(overlay, (0, 0))
        
        # Victory text
        title_font = pygame.font.Font(None, 72)
        subtitle_font = pygame.font.Font(None, 36)
        
        victory_text = title_font.render("Victory!", True, GOLD)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(victory_text, victory_rect)
        
        completion_text = subtitle_font.render("Moses has reached the Promised Land!", True, WHITE)
        completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(completion_text, completion_rect)
        
        moral_text = subtitle_font.render(f"Final Standing: {self.moral_system.get_moral_standing()}", True, WHITE)
        moral_rect = moral_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(moral_text, moral_rect)
        
        restart_text = subtitle_font.render("Press SPACE to play again or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
        
        # Handle victory input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = GameState.MENU
        elif keys[pygame.K_ESCAPE]:
            self.running = False
    
    def render_game_over_screen(self):
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press SPACE to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
        
        # Handle game over input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = GameState.MENU
        elif keys[pygame.K_ESCAPE]:
            self.running = False

if __name__ == "__main__":
    # Create game instance and run
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Game crashed with error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
