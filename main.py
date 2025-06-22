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
    from sound_manager import SoundManager  # Import the new sound manager
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
        # Enhanced audio initialization
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Moses Adventure - Biblical Platformer")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.MENU
        self.stone_throw_mode = False  # Stone throwing mode
        self.healing_ready = False  # Healing ready mode
        self.healing_item = None  # What healing item is ready
        self.healing_amount = 0  # How much healing is ready
        
        # Initialize font manager
        self.font_manager = initialize_font_manager()
        
        # Game systems
        self.player = None
        self.camera = Camera()
        self.level_manager = LevelManager()
        self.inventory = Inventory()
        self.inventory.game_instance = self  # Connect for item effects
        self.dialogue_system = DialogueSystem()
        self.dialogue_system.game_instance = self  # Connect for health effects
        self.sound_manager = SoundManager()
        self.moral_system = MoralSystem()
        self.visual_feedback = VisualFeedback()
        
        # Connect systems
        # self.dialogue_system.moral_system = self.moral_system
        self.dialogue_system.set_sound_manager(self.sound_manager)
        
        # Load sprites
        self.sprites = self.load_sprites()
        
        # Game state
        self.paused = False
        self.show_fps = False
        self.stone_throw_mode = False  # For stone throwing at enemies
        self.scripture_dialogue_active = False
        
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
        print("- Number Keys (1-9): Use items from inventory")
        print("- H: Apply healing (after using healing items)")
        print("- A: Throw stone (when stone is ready)")
        print("- W: Shoot staff projectile (when staff is active)")
        print("- W: Shoot staff projectile (when staff is active)")
        print("- M: Toggle Music")
        print("- S: Toggle Sound Effects")
        print("- ESC: Pause/Menu")
        print("- F1: Show FPS")
        print("- F11: Toggle Fullscreen")
        print("- Ctrl+1/2/3: Walking pace (Slow/Normal/Fast)")
                # FPS Optimization Settings
        self.target_fps = 60
        self.clock = pygame.time.Clock()
        self.frame_skip = 0  # Skip frames if needed
        self.performance_mode = True
        
        # Reduce debug output for better performance
        self.debug_collision = False
        self.debug_camera = False
        
        print(f"🚀 Performance optimization enabled - Target FPS: {self.target_fps}")
        # Enhanced visual feedback system for all messages
        self.feedback_messages = []  # List of active feedback messages
        self.feedback_duration = 1.5  # 1.5 seconds display time for all messages
        
        # Legacy support for consumption text
        self.consumption_text = ""
        self.consumption_text_timer = 0.0
        self.consumption_text_duration = 1.5  # Updated to 1.5 seconds
        
        print("✅ Item consumption text timer system initialized")
        
    def initialize_multi_level_world(self):
        """Initialize the multi-level platform world"""
        print("🏗️  Creating multi-level platform world...")
        
                # Create platform system with MUCH MORE HEIGHT SPACING from old platforms
        # Old platforms are around y=608-670, new platforms positioned MUCH HIGHER for clear separation
        # 400px horizontal spacing, 160px+ vertical spacing between levels
        self.game_platforms = [
            # Base level - MUCH HIGHER above old platforms (y=480-520) - 88-128px separation from old platforms
            {'x': 400, 'y': 490, 'width': 120, 'height': 20},   # 400px spacing between platforms
            {'x': 800, 'y': 500, 'width': 110, 'height': 20},   # 400px spacing - no overlap
            {'x': 1200, 'y': 495, 'width': 120, 'height': 20},  # 400px spacing - clear separation
            {'x': 1600, 'y': 505, 'width': 110, 'height': 20},  # 400px spacing - well spaced
            {'x': 2000, 'y': 490, 'width': 120, 'height': 20},  # 400px spacing - good distance
            {'x': 2400, 'y': 500, 'width': 110, 'height': 20},  # 400px spacing - final base platform
            
            # Level 1 - First elevated platforms (y=320-360) - 160px above base level
            {'x': 300, 'y': 330, 'width': 100, 'height': 20},   # Offset start, 400px spacing
            {'x': 700, 'y': 340, 'width': 95, 'height': 20},    # 400px spacing - good distance
            {'x': 1100, 'y': 335, 'width': 100, 'height': 20},  # 400px spacing - clear separation
            {'x': 1500, 'y': 345, 'width': 95, 'height': 20},   # 400px spacing - well spaced
            {'x': 1900, 'y': 330, 'width': 100, 'height': 20},  # 400px spacing - good distance
            {'x': 2300, 'y': 340, 'width': 95, 'height': 20},   # 400px spacing - final level 1
            
            # Level 2 - Second elevated platforms (y=160-200) - 160px above Level 1
            {'x': 200, 'y': 170, 'width': 85, 'height': 20},    # Offset start, 400px spacing
            {'x': 600, 'y': 180, 'width': 90, 'height': 20},    # 400px spacing - good distance
            {'x': 1000, 'y': 175, 'width': 85, 'height': 20},   # 400px spacing - clear separation
            {'x': 1400, 'y': 185, 'width': 90, 'height': 20},   # 400px spacing - well spaced
            {'x': 1800, 'y': 170, 'width': 85, 'height': 20},   # 400px spacing - good distance
            {'x': 2200, 'y': 180, 'width': 90, 'height': 20},   # 400px spacing - final level 2
            
            # Level 3 - Third elevated platforms (y=20-60) - 140px above Level 2
            {'x': 500, 'y': 30, 'width': 75, 'height': 20},     # Centered start, 400px spacing
            {'x': 900, 'y': 40, 'width': 80, 'height': 20},     # 400px spacing - good distance
            {'x': 1300, 'y': 35, 'width': 75, 'height': 20},    # 400px spacing - clear separation
            {'x': 1700, 'y': 45, 'width': 80, 'height': 20},    # 400px spacing - well spaced
            {'x': 2100, 'y': 30, 'width': 75, 'height': 20},    # 400px spacing - final level 3
        ]
        
        # Create strategic items on HIGHER SPACED platforms (positioned on platform centers)
        self.game_items = [
            # Base level items (y=480-520) - On much higher platforms
            {'x': 460, 'y': 470, 'type': 'stone'},      # On platform at x=400
            {'x': 860, 'y': 480, 'type': 'water'},      # On platform at x=800
            {'x': 1260, 'y': 475, 'type': 'bread'},     # On platform at x=1200
            {'x': 1660, 'y': 485, 'type': 'scroll'},    # On platform at x=1600
            {'x': 2060, 'y': 470, 'type': 'meat'},      # On platform at x=2000
            {'x': 2460, 'y': 480, 'type': 'armor_of_god'}, # On platform at x=2400
            
            # Level 1 items (y=320-360) - On elevated platforms
            {'x': 360, 'y': 310, 'type': 'water'},      # On platform at x=300
            {'x': 760, 'y': 320, 'type': 'bread'},      # On platform at x=700
            {'x': 1160, 'y': 315, 'type': 'scroll'},    # On platform at x=1100
            {'x': 1560, 'y': 325, 'type': 'meat'},      # On platform at x=1500
            {'x': 1960, 'y': 310, 'type': 'armor_of_god'}, # On platform at x=1900
            {'x': 2360, 'y': 320, 'type': 'staff'},     # On platform at x=2300
            
            # Level 2 items (y=160-200) - On higher platforms
            {'x': 260, 'y': 150, 'type': 'scroll'},     # On platform at x=200
            {'x': 660, 'y': 160, 'type': 'meat'},       # On platform at x=600
            {'x': 1060, 'y': 155, 'type': 'armor_of_god'}, # On platform at x=1000
            {'x': 1460, 'y': 165, 'type': 'staff'},     # On platform at x=1400
            {'x': 1860, 'y': 150, 'type': 'stone'},     # On platform at x=1800
            {'x': 2260, 'y': 160, 'type': 'water'},     # On platform at x=2200
            
            # Level 3 items (y=20-60) - On top platforms - Ultimate rewards
            {'x': 560, 'y': 10, 'type': 'armor_of_god'}, # On platform at x=500 - Ultimate reward
            {'x': 960, 'y': 20, 'type': 'staff'},       # On platform at x=900 - Ultimate reward
            {'x': 1360, 'y': 15, 'type': 'meat'},       # On platform at x=1300 - Ultimate reward
            {'x': 1760, 'y': 25, 'type': 'scroll'},     # On platform at x=1700 - Ultimate reward
            {'x': 2160, 'y': 10, 'type': 'stone'},      # On platform at x=2100 - Ultimate reward
        ]
        
        # Create NPCs and enemies on platforms
        self.game_npcs = [
            # Ground NPCs
            {'x': 320, 'y': 550, 'type': 'hebrew_slave'},
            {'x': 720, 'y': 560, 'type': 'egyptian_citizen'},
            {'x': 1120, 'y': 575, 'type': 'priest'},
            {'x': 1720, 'y': 540, 'type': 'palace_guard'},
            
            # Platform NPCs
            {'x': 470, 'y': 460, 'type': 'egyptian_citizen'},
            {'x': 870, 'y': 470, 'type': 'hebrew_slave'},
            {'x': 1270, 'y': 465, 'type': 'priest'},
            {'x': 420, 'y': 360, 'type': 'priest'},
            {'x': 820, 'y': 370, 'type': 'hebrew_slave'},
            {'x': 570, 'y': 250, 'type': 'priest'},
            {'x': 970, 'y': 240, 'type': 'palace_guard'},
        ]
        
        self.game_enemies = [
            # Ground enemies
            {'x': 600, 'y': 640, 'type': 'egyptian_soldier'},
            {'x': 1000, 'y': 620, 'type': 'egyptian_soldier'},
            {'x': 1400, 'y': 640, 'type': 'egyptian_soldier'},
            {'x': 1800, 'y': 640, 'type': 'egyptian_soldier'},
            
            # Platform enemies
            {'x': 540, 'y': 570, 'type': 'egyptian_soldier'},
            {'x': 940, 'y': 588, 'type': 'egyptian_soldier'},
            {'x': 290, 'y': 450, 'type': 'egyptian_soldier'},
            {'x': 690, 'y': 440, 'type': 'egyptian_soldier'},
            {'x': 1090, 'y': 450, 'type': 'egyptian_soldier'},
            {'x': 240, 'y': 350, 'type': 'egyptian_soldier'},
            {'x': 640, 'y': 340, 'type': 'egyptian_soldier'},
            {'x': 1040, 'y': 350, 'type': 'egyptian_soldier'},
            {'x': 390, 'y': 260, 'type': 'egyptian_soldier'},
            {'x': 790, 'y': 270, 'type': 'egyptian_soldier'},
            {'x': 1190, 'y': 265, 'type': 'egyptian_soldier'},
        ]
        
        print(f"✅ Created {len(self.game_platforms)} platforms across 4 levels")
        print(f"✅ Created {len(self.game_items)} strategic items")
        print(f"✅ Created {len(self.game_npcs)} NPCs and {len(self.game_enemies)} enemies")
        
        return True


    def load_sprites(self):
        """Load all game sprites including NPCs and tiles for enhanced UI"""
        sprites = {}
        
        # Load tile sprites for enhanced UI
        sprites['tiles'] = {}
        tile_path = "assets/tiles/"
        if os.path.exists(tile_path):
            tile_files = ['ground', 'stone_platform', 'palace_wall', 'sand', 'water']
            for tile_name in tile_files:
                sprite = self.load_sprite(f"{tile_path}{tile_name}.png")
                if sprite:
                    sprites['tiles'][tile_name] = sprite
                    print(f"✅ Loaded tile: {tile_name}")
                else:
                    # Create fallback tile
                    sprites['tiles'][tile_name] = self.create_tile_fallback(tile_name)
        
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
                print(f"✅ Loaded NPC: {npc_type}")
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
        
        # Load enemy sprites
        sprites['enemies'] = {}
        enemy_path = "assets/sprites/enemies/"
        enemy_types = ['egyptian_soldier', 'wild_animal']
        for enemy_type in enemy_types:
            sprite = self.load_sprite(f"{enemy_path}{enemy_type}.png")
            if sprite:
                sprites['enemies'][enemy_type] = sprite
                print(f"✅ Loaded enemy: {enemy_type}")
            else:
                # Create fallback enemy sprite
                sprites['enemies'][enemy_type] = self.create_enemy_fallback(enemy_type)
        
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
        
        print(f"🎨 Loaded sprites: {len(sprites['tiles'])} tiles, {len(sprites['npcs'])} NPCs, {len(sprites['player'])} player, {len(sprites.get('enemies', {}))} enemies")
        return sprites
    
    def create_tile_fallback(self, tile_name):
        """Create fallback tile sprites with appropriate colors"""
        surface = pygame.Surface((32, 32))
        
        tile_colors = {
            'ground': (139, 69, 19),      # Brown
            'stone_platform': (128, 128, 128),  # Gray
            'palace_wall': (218, 165, 32),      # Golden
            'sand': (238, 203, 173),            # Sandy
            'water': (64, 164, 223)             # Blue
        }
        
        color = tile_colors.get(tile_name, (100, 100, 100))
        surface.fill(color)
        
        # Add simple pattern
        pygame.draw.rect(surface, (color[0] + 20, color[1] + 20, color[2] + 20), (0, 0, 32, 32), 2)
        
        return surface
    
    def create_enemy_fallback(self, enemy_type):
        """Create fallback enemy sprites"""
        surface = pygame.Surface((32, 32))
        
        enemy_colors = {
            'egyptian_soldier': (220, 20, 60),    # Red
            'wild_animal': (139, 69, 19)          # Brown
        }
        
        color = enemy_colors.get(enemy_type, (128, 128, 128))
        surface.fill(color)
        
        # Add enemy design
        pygame.draw.circle(surface, (0, 0, 0), (16, 16), 4)  # Eye
        pygame.draw.rect(surface, (255, 255, 255), (12, 20, 8, 8))  # Body
        pygame.draw.rect(surface, (0, 0, 0), surface.get_rect(), 2)  # Border
        
        return surface
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
        print("Controls: Arrow keys to move, E to interact, M for music, S for sound")
        
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
            
            # Mouse click for stone throwing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.stone_throw_mode:  # Left click
                    self.handle_stone_throw(event.pos)
            
            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")
                
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
            
            # State-specific events
            if self.state == GameState.MENU:
                self.handle_menu_events(event)
            elif self.state == GameState.PLAYING:
                self.handle_game_events(event)
            elif self.state == GameState.DIALOGUE:
                # Handle dialogue events
                self.dialogue_system.handle_event(event)
                if not self.dialogue_system.active:
                    self.state = GameState.PLAYING
                    print("🎭 Dialogue ended - returning to gameplay")
                self.dialogue_system.render(self.screen, self.sprites)
                # Dialogue system rendering (debug reduced)
                # Emergency dialogue exit if system is stuck
                if not hasattr(self.dialogue_system, 'active') or not self.dialogue_system.active:
                    print("🔄 Dialogue system inactive - returning to game")
                    self.state = GameState.PLAYING
                else:
                    self.dialogue_system.handle_event(event)
                    if not self.dialogue_system.active:
                        self.state = GameState.PLAYING
                        # Remove the NPC that was just talked to
                    self.remove_interacted_npc()
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
            # Close scripture dialogue if active
            if self.scripture_dialogue_active:
                self.scripture_dialogue_active = False
                return
            
            # Handle stone throwing mode
            if hasattr(self, 'stone_throw_mode') and self.stone_throw_mode:
                if event.key == pygame.K_a:
                    # Throw stone
                    self.throw_stone_from_inventory()
                    return
                
                # Skip dialogue with SPACE or ENTER
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    if self.state == GameState.DIALOGUE:
                        if hasattr(self.dialogue_system, 'active') and self.dialogue_system.active:
                            # Skip to end of current dialogue or advance
                            if hasattr(self.dialogue_system, 'skip_to_end'):
                                self.dialogue_system.skip_to_end()
                            else:
                                # Force dialogue to end if stuck
                                self.dialogue_system.active = False
                                self.state = GameState.PLAYING
                                print("🔄 Dialogue skipped - returning to game")
                
            elif event.key == pygame.K_ESCAPE:
                    # Cancel stone throw mode
                    self.stone_throw_mode = False
                    self.visual_feedback.show_message("Stone throw cancelled", 1.5)
                    return
            
            # Handle healing
            elif event.key == pygame.K_h:
                self.apply_healing()
                return
            
            # Handle staff shooting - COMPREHENSIVE DEBUG VERSION
            elif event.key == pygame.K_w:
                print("🎯 W KEY PRESSED!")
                if self.player:
                    print(f"🎯 Player exists: {self.player is not None}")
                    if hasattr(self.player, 'staff_active'):
                        print(f"🎯 Staff active: {self.player.staff_active}")
                        if self.player.staff_active:
                            print("🎯 Attempting to shoot staff projectile...")
                            success = self.player.shoot_staff_projectile()
                            print(f"🎯 Shoot success: {success}")
                            if success:
                                # Play staff sound if available
                                if hasattr(self.sound_manager, 'play_sound'):
                                    self.sound_manager.play_sound('jump')
                                # Visual feedback
                                if hasattr(self.visual_feedback, 'show_message'):
                                    self.visual_feedback.show_message("⚡ Divine Energy!", 1.0)
                                print("🎯 Staff projectile should be created and visible!")
                            else:
                                print("❌ Failed to shoot staff projectile")
                        else:
                            print("❌ Staff not active! Use staff from inventory first.")
                            if hasattr(self.visual_feedback, 'show_message'):
                                self.visual_feedback.show_message("Staff not active!", 1.5)
                    else:
                        print("❌ Player has no staff_active attribute")
                else:
                    print("❌ No player found")
                return
            
            elif event.key == pygame.K_i:
                self.inventory.active = True
                self.state = GameState.INVENTORY
            elif event.key == pygame.K_ESCAPE:
                self.paused = True
                self.state = GameState.PAUSED
                # Play pause sound effect
                self.sound_manager.play_pause_sound()
            elif event.key == pygame.K_m:
                self.sound_manager.toggle_music()
            elif event.key == pygame.K_s:
                self.sound_manager.toggle_sound()
            # Walking pace controls (for testing/customization)
            elif event.key == pygame.K_1 and pygame.key.get_pressed()[pygame.K_LCTRL]:
                # Ctrl+1 = Slow walking pace
                if hasattr(self.player, 'set_walking_pace'):
                    self.player.set_walking_pace("slow")
                    self.visual_feedback.show_message("Walking pace: SLOW", 2.0)
            elif event.key == pygame.K_2 and pygame.key.get_pressed()[pygame.K_LCTRL]:
                # Ctrl+2 = Normal walking pace
                if hasattr(self.player, 'set_walking_pace'):
                    self.player.set_walking_pace("normal")
                    self.visual_feedback.show_message("Walking pace: NORMAL", 2.0)
            elif event.key == pygame.K_3 and pygame.key.get_pressed()[pygame.K_LCTRL]:
                # Ctrl+3 = Fast walking pace
                if hasattr(self.player, 'set_walking_pace'):
                    self.player.set_walking_pace("fast")
                    self.visual_feedback.show_message("Walking pace: FAST", 2.0)
    
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
                # Restart the game
                print("🔄 Restarting Moses' journey...")
                self.restart_game()
                # Play restart sound if available
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_r:
                # Alternative restart key
                print("🔄 Restarting Moses' journey...")
                self.restart_game()
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_ESCAPE:
                # Return to main menu
                print("📋 Returning to main menu...")
                self.state = GameState.MENU
                self.player = None
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_q:
                # Quit game
                print("👋 Farewell, Moses...")
                self.running = False
    
    def restart_game(self):
        """Restart the game from the beginning"""
        # Reset player health and position
        ground_y = SCREEN_HEIGHT - 50
        player_y = ground_y - 48
        self.player = Player(150, player_y, self.sprites.get('player', {}))
        
        # Give player access to platforms for collision detection
        if hasattr(self, 'game_platforms'):
            self.player.game_platforms = self.game_platforms
        
        # Reset player health to full
        self.player.health = self.player.max_health
        
        # Clear any active states
        self.stone_throw_mode = False
        self.healing_ready = False
        self.healing_item = None
        self.healing_amount = 0
        
        # Reset inventory (optional - you might want to keep items)
        # self.inventory = Inventory()
        # self.inventory.game_instance = self
        
        # Reload the current level
        self.level_manager.load_level(Location.PALACE, self.sprites)
        
        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")
        
        # Platform integration handled by render_platforms method
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")
        
        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")
        
        # Platform integration handled by render_platforms method
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")
        
        # Reset camera
        self.camera = Camera()
        
        # Connect systems
        self.player.sound_manager = self.sound_manager
        
        # Start playing again
        self.state = GameState.PLAYING
        
        print("✅ Game restarted successfully!")
    
    def start_game(self):
        """Initialize and start the game with opening dialogue"""
        # Place player properly on the ground
        # Ground platform is at y=718, player height is 48, so player should be at y=670
        ground_y = SCREEN_HEIGHT - 50  # 718
        player_y = ground_y - 48  # 670 (player height is 48)
        self.player = Player(150, player_y, self.sprites.get('player', {}))
        
        # Give player access to platforms for collision detection
        if hasattr(self, 'game_platforms'):
            self.player.game_platforms = self.game_platforms
        
        # Debug: Show Moses' exact position
        print(f"🎯 Moses Position: x={self.player.rect.x}, y={self.player.rect.y}, bottom={self.player.rect.bottom}")
        
        # Connect sound manager to player for jump sounds
        if hasattr(self.player, 'set_sound_manager'):
            self.player.set_sound_manager(self.sound_manager)
        
        # Configure realistic walking sounds
        if hasattr(self.player, 'set_walking_pace'):
            self.player.set_walking_pace("normal")  # Set normal walking pace
        
        # Set comfortable step volume
        self.sound_manager.set_step_volume(0.5)  # 50% volume for comfortable listening
        
        self.level_manager.load_level(Location.PALACE, self.sprites)
        
        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")
        
        # Platform integration handled by render_platforms method
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")
        
        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")
        
        # Platform integration handled by render_platforms method
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")
        
        # Reset camera to show the game world properly
        self.camera.x = 0
        self.camera.y = 0
        
        # Play ancient_egypt.mp3 background music
        self.sound_manager.play_background_music()
        
        # Reset game systems
        self.moral_system = MoralSystem()
        # self.dialogue_system.moral_system = self.moral_system
        self.inventory = Inventory()
        self.inventory.game_instance = self  # Connect for item effects
        self.visual_feedback = VisualFeedback()
        
        # START WITH OPENING DIALOGUE instead of going straight to playing
        
        # DIALOGUE BYPASS FOR TESTING - uncomment next line to skip dialogue
        # self.state = GameState.PLAYING; return
        
        # START WITH OPENING DIALOGUE - RESTORED
        self.state = GameState.DIALOGUE
        self.dialogue_system.start_dialogue("opening")
        print("🎭 Opening dialogue started - narrator text should appear")
        print("💬 DIALOGUE CONTROLS:")
        print("   - SPACE or ENTER: Advance dialogue")
        print("   - ESC: Skip dialogue (if needed)")
        print("   - Read the narrator text and press SPACE to continue")
        
        
        print("Game started! Opening dialogue will begin...")
        print("Controls: Arrow keys to move, E to interact, M for music, S for sound")
    
    def update(self, dt):
        """Update game state with delta time for smooth 60 FPS"""
        # Update scripture dialogue timer
        if self.scripture_dialogue_active:
            self.scripture_timer -= dt
            if self.scripture_timer <= 0:
                self.scripture_dialogue_active = False
        
        if self.state == GameState.PLAYING:
            if self.player:
                # Update player physics
                self.player.update(dt)
        
        # Update camera to follow Moses vertically and horizontally
        if hasattr(self, 'camera') and hasattr(self, 'player'):
            self.camera.follow_player(self.player)
        
        # Update simple enemies
        self.level_manager.update_simple_enemies(dt)
        
        # Update stone projectiles
        self.level_manager.update_stones(dt)
        
        # Check stone-enemy collisions
        hits = self.level_manager.check_stone_enemy_collisions()
        if hits > 0:
            # Play enemy defeat sound
            if hasattr(self.sound_manager, 'play_sound'):
                self.sound_manager.play_sound('enemy_defeat')
        
        # Check collisions AFTER player update
        self.check_collisions()
        
        # Update camera and other systems
        if self.player:
            self.camera.follow_player(self.player)
        self.check_interactions()
        self.check_level_transitions()
        
        # Check for game over
        if self.player and self.player.health <= 0:
            self.state = GameState.GAME_OVER
        
            self.level_manager.update(dt)

        # Update all visual feedback messages
        if self.consumption_text_timer > 0:
            self.consumption_text_timer -= dt
            if self.consumption_text_timer <= 0:
                self.consumption_text = ""  # Clear text after timer expires
        
        # Update item feedback messages (separate from dialogue)
        if hasattr(self, 'item_feedback_messages'):
            for message in self.item_feedback_messages[:]:
                message['timer'] -= dt
                if message['timer'] <= 0:
                    self.item_feedback_messages.remove(message)
        
        # Update feedback messages list (keep for backward compatibility)
        if hasattr(self, 'feedback_messages'):
            for message in self.feedback_messages[:]:
                message['timer'] -= dt
                if message['timer'] <= 0:
                    self.feedback_messages.remove(message)
            self.visual_feedback.update(dt)
        
        elif self.state == GameState.DIALOGUE:
            # Update dialogue system for typing effect
            if self.dialogue_system and self.dialogue_system.active:
                self.dialogue_system.update(dt)
    
    def check_collisions(self):
        """Check for collisions with FIXED physics effects"""
        if not self.player:
            return
        
        try:
            # Platform collisions with FIXED physics
            platforms = self.level_manager.get_platforms()
            
            # Debug: Show platform count
            if not hasattr(self, '_platform_debug_shown'):
                print(f"🏗️  Loaded {len(platforms)} platforms for collision detection")
                self._platform_debug_shown = True
            
            # FIXED: Check if player needs platform support after horizontal movement
            if hasattr(self.player, 'needs_platform_check') and self.player.needs_platform_check:
                self.player.needs_platform_check = False
                # Check if player is still on any platform
                on_platform = False
                for platform in platforms:
                    if platform and hasattr(platform, 'rect'):
                        # Check if player's bottom is close to platform top and overlapping horizontally
                        if (abs(self.player.rect.bottom - platform.rect.top) <= 5 and
                            self.player.rect.right > platform.rect.left and
                            self.player.rect.left < platform.rect.right):
                            on_platform = True
                            break
                
                # If not on any platform, start falling
                if not on_platform:
                    self.player.on_ground = False
                    print("🪂 Moses walked off platform - starting to fall")
            
            # Regular collision detection
            for platform in platforms:
                if platform and hasattr(platform, 'rect') and self.player.rect.colliderect(platform.rect):
                    self.handle_platform_collision(platform)
            
            # Item collisions
            items = self.level_manager.get_items()
            for item in items[:]:
                if item and hasattr(item, 'rect') and self.player.rect.colliderect(item.rect):
                    self.collect_item(item)
            
            # Enemy collisions (original enemies)
            enemies = self.level_manager.get_enemies()
            for enemy in enemies:
                if enemy and hasattr(enemy, 'rect') and self.player.rect.colliderect(enemy.rect):
                    self.handle_enemy_collision(enemy)
            
            # Simple enemy collisions
            collision_result = self.level_manager.check_simple_enemy_collisions(self.player)
            if collision_result == 'game_over':
                self.state = GameState.GAME_OVER
            elif collision_result == 'damage_taken':
                # Player took damage but is still alive
                pass
        
            
            # Staff projectile collisions
            if hasattr(self.player, 'staff_projectiles'):
                for projectile in self.player.staff_projectiles[:]:
                    # Check collision with enemies
                    enemies = self.level_manager.get_enemies()
                    for enemy in enemies:
                        if enemy and hasattr(enemy, 'rect') and projectile.rect.colliderect(enemy.rect):
                            # Staff hit enemy
                            if hasattr(enemy, 'health'):
                                enemy.health -= projectile.damage
                                if enemy.health <= 0:
                                    enemy.defeated = True
                            elif hasattr(enemy, 'defeated'):
                                enemy.defeated = True
                            
                            # Remove projectile
                            projectile.active = False
                            
                            # Visual and audio feedback
                            if hasattr(self.visual_feedback, 'create_dust_effect'):
                                self.visual_feedback.create_dust_effect(enemy.rect.centerx, enemy.rect.centery)
                            if hasattr(self.sound_manager, 'play_sound'):
                                self.sound_manager.play_sound('enemy_defeat')
                            
                            print(f"⚡ Staff projectile hit enemy for {projectile.damage} damage!")
                            break
                    
                    # Check collision with simple enemies
                    simple_enemies = self.level_manager.get_simple_enemies()
                    for enemy in simple_enemies:
                        if enemy and not enemy['defeated'] and projectile.rect.colliderect(enemy['rect']):
                            # Staff hit simple enemy
                            enemy['defeated'] = True
                            projectile.active = False
                            
                            # Visual and audio feedback
                            if hasattr(self.visual_feedback, 'create_dust_effect'):
                                self.visual_feedback.create_dust_effect(enemy['rect'].centerx, enemy['rect'].centery)
                            if hasattr(self.sound_manager, 'play_sound'):
                                self.sound_manager.play_sound('enemy_defeat')
                            
                            print(f"⚡ Staff projectile defeated simple enemy!")
                            break
        
        except Exception as e:
            print(f"⚠️  Collision check error: {e}")
    
    def handle_platform_collision(self, platform):
        """Handle collision with platforms with FIXED physics"""
        if not self.player or not platform:
            return
            
        player = self.player
        
        try:
            # Calculate overlap with tolerance for edge cases
            overlap_x = min(player.rect.right - platform.rect.left, 
                           platform.rect.right - player.rect.left)
            overlap_y = min(player.rect.bottom - platform.rect.top, 
                           platform.rect.bottom - player.rect.top)
            
            # FIXED: Better platform landing detection
            if abs(player.rect.bottom - platform.rect.top) <= 5 and player.velocity_y >= 0:
                # Player is landing on or standing on platform
                player.rect.bottom = platform.rect.top
                if hasattr(player, 'velocity_y'):
                    player.velocity_y = 0
                if hasattr(player, 'on_ground'):
                    player.on_ground = True
                if hasattr(player, 'is_jumping'):
                    player.is_jumping = False
                
                # Clear the platform check flag if it exists
                if hasattr(player, 'needs_platform_check'):
                    player.needs_platform_check = False
                
                # Create dust effect
                if hasattr(self, 'visual_feedback'):
                    self.visual_feedback.create_dust_effect(player.rect.centerx, player.rect.bottom)
                # Landing sound
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound("jump")
                return
            
            # Resolve collision based on smallest overlap for other cases
            if overlap_x < overlap_y:
                # Horizontal collision
                if player.rect.centerx < platform.rect.centerx:
                    player.rect.right = platform.rect.left
                else:
                    player.rect.left = platform.rect.right
                if hasattr(player, 'velocity_x'):
                    player.velocity_x = 0
            else:
                # Vertical collision
                if player.rect.centery < platform.rect.centery:
                    # Landing on top
                    player.rect.bottom = platform.rect.top
                    if hasattr(player, 'velocity_y'):
                        player.velocity_y = 0
                    if hasattr(player, 'on_ground'):
                        player.on_ground = True
                    if hasattr(player, 'is_jumping'):
                        player.is_jumping = False
                    
                    # Clear the platform check flag if it exists
                    if hasattr(player, 'needs_platform_check'):
                        player.needs_platform_check = False
                    
                    # Create dust effect
                    if hasattr(self, 'visual_feedback'):
                        self.visual_feedback.create_dust_effect(player.rect.centerx, player.rect.bottom)
                    # Landing sound
                    if hasattr(self.sound_manager, 'play_sound'):
                        self.sound_manager.play_sound("jump")
                else:
                    # Hitting from below
                    player.rect.top = platform.rect.bottom
                    if hasattr(player, 'velocity_y'):
                        player.velocity_y = 0
        except Exception as e:
            print(f"⚠️  Collision error: {e}")
            # Prevent crash by doing basic collision resolution
            if hasattr(player, 'rect') and hasattr(platform, 'rect'):
                player.rect.bottom = platform.rect.top - 1
    
    def collect_item(self, item):
        """Collect an item and add to inventory"""
        try:
            self.inventory.add_item(item.item_type)
            self.level_manager.remove_item(item)
            
            if hasattr(self.sound_manager, 'play_sound'):
                self.sound_manager.play_sound("pickup")
            
            # Show visual feedback if available
            if hasattr(self.visual_feedback, 'show_item_collected'):
                self.visual_feedback.show_item_collected(item.item_type, item.rect.center)
            elif hasattr(self.visual_feedback, 'create_pickup_effect'):
                self.visual_feedback.create_pickup_effect(item.rect.centerx, item.rect.centery)
            
            print(f"📦 Collected {item.item_type}")
        except Exception as e:
            print(f"⚠️  Item collection error: {e}")
    
    def handle_enemy_collision(self, enemy):
        """Handle collision with enemies - damage instead of instant death"""
        try:
            if self.player.velocity_y > 0 and self.player.rect.bottom <= enemy.rect.top + 10:
                # Player jumped on enemy
                if hasattr(enemy, 'defeated'):
                    enemy.defeated = True
                self.player.velocity_y = JUMP_STRENGTH // 2  # Small bounce
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound("enemy_defeat")
                if hasattr(self.visual_feedback, 'create_sparkle_effect'):
                    self.visual_feedback.create_sparkle_effect(enemy.rect.center)
                print("⚔️  Enemy defeated!")
            else:
                # Player takes damage instead of instant death
                damage = 15
                self.player.health -= damage
                print(f"💔 Moses took {damage} damage! Health: {self.player.health}/100")
                
                # Push player back to avoid continuous damage
                if self.player.rect.centerx < enemy.rect.centerx:
                    self.player.rect.x -= 30
                else:
                    self.player.rect.x += 30
                
                # Play hurt sound
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound("player_hurt")
                
                # Visual feedback
                if hasattr(self.visual_feedback, 'create_dust_effect'):
                    self.visual_feedback.create_dust_effect(self.player.rect.centerx, self.player.rect.centery)
                
                # Check for game over only when health reaches 0
                if self.player.health <= 0:
                    print("💀 Moses has fallen! Game Over!")
                    self.state = GameState.GAME_OVER
        except Exception as e:
            print(f"⚠️  Enemy collision error: {e}")
            # Fallback: just push player away
            if self.player.rect.centerx < enemy.rect.centerx:
                self.player.rect.x -= 20
            else:
                self.player.rect.x += 20
    
    def remove_interacted_npc(self):
        """Remove the NPC that was just interacted with"""
        if hasattr(self, 'last_interacted_npc') and self.last_interacted_npc:
            try:
                # Mark NPC as completed and move them off-screen
                npc = self.last_interacted_npc
                npc.rect.x = -1000  # Move far off-screen
                npc.completed = True
                print(f"✅ {npc.npc_type} completed their task and moved away")
                
                # Alternative: Remove from level manager if possible
                if hasattr(self.level_manager, 'remove_npc'):
                    self.level_manager.remove_npc(npc)
                
                self.last_interacted_npc = None
            except Exception as e:
                print(f"⚠️  Error removing NPC: {e}")
    
    def check_interactions(self):
        """Check for NPC interactions with enhanced visibility and feedback"""
        if not self.player:
            return
        
        try:
            npcs = self.level_manager.get_npcs()
            keys = pygame.key.get_pressed()
            
            interaction_found = False
            
            for npc in npcs:
                if not npc or not hasattr(npc, 'rect'):
                    continue
                    
                # Check if player is close enough to interact (increased range)
                distance = abs(self.player.rect.centerx - npc.rect.centerx)
                vertical_distance = abs(self.player.rect.centery - npc.rect.centery)
                
                # More generous interaction range
                if distance < 100 and vertical_distance < 60:  # Increased interaction range
                    interaction_found = True
                    
                    # Show interaction prompt
                    npc.showing_prompt = True
                    
                    # Show NPC info in console
                    if not hasattr(npc, 'info_shown'):
                        print(f"💬 Press E to talk to {npc.npc_type}")
                        print(f"📏 Distance: {distance} pixels (Moses at x={self.player.rect.x})")
                        npc.info_shown = True
                    
                    if keys[pygame.K_e] and not getattr(npc, 'is_interacting', False):  # Interact key
                        # Store reference to this NPC for removal after dialogue
                        self.last_interacted_npc = npc
                        
                        # Start interaction
                        npc.is_interacting = True
                        
                        # Start interaction animation
                        if hasattr(self.player, 'start_interaction'):
                            self.player.start_interaction()
                        
                        # Switch to dialogue state
                        self.state = GameState.DIALOGUE
                        
                        # Start dialogue with enhanced system
                        dialogue_success = self.dialogue_system.start_dialogue(npc.dialogue_id)
                        if dialogue_success:
                            print(f"✅ Started dialogue with {npc.npc_type}")
                            # Play dialogue sound
                            if hasattr(self.sound_manager, 'play_dialogue_sound'):
                                self.sound_manager.play_dialogue_sound()
                        else:
                            print(f"❌ Failed to start dialogue with {npc.npc_type}")
                            self.state = GameState.PLAYING  # Return to playing if dialogue fails
                        
                        break
                else:
                    # Reset info and prompt when moving away
                    if hasattr(npc, 'info_shown'):
                        npc.info_shown = False
                    if hasattr(npc, 'showing_prompt'):
                        npc.showing_prompt = False
            
            # Clear all interaction prompts if no NPCs are nearby
            if not interaction_found:
                if hasattr(self, 'visual_feedback'):
                    self.visual_feedback.clear_interaction_prompt()
        except Exception as e:
            print(f"⚠️  Interaction check error: {e}")
    
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
    
    def show_scripture_dialogue(self):
        """Show scripture dialogue when scroll is used"""
        scriptures = [
            "\"The Lord is my shepherd; I shall not want.\" - Psalm 23:1",
            "\"Be strong and courageous. Do not be afraid; do not be discouraged, for the Lord your God will be with you wherever you go.\" - Joshua 1:9",
            "\"Trust in the Lord with all your heart and lean not on your own understanding.\" - Proverbs 3:5",
            "\"I can do all things through Christ who strengthens me.\" - Philippians 4:13",
            "\"The Lord will fight for you; you need only to be still.\" - Exodus 14:14",
            "\"Have I not commanded you? Be strong and courageous!\" - Joshua 1:9",
            "\"For I know the plans I have for you,\" declares the Lord, \"plans to prosper you and not to harm you.\" - Jeremiah 29:11"
        ]
        
        import random
        selected_scripture = random.choice(scriptures)
        
        # Create a custom scripture dialogue
        self.scripture_dialogue_active = True
        self.current_scripture = selected_scripture
        self.scripture_timer = 5.0  # Show for 5 seconds
        
        print(f"📜 Scripture: {selected_scripture}")
        self.visual_feedback.show_message("Sacred Scripture", 5.0)
    
    def activate_stone_throw_mode(self):
        """Activate stone throwing mode"""
        self.stone_throw_mode = True
        print("🪨 Stone ready! Press A to throw or ESC to cancel.")
        
    def throw_stone_from_inventory(self):
        """Throw stone when in stone throw mode"""
        if self.stone_throw_mode:  # Removed can_attack requirement for inventory stones
            # Create stone projectile
            stone_x = self.player.rect.centerx + (20 if self.player.facing_right else -20)
            stone_y = self.player.rect.centery
            direction = 1 if self.player.facing_right else -1
            
            stone = Stone(stone_x, stone_y, direction)
            self.level_manager.add_stone(stone)
            
            # Set attack cooldown
            self.player.can_attack = False
            self.player.attack_cooldown = self.player.attack_cooldown_time
            
            # Play throw sound
            if hasattr(self.sound_manager, 'play_sound'):
                self.sound_manager.play_sound('menu_select')
            
            # Deactivate stone throw mode
            self.stone_throw_mode = False
            
            print("🪨 Stone thrown!")
            self.visual_feedback.show_message("Stone thrown!", 1.5)
            return True
        
        return False
    
    def prepare_healing(self, item_name, heal_amount):
        """Prepare healing item for use with H key"""
        self.healing_ready = True
        self.healing_item = item_name
        self.healing_amount = heal_amount
        print(f"💊 {item_name.title()} ready for healing! Press H to restore {heal_amount} health.")
        
    def apply_healing(self):
        """Apply prepared healing when H key is pressed"""
        if self.healing_ready and self.healing_amount > 0:
            old_health = self.player.health
            
            # Check if player is already at full health
            if self.player.health >= self.player.max_health:
                print("💚 Already at full health! No healing needed.")
                self.visual_feedback.show_message("Already at full health!", 2.0)
                # Still clear the healing state
                self.healing_ready = False
                self.healing_item = None
                self.healing_amount = 0
                return True
            
            self.player.heal(self.healing_amount)
            
            # Get healing item emoji
            item_emoji = {
                "meat": "🥩",
                "bread": "🍞", 
                "water": "💧"
            }.get(self.healing_item, "💊")
            
            print(f"{item_emoji} {self.healing_item.title()} consumed! Health: {old_health} → {self.player.health}")
            self.visual_feedback.show_message(f"Health +{self.healing_amount}! ({self.player.health}/{self.player.max_health})", 2.5)
            
            # Play healing sound if available
            if hasattr(self.sound_manager, 'play_sound'):
                self.sound_manager.play_sound('pickup')  # Use pickup sound for healing
            
            # Clear healing state
            self.healing_ready = False
            self.healing_item = None
            self.healing_amount = 0
            
            return True
        else:
            print("💊 No healing item ready! Use healing items from inventory first.")
            self.visual_feedback.show_message("No healing item ready! Use items from inventory first.", 2.5)
            return False
        print("🎯 Stone throw mode activated! Click on an enemy to throw stone.")
    
    def handle_stone_throw(self, mouse_pos):
        """Handle stone throwing at enemies"""
        if not self.stone_throw_mode:
            return
        
        # Check if mouse click hit any enemy
        enemies = self.level_manager.get_enemies()
        camera_offset = self.camera.get_offset()
        
        for enemy in enemies:
            if enemy and hasattr(enemy, 'rect'):
                # Adjust enemy position for camera offset
                enemy_screen_rect = enemy.rect.copy()
                enemy_screen_rect.x -= camera_offset[0]
                enemy_screen_rect.y -= camera_offset[1]
                
                if enemy_screen_rect.collidepoint(mouse_pos):
                    # Hit the enemy with stone
                    print(f"🎯 Stone hit {enemy.__class__.__name__}!")
                    enemy.take_damage(50)  # Stone does significant damage
                    self.visual_feedback.create_sparkle_effect(enemy.rect.center)
                    self.sound_manager.play_sound("enemy_defeat")
                    
                    # Deactivate stone throw mode
                    self.stone_throw_mode = False
                    self.visual_feedback.show_message("Stone thrown successfully!", 2.0)
                    return True
        
        # No enemy hit
        self.stone_throw_mode = False
        self.visual_feedback.show_message("Stone missed target", 1.5)
        return False
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

            # Render dialogue system if active (for NPC interactions)
            if self.dialogue_system.active:
                self.dialogue_system.render(self.screen)
                print("🎭 Rendering NPC dialogue on screen")
            
            if self.state == GameState.DIALOGUE:
                self.dialogue_system.render(self.screen, self.sprites)
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
        
        # Render scripture dialogue if active
        if self.scripture_dialogue_active:
            self.render_scripture_dialogue()
        
        
        
        # Show staff status
        if self.player and hasattr(self.player, 'staff_active') and self.player.staff_active:
            staff_time = self.player.get_staff_time_remaining()
            minutes = int(staff_time // 60)
            seconds = int(staff_time % 60)
            staff_text = self.font_manager.render_text(f"Staff Active: {minutes}:{seconds:02d}", 'small', GOLD)
            self.screen.blit(staff_text, (10, 120))
            
            # Staff usage hint
            hint_text = self.font_manager.render_text("Press W to shoot divine energy!", 'tiny', WHITE)
            self.screen.blit(hint_text, (10, 140))
        
        # Show staff status
        if self.player and hasattr(self.player, 'staff_active') and self.player.staff_active:
            staff_time = self.player.get_staff_time_remaining()
            minutes = int(staff_time // 60)
            seconds = int(staff_time % 60)
            staff_text = self.font_manager.render_text(f"Staff Active: {minutes}:{seconds:02d}", 'small', GOLD)
            self.screen.blit(staff_text, (10, 120))
            
            # Staff usage hint
            hint_text = self.font_manager.render_text("Press W to shoot divine energy!", 'tiny', WHITE)
            self.screen.blit(hint_text, (10, 140))# Show stone throw mode indicator
        if self.stone_throw_mode:
            stone_text = self.font_manager.render_text("🎯 STONE READY - Click on enemy to throw!", 'medium', GOLD)
            stone_rect = stone_text.get_rect(center=(SCREEN_WIDTH//2, 50))
            self.screen.blit(stone_text, stone_rect)
                
        # FPS Counter - Only show when toggled with F1
        if hasattr(self, 'show_fps') and self.show_fps and hasattr(self, 'clock'):
            fps = self.clock.get_fps()
            if fps > 0:  # Avoid division by zero
                fps_text = self.font_manager.get_font('small').render(f"FPS: {fps:.1f}", True, (255, 255, 255))
                self.screen.blit(fps_text, (10, 10))
                
                # Performance warning
                if fps < 30:
                    warning_text = self.font_manager.get_font('small').render("Low FPS - Consider reducing quality", True, (255, 255, 0))
                    self.screen.blit(warning_text, (10, 35))
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
        # Render multi-level platforms
        if hasattr(self, 'platforms'):
            for platform in self.platforms:
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                pygame.draw.rect(self.screen, (128, 128, 128), platform_rect)  # Gray platforms
                pygame.draw.rect(self.screen, (100, 100, 100), platform_rect, 2)  # Dark border

        # Render multi-level platforms
        if hasattr(self, 'platforms'):
            for platform in self.platforms:
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                pygame.draw.rect(self.screen, (128, 128, 128), platform_rect)  # Gray platforms
                pygame.draw.rect(self.screen, (100, 100, 100), platform_rect, 2)  # Dark border

        """Render the main game with proper background"""
        # Clear screen first
        self.screen.fill(BLACK)
        
        # Apply camera offset
        camera_offset = self.camera.get_offset()
        
        # Render background first (this should show the palace)
        self.level_manager.render_background(self.screen, camera_offset)
        
        # Render level elements (platforms, items, NPCs)
        self.level_manager.render(self.screen, camera_offset)

        # Render FIXED ground that stays at bottom of screen
        self.render_fixed_ground(camera_offset)
        
        # Render multi-level platforms
        self.render_platforms(camera_offset)
                
        # Render player on top
        if self.player:
            self.player.render(self.screen, camera_offset)
            
            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)
        
        # Render UI on top of everything
        
        # Render ITEM feedback messages only (disappear after 1.5 seconds)
        if hasattr(self, 'item_feedback_messages') and self.item_feedback_messages:
            import pygame
            for i, message in enumerate(self.item_feedback_messages):
                text_surface = self.font_manager.get_font('medium').render(message['text'], True, message['color'])
                
                # Position item feedback at top-right corner (away from dialogue)
                text_rect = text_surface.get_rect()
                text_rect.right = SCREEN_WIDTH - 20
                text_rect.y = 20 + (i * 35)  # Stack messages with 35px spacing
                
                # Add background for better visibility
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
                pygame.draw.rect(self.screen, message['color'], bg_rect, 2)
                
                self.screen.blit(text_surface, text_rect)
        
        # Legacy consumption text support (for backward compatibility)
        elif hasattr(self, 'consumption_text') and self.consumption_text and hasattr(self, 'consumption_text_timer') and self.consumption_text_timer > 0:
            import pygame
            text_surface = self.font_manager.get_font('medium').render(self.consumption_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = 50
            
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
            
            self.screen.blit(text_surface, text_rect)
        
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
            
            # Stone throw mode indicator
            if hasattr(self, 'stone_throw_mode') and self.stone_throw_mode:
                stone_ready_text = self.font_manager.render_text("🎯 STONE READY! Press A to throw", 'small', (255, 255, 0))
                self.screen.blit(stone_ready_text, (120, 40))
                # Add debug info
                can_attack_text = self.font_manager.render_text(f"Can attack: {self.player.can_attack}", 'tiny', (255, 255, 255))
                self.screen.blit(can_attack_text, (120, 60))
            # Healing ready indicator
            elif hasattr(self, 'healing_ready') and self.healing_ready:
                healing_text = self.font_manager.render_text(f"🩹 HEALING READY! Press H to heal +{self.healing_amount}", 'small', (0, 255, 0))
                self.screen.blit(healing_text, (120, 40))
                # Add blinking effect for better visibility
                import time
                if int(time.time() * 2) % 2:  # Blink every 0.5 seconds
                    healing_bg = pygame.Surface((400, 25))
                    healing_bg.set_alpha(50)
                    healing_bg.fill((0, 255, 0))
                    self.screen.blit(healing_bg, (115, 38))
            else:
                # Inventory instructions
                inventory_text = self.font_manager.render_text("Press I for inventory, use number keys for items", 'tiny', (240, 240, 240))
                self.screen.blit(inventory_text, (10, 115))
            
            # Debug: Show player position and movement limits
            # pos_text = self.font_manager.render_text(f"Moses: X={self.player.rect.x}, Y={self.player.rect.y}", 'tiny', WHITE)
            # self.screen.blit(pos_text, (10, 90))
            
            # limit_text = self.font_manager.render_text(f"Movement Limit: {SCREEN_WIDTH * 5} pixels", 'tiny', WHITE)
            # self.screen.blit(limit_text, (10, 110))
        
        # Current location
        # location_name = self.level_manager.current_location.value.replace('_', ' ').title()
        # location_text = self.font_manager.render_text(f"Location: {location_name}", 'small', WHITE)
        # self.screen.blit(location_text, (10, 40))
        
        # Moral standing
        moral_standing = self.moral_system.get_moral_standing()
        moral_color = self.moral_system.get_moral_color()
        moral_text = self.font_manager.render_text(f"Standing: {moral_standing}", 'small', moral_color)
        self.screen.blit(moral_text, (10, 65))
        
        # Instructions with movement reminder
        instruction_text = self.font_manager.render_text("Arrow Keys: Move Moses | E: Interact | I: Inventory | ESC: Pause", 'tiny', WHITE)
        self.screen.blit(instruction_text, (10, SCREEN_HEIGHT - 30))
        
        # Game state indicator
        # state_text = self.font_manager.render_text(f"State: {self.state.value}", 'tiny', GREEN)
        # self.screen.blit(state_text, (10, 115))
        
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
    
    def render_scripture_dialogue(self):
        """Render scripture dialogue overlay"""
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Scripture box
        box_width = SCREEN_WIDTH - 100
        box_height = 200
        box_x = 50
        box_y = SCREEN_HEIGHT // 2 - box_height // 2
        
        # Draw scripture box
        pygame.draw.rect(self.screen, WHITE, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, GOLD, (box_x, box_y, box_width, box_height), 3)
        
        # Title
        title_text = self.font_manager.render_text("📜 Sacred Scripture", 'medium', GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, box_y + 30))
        self.screen.blit(title_text, title_rect)
        
        # Scripture text (word wrap)
        if hasattr(self, 'current_scripture'):
            words = self.current_scripture.split(' ')
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.font_manager.render_text(test_line, 'small', BLACK)
                if test_surface.get_width() < box_width - 40:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Render lines
            y_offset = box_y + 70
            for line in lines:
                line_surface = self.font_manager.render_text(line, 'small', BLACK)
                line_rect = line_surface.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                self.screen.blit(line_surface, line_rect)
                y_offset += 25
        
        # Close instruction
        close_text = self.font_manager.render_text("Press any key to close", 'tiny', GRAY)
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH//2, box_y + box_height - 20))
        self.screen.blit(close_text, close_rect)
    
    def render_game_over_screen(self):
        """Render game over screen with dialog options"""
        # Semi-transparent red overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        # Game over dialog box
        dialog_width = 500
        dialog_height = 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background
        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill(BLACK)
        pygame.draw.rect(dialog_surface, WHITE, dialog_surface.get_rect(), 3)
        self.screen.blit(dialog_surface, (dialog_x, dialog_y))
        
        # Game over title
        game_over_text = self.font_manager.render_text("Moses Has Fallen!", 'large', RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Subtitle
        subtitle_text = self.font_manager.render_text("The journey ends here...", 'medium', WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Options
        restart_text = self.font_manager.render_text("Press SPACE to Restart Journey", 'medium', GOLD)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 160))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_manager.render_text("Press ESC to Return to Main Menu", 'medium', LIGHT_GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 190))
        self.screen.blit(menu_text, menu_rect)
        
        quit_text = self.font_manager.render_text("Press Q to Quit Game", 'small', GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 230))
        self.screen.blit(quit_text, quit_rect)


    def render_platforms(self, camera_offset):
        """OPTIMIZED: Render platforms with better performance"""
        if not hasattr(self, 'game_platforms'):
            return
        
        import pygame
        
        # OPTIMIZATION: Pre-calculate screen bounds for culling
        left_bound = -50
        right_bound = SCREEN_WIDTH + 50
        top_bound = -50
        bottom_bound = SCREEN_HEIGHT + 50
        
        for platform in self.game_platforms:
            # Calculate screen position
            screen_x = platform['x'] - camera_offset[0]
            screen_y = platform['y'] - camera_offset[1]
            
            # OPTIMIZED: Early culling check
            if not (left_bound <= screen_x <= right_bound and top_bound <= screen_y <= bottom_bound):
                continue
            
            # Create platform rectangle
            platform_rect = pygame.Rect(screen_x, screen_y, platform['width'], platform['height'])
            
            # OPTIMIZED: Simplified rendering for better performance
            pygame.draw.rect(self.screen, (139, 69, 19), platform_rect)    # Brown stone
            pygame.draw.rect(self.screen, (101, 67, 33), platform_rect, 2) # Border (reduced thickness)
            
            # OPTIMIZED: Reduced texture details for better FPS
            if platform['width'] > 60:  # Only add details to larger platforms
                pygame.draw.rect(self.screen, (160, 82, 45), (screen_x + 2, screen_y + 2, platform['width'] - 4, 3))


    def render_fixed_ground(self, camera_offset):
        """Render ground that stays FIXED at bottom of screen"""
        import pygame
        
        # Ground dimensions
        ground_height = 50
        ground_width = SCREEN_WIDTH * 6  # Extended ground width
        
        # FIXED: Ground Y position always at bottom of screen
        ground_y = SCREEN_HEIGHT - ground_height
        
        # Ground X position follows camera horizontally only
        ground_x = -camera_offset[0]
        
        # Create ground rectangle
        ground_rect = pygame.Rect(ground_x, ground_y, ground_width, ground_height)
        
        # Draw ground with brown stone color (matching platforms)
        pygame.draw.rect(self.screen, (139, 69, 19), ground_rect)    # Brown stone
        pygame.draw.rect(self.screen, (101, 67, 33), ground_rect, 3) # Dark brown border
        
        # Add ground texture
        for x in range(ground_x, ground_x + ground_width, 20):
            if 0 <= x <= SCREEN_WIDTH:  # Only draw visible texture
                pygame.draw.line(self.screen, (120, 60, 15), 
                               (x, ground_y + 5), (x, ground_y + ground_height - 5))


    def show_consumption_text(self, text):
        """Show consumption text that disappears after 1 second"""
        self.consumption_text = text
        self.consumption_text_timer = self.consumption_text_duration
        print(text)  # Also print to console for debugging


    def show_feedback_message(self, text, message_type="info", color=(255, 255, 255)):
        """Show a feedback message that disappears after 1.5 seconds"""
        if not hasattr(self, 'feedback_messages'):
            self.feedback_messages = []
        
        message = {
            'text': text,
            'timer': self.feedback_duration,
            'type': message_type,
            'color': color,
            'y_offset': len(self.feedback_messages) * 30  # Stack messages vertically
        }
        
        self.feedback_messages.append(message)
        print(text)  # Also print to console for debugging
    
    def show_item_collection_message(self, item_name, item_type):
        """Show item collection feedback message"""
        emoji_map = {
            'stone': '🪨',
            'water': '💧',
            'bread': '🍞',
            'meat': '🥩',
            'scroll': '📜',
            'armor_of_god': '🛡️',
            'staff': '🪄'
        }
        
        emoji = emoji_map.get(item_type, '📦')
        message = f"{emoji} Collected {item_name}!"
        self.show_feedback_message(message, "collection", (0, 255, 0))  # Green for collection
    
    def show_item_usage_message(self, item_name, effect):
        """Show item usage feedback message"""
        message = f"✨ Used {item_name}! {effect}"
        self.show_feedback_message(message, "usage", (255, 255, 0))  # Yellow for usage
    
    def show_combat_message(self, message):
        """Show combat feedback message"""
        self.show_feedback_message(message, "combat", (255, 100, 100))  # Red for combat
    
    def show_interaction_message(self, message):
        """Show interaction feedback message"""
        self.show_feedback_message(message, "interaction", (100, 200, 255))  # Blue for interaction
    
    def show_system_message(self, message):
        """Show system feedback message"""
        self.show_feedback_message(message, "system", (200, 200, 200))  # Gray for system


    
    def show_item_collection_feedback(self, item_name, item_type):
        """Show item collection feedback (green, 1.5 seconds)"""
        emoji_map = {
            'stone': '🪨',
            'water': '💧', 
            'bread': '🍞',
            'meat': '🥩',
            'scroll': '📜',
            'armor_of_god': '🛡️',
            'staff': '🪄'
        }
        
        emoji = emoji_map.get(item_type, '📦')
        message = f"{emoji} Collected {item_name}!"
        self.show_item_feedback(message, (0, 255, 0))  # Green for collection
    
    def show_item_usage_feedback(self, item_name, effect):
        """Show item usage feedback (yellow, 1.5 seconds)"""
        message = f"✨ Used {item_name}! {effect}"
        self.show_item_feedback(message, (255, 255, 0))  # Yellow for usage

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
