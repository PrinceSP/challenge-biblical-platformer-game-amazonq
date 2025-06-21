#!/usr/bin/env python3
"""
Moses Adventure - Biblical Platformer Game
Main launcher file

A classic platformer-style adventure game featuring Moses' journey from Egypt to Jerusalem
"""

import pygame
import sys
import os
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import game components
try:
    from game_classes import *
    from game_systems import *
    from font_manager import initialize_font_manager, get_font_manager
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all game files are in the same directory")
    sys.exit(1)

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

class MosesAdventureGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moses Adventure - Biblical Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        
        # Initialize font manager
        self.font_manager = initialize_font_manager()
        
        # Game systems
        self.player = None
        self.camera = Camera()
        self.level_manager = LevelManager()
        self.inventory = Inventory()
        self.dialogue_system = DialogueSystem()
        self.sound_manager = SoundManager()
        self.moral_system = MoralSystem()
        self.visual_feedback = VisualFeedback()
        
        # Connect moral system to dialogue system
        self.dialogue_system.moral_system = self.moral_system
        
        # Load sprites
        self.sprites = self.load_sprites()
        
        # Game state
        self.paused = False
        self.show_fps = False
        
        print("Moses Adventure initialized successfully!")
        print("Font System:")
        font_info = self.font_manager.get_font_info()
        if font_info['custom_font_available']:
            print(f"✅ Using custom Pixeled font from {font_info['custom_font_path']}")
        else:
            print("⚠️  Using default system fonts")
        print(f"Available sizes: {', '.join(font_info['loaded_sizes'])}")
        print()
        print("Controls:")
        print("- Arrow Keys: Move")
        print("- E: Interact with NPCs")
        print("- I: Open Inventory")
        print("- M: Toggle Music")
        print("- S: Toggle Sound Effects")
        print("- ESC: Pause/Menu")
        print("- F1: Show FPS")
        print("- F11: Toggle Fullscreen")
        
    def load_sprites(self):
        """Load all game sprites including NPCs for every location"""
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
        
        # Load NPC sprites for all locations
        sprites['npcs'] = {}
        npc_path = "assets/sprites/npcs/"
        
        # Base NPC types (actual sprite files)
        base_npc_types = ['palace_guard', 'egyptian_citizen', 'hebrew_slave', 'priest']
        for npc_type in base_npc_types:
            sprite = self.load_sprite(f"{npc_path}{npc_type}.png")
            if sprite:
                sprites['npcs'][npc_type] = sprite
            else:
                # Create fallback colored sprite
                sprites['npcs'][npc_type] = self.create_npc_fallback(npc_type)
        
        # Extended NPC types (using base sprites or fallbacks)
        npc_mappings = {
            # Palace NPCs
            'royal_servant': 'egyptian_citizen',
            'taskmaster': 'palace_guard',
            
            # Egypt City NPCs
            'merchant': 'egyptian_citizen',
            'scribe': 'priest',
            'noble': 'egyptian_citizen',
            'overseer': 'palace_guard',
            
            # Desert NPCs
            'bedouin': 'hebrew_slave',
            'nomad': 'hebrew_slave',
            'desert_guide': 'hebrew_slave',
            
            # Red Sea NPCs
            'fisherman': 'hebrew_slave',
            'boat_captain': 'egyptian_citizen',
            
            # Wilderness NPCs
            'elder': 'priest',
            'shepherd': 'hebrew_slave',
            'tribal_leader': 'priest',
            
            # Mount Sinai NPCs
            'prophet': 'priest',
            'mountain_guide': 'hebrew_slave',
            
            # Jerusalem NPCs
            'jerusalem_elder': 'priest',
            'temple_priest': 'priest',
            'city_guard': 'palace_guard'
        }
        
        # Map extended NPCs to base sprites or create unique fallbacks
        for extended_npc, base_npc in npc_mappings.items():
            if base_npc in sprites['npcs'] and sprites['npcs'][base_npc]:
                sprites['npcs'][extended_npc] = sprites['npcs'][base_npc]
            else:
                sprites['npcs'][extended_npc] = self.create_npc_fallback(extended_npc)
        
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
    
    def create_npc_fallback(self, npc_type):
        """Create a colored fallback sprite for NPCs with better visibility"""
        npc_surface = pygame.Surface((32, 48))
        npc_colors = {
            'palace_guard': (220, 20, 60),      # Red
            'hebrew_slave': (139, 69, 19),      # Brown
            'egyptian_citizen': (255, 255, 255), # White
            'priest': (255, 215, 0),            # Gold
            'royal_servant': (200, 200, 255),   # Light Blue
            'taskmaster': (180, 0, 0),          # Dark Red
            'merchant': (0, 100, 200),          # Blue
            'scribe': (150, 150, 0),            # Olive
            'noble': (128, 0, 128),             # Purple
            'overseer': (100, 0, 0),            # Maroon
            'bedouin': (160, 82, 45),           # Saddle Brown
            'nomad': (210, 180, 140),           # Tan
            'desert_guide': (244, 164, 96),     # Sandy Brown
            'fisherman': (70, 130, 180),        # Steel Blue
            'boat_captain': (25, 25, 112),      # Midnight Blue
            'elder': (184, 134, 11),            # Dark Goldenrod
            'shepherd': (107, 142, 35),         # Olive Drab
            'tribal_leader': (205, 133, 63),    # Peru
            'prophet': (255, 140, 0),           # Dark Orange
            'mountain_guide': (105, 105, 105),  # Dim Gray
            'jerusalem_elder': (218, 165, 32),  # Goldenrod
            'temple_priest': (255, 215, 0),     # Gold
            'city_guard': (178, 34, 34)         # Fire Brick
        }
        color = npc_colors.get(npc_type, (128, 128, 128))
        npc_surface.fill(color)
        
        # Add a simple character design
        pygame.draw.circle(npc_surface, (0, 0, 0), (16, 12), 4)  # Head
        pygame.draw.rect(npc_surface, (0, 0, 0), (12, 20, 8, 20))  # Body
        pygame.draw.rect(npc_surface, (0, 0, 0), (8, 25, 4, 15))   # Left arm
        pygame.draw.rect(npc_surface, (0, 0, 0), (20, 25, 4, 15))  # Right arm
        pygame.draw.rect(npc_surface, (0, 0, 0), (12, 35, 3, 10))  # Left leg
        pygame.draw.rect(npc_surface, (0, 0, 0), (17, 35, 3, 10))  # Right leg
        pygame.draw.rect(npc_surface, (0, 0, 0), npc_surface.get_rect(), 3)  # Border
        
        return npc_surface
    
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
        print("Starting Moses Adventure...")
        
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            if not self.paused:
                self.update(dt)
            self.render()
            
            # Optional FPS display
            if self.show_fps:
                fps = self.clock.get_fps()
                fps_text = self.font_manager.render_text(f"FPS: {fps:.1f}", 'small', WHITE)
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
            elif self.state == GameState.VICTORY:
                self.handle_victory_events(event)
            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events(event)
    
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
                self.player = None
    
    def handle_victory_events(self, event):
        """Handle victory screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = GameState.MENU
                self.player = None
            elif event.key == pygame.K_ESCAPE:
                self.running = False
    
    def handle_game_over_events(self, event):
        """Handle game over screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state = GameState.MENU
                self.player = None
            elif event.key == pygame.K_ESCAPE:
                self.running = False
    
    def start_game(self):
        """Initialize and start the game with opening dialogue"""
        # Place player properly on the ground
        self.player = Player(150, SCREEN_HEIGHT - 100, self.sprites.get('player', {}))
        
        # Debug: Show Moses' exact position
        print(f"🎯 Moses Position: x={self.player.rect.x}, y={self.player.rect.y}, bottom={self.player.rect.bottom}")
        
        # Connect sound manager to player for jump sounds
        if hasattr(self.player, 'set_sound_manager'):
            self.player.set_sound_manager(self.sound_manager)
        
        self.level_manager.load_level(Location.PALACE, self.sprites)
        
        # Reset camera to show the game world properly
        self.camera.x = 0
        self.camera.y = 0
        
        # Play ancient_egypt.mp3 background music
        self.sound_manager.play_background_music()
        
        # Reset game systems
        self.moral_system = MoralSystem()
        self.dialogue_system.moral_system = self.moral_system
        self.inventory = Inventory()
        self.visual_feedback = VisualFeedback()
        
        # START WITH OPENING DIALOGUE instead of going straight to playing
        self.state = GameState.DIALOGUE
        self.dialogue_system.start_dialogue("opening")
        
        print("Game started! Opening dialogue will begin...")
        print("Controls: Arrow keys to move, E to interact, M for music, S for sound")
    
    def update(self, dt):
        """Update game state with delta time for smooth 60 FPS"""
        if self.state == GameState.PLAYING:
            if self.player:
                self.player.update(dt)
                self.camera.follow_player(self.player)
                self.check_collisions()
                self.check_interactions()
                self.check_level_transitions()
                
                # Check for game over
                if self.player.health <= 0:
                    self.state = GameState.GAME_OVER
            
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
                player.is_jumping = False
                # Create dust effect
                self.visual_feedback.create_dust_effect(player.rect.centerx, player.rect.bottom)
                self.sound_manager.play_sound("jump")  # Landing sound
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
            if self.player.take_damage(10):
                self.state = GameState.GAME_OVER
            self.sound_manager.play_sound("player_hurt")
            self.visual_feedback.create_damage_effect(self.player.rect.center)
    
    def check_interactions(self):
        """Check for NPC interactions with proper feedback"""
        if not self.player:
            return
            
        npcs = self.level_manager.get_npcs()
        keys = pygame.key.get_pressed()
        
        interaction_found = False
        
        for npc in npcs:
            # Check if player is close enough to interact
            distance = abs(self.player.rect.centerx - npc.rect.centerx)
            if distance < 60:  # Interaction range
                interaction_found = True
                
                # Show interaction prompt
                self.visual_feedback.show_interaction_prompt(npc.rect.centerx, npc.rect.top - 20)
                
                if keys[pygame.K_e]:  # Interact key
                    # Start interaction animation
                    if hasattr(self.player, 'start_interaction'):
                        self.player.start_interaction()
                    
                    # Play dialogue sound if available
                    if hasattr(self.sound_manager, 'play_sound'):
                        self.sound_manager.play_sound('dialogue')
                    
                    # Start dialogue
                    print(f"🗣️  Interacting with {npc.npc_type}: {npc.dialogue_id}")
                    self.dialogue_system.start_dialogue(npc.dialogue_id)
                    self.state = GameState.DIALOGUE
                    break
        
        # Clear interaction prompt if no NPCs nearby
        if not interaction_found:
            self.visual_feedback.clear_interaction_prompt()
    
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
        
        # Reset player position for new level
        if self.player:
            self.player.rect.x = 100
            self.player.rect.y = SCREEN_HEIGHT - 100  # Position on ground level
            self.player.velocity_x = 0
            self.player.velocity_y = 0
            self.player.on_ground = True  # Make sure player starts on ground
        
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
        """Render the main menu with improved layout"""
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
        
        # Title section
        title_y = SCREEN_HEIGHT // 4
        
        # Title with improved spacing
        title = self.font_manager.render_text("Moses Adventure", 'large', GOLD)
        subtitle = self.font_manager.render_text("A Biblical Platformer Journey", 'medium', WHITE)
        
        # Center title and subtitle
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, title_y - 30))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, title_y + 20))
        
        self.screen.blit(title, title_rect)
        self.screen.blit(subtitle, subtitle_rect)
        
        # Start instruction
        start_text = self.font_manager.render_text("Press SPACE or ENTER to Start", 'medium', GOLD)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, title_y + 70))
        self.screen.blit(start_text, start_rect)
        
        # Controls section
        controls_y = SCREEN_HEIGHT // 2 + 50
        controls_title = self.font_manager.render_text("Controls", 'medium', GOLD)
        controls_title_rect = controls_title.get_rect(center=(SCREEN_WIDTH//2, controls_y))
        self.screen.blit(controls_title, controls_title_rect)
        
        # Control instructions
        controls = [
            "Arrow Keys: Move Moses",
            "E: Interact with NPCs",
            "I: Open Inventory",
            "ESC: Pause/Menu",
            "M: Toggle Music | S: Toggle Sound"
        ]
        
        y_offset = controls_y + 40
        for control in controls:
            text = self.font_manager.render_text(control, 'small', WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30
    
    def render_game(self):
        """Render the main game with proper background"""
        # Clear screen first
        self.screen.fill(BLACK)
        
        # Apply camera offset
        camera_offset = self.camera.get_offset()
        
        # Render background first (this should show the palace)
        self.level_manager.render_background(self.screen, camera_offset)
        
        # Render level elements (platforms, items, NPCs)
        self.level_manager.render(self.screen, camera_offset)
        
        # Render player on top
        if self.player:
            self.player.render(self.screen, camera_offset)
        
        # Render UI on top of everything
        self.render_ui()
    
    def render_ui(self):
        """Render UI elements with debug info"""
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
            health_text = self.font_manager.render_text(f"Health: {self.player.health}/{self.player.max_health}", 'small', WHITE)
            self.screen.blit(health_text, (120, 15))
            
            # Debug: Show player position and movement limits
            pos_text = self.font_manager.render_text(f"Moses: X={self.player.rect.x}, Y={self.player.rect.y}", 'tiny', WHITE)
            self.screen.blit(pos_text, (10, 90))
            
            limit_text = self.font_manager.render_text(f"Movement Limit: {SCREEN_WIDTH * 5} pixels", 'tiny', WHITE)
            self.screen.blit(limit_text, (10, 110))
        
        # Current location
        location_name = self.level_manager.current_location.value.replace('_', ' ').title()
        location_text = self.font_manager.render_text(f"Location: {location_name}", 'small', WHITE)
        self.screen.blit(location_text, (10, 40))
        
        # Moral standing
        moral_standing = self.moral_system.get_moral_standing()
        moral_color = self.moral_system.get_moral_color()
        moral_text = self.font_manager.render_text(f"Standing: {moral_standing}", 'small', moral_color)
        self.screen.blit(moral_text, (10, 65))
        
        # Instructions with movement reminder
        instruction_text = self.font_manager.render_text("Arrow Keys: Move Moses | E: Interact | I: Inventory | ESC: Pause", 'tiny', WHITE)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
        
        # Game state indicator
        state_text = self.font_manager.render_text(f"State: {self.state.value}", 'tiny', GREEN)
        self.screen.blit(state_text, (10, 115))
        
        # Audio status
        audio_status = []
        if not self.sound_manager.music_enabled:
            audio_status.append("Music: OFF")
        if not self.sound_manager.sound_enabled:
            audio_status.append("Sound: OFF")
        
        if audio_status:
            audio_text = self.font_manager.render_text(" | ".join(audio_status), 'tiny', RED)
            self.screen.blit(audio_text, (SCREEN_WIDTH - 200, 10))
        
        # FPS counter (if enabled)
        if self.show_fps:
            fps = self.clock.get_fps()
            fps_text = self.font_manager.render_text(f"FPS: {fps:.1f}", 'tiny', GREEN)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
    
    def render_pause_menu(self):
        """Render pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Pause menu with custom font
        pause_text = self.font_manager.render_text("PAUSED", 'large', WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        instructions = [
            "ESC or SPACE: Resume",
            "Q: Return to Main Menu"
        ]
        
        y_offset = SCREEN_HEIGHT//2 + 20
        for instruction in instructions:
            text = self.font_manager.render_text(instruction, 'small', WHITE)
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
        
        # Victory text with custom font
        victory_text = self.font_manager.render_text("Victory!", 'large', GOLD)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(victory_text, victory_rect)
        
        completion_text = self.font_manager.render_text("Moses has reached the Promised Land!", 'medium', WHITE)
        completion_rect = completion_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(completion_text, completion_rect)
        
        moral_text = self.font_manager.render_text(f"Final Standing: {self.moral_system.get_moral_standing()}", 'medium', WHITE)
        moral_rect = moral_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(moral_text, moral_rect)
        
        restart_text = self.font_manager.render_text("Press SPACE to play again or ESC to quit", 'small', WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
    
    def render_game_over_screen(self):
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with custom font
        game_over_text = self.font_manager.render_text("Game Over", 'large', WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.font_manager.render_text("Press SPACE to restart or ESC to quit", 'medium', WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)

def main():
    """Main function to run the game"""
    try:
        print("=" * 50)
        print("Moses Adventure - Biblical Platformer Game")
        print("=" * 50)
        print("Initializing game...")
        
        game = MosesAdventureGame()
        game.run()
        
    except Exception as e:
        print(f"Game crashed with error: {e}")
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
