import pygame
import random
import math
import os
from enum import Enum
from typing import Dict, List, Tuple, Optional

# Import constants from main game
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Game states and locations
class Location:
    PALACE = "palace"
    EGYPT_CITY = "egypt_city"
    DESERT = "desert"
    RED_SEA = "red_sea"
    WILDERNESS = "wilderness"
    MOUNT_SINAI = "mount_sinai"
    JERUSALEM = "jerusalem"
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

class Location(Enum):
    PALACE = "palace"
    EGYPT_CITY = "egypt_city"
    DESERT = "desert"
    RED_SEA = "red_sea"
    WILDERNESS = "wilderness"
    MOUNT_SINAI = "mount_sinai"
    JERUSALEM = "jerusalem"

class Player:
    def __init__(self, x, y, sprites):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True  # Start on ground
        self.health = 100
        self.max_health = 100
        self.facing_right = True
        
        # Animation
        self.sprites = sprites
        self.current_sprite = 'idle'
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        
        # Movement and interaction states
        self.is_walking = False
        self.is_jumping = False
        self.is_interacting = False
        self.interaction_timer = 0
        
        # Enhanced movement tracking for smart sound system
        self.movement_start_time = 0
        self.continuous_walk_threshold = 0.5  # Seconds before switching to continuous walk
        self.last_movement_time = 0
        self.movement_timer = 0
        self.was_walking_last_frame = False
        
        # Position Moses properly on the ground
        self.rect.bottom = SCREEN_HEIGHT - 50
        
    def update(self, dt):
        """Update player state with enhanced physics and smart sound system"""
        keys = pygame.key.get_pressed()
        
        # Handle interaction state
        if self.is_interacting:
            self.interaction_timer -= dt
            if self.interaction_timer <= 0:
                self.is_interacting = False
        
        # Track movement timing
        current_time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
        
        # Horizontal movement with smart sound system
        old_velocity_x = self.velocity_x
        self.velocity_x = 0
        self.is_walking = False
        
        if keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
            self.is_walking = True
        if keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
            self.is_walking = True
        
        # Smart walking sound system with realistic timing
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            if self.is_walking:
                if not self.was_walking_last_frame:
                    # Just started walking
                    self.movement_start_time = current_time
                    self.sound_manager.play_single_step()  # Play single step sound
                    print("🦶 Started walking - single step")
                elif current_time - self.movement_start_time >= self.continuous_walk_threshold:
                    # Been walking for a while, switch to timed continuous walking
                    if not self.sound_manager.is_walking_continuously:
                        self.sound_manager.start_continuous_walking()
                        print("🚶 Switched to realistic continuous walking (timed steps)")
            else:
                if self.was_walking_last_frame:
                    # Just stopped walking
                    self.sound_manager.stop_movement_sounds()
                    print("🛑 Stopped walking")
        
        # Update walking state for next frame
        self.was_walking_last_frame = self.is_walking
        
        # Jumping with sound effect - check BEFORE gravity is applied
        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.is_jumping = True
            print(f"🦘 Moses jumping from y={self.rect.y}")
            # Play jump sound if sound manager is available
            if hasattr(self, 'sound_manager') and self.sound_manager:
                self.sound_manager.play_jump_sound()
        
        # Alternative jump key (SPACE)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
            self.is_jumping = True
            print(f"🦘 Moses jumping with SPACE from y={self.rect.y}")
            if hasattr(self, 'sound_manager') and self.sound_manager:
                self.sound_manager.play_jump_sound()
        
        # IMPROVED GRAVITY SYSTEM
        # Always apply gravity when not on ground
        if not self.on_ground:
            self.velocity_y += GRAVITY
            # Terminal velocity to prevent infinite acceleration
            if self.velocity_y > 15:
                self.velocity_y = 15
        
        # Store old position for collision detection
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Update horizontal position
        self.rect.x += self.velocity_x
        
        # Update vertical position
        self.rect.y += self.velocity_y
        
        # Debug: Print movement info occasionally
        if self.velocity_x != 0 and int(old_x) % 50 == 0:
            print(f"Moses moving: x={self.rect.x}, y={self.rect.y}, on_ground={self.on_ground}")
        
        # Debug: Print falling info
        if not self.on_ground and self.velocity_y > 0:
            if int(old_y) % 20 == 0:  # Print every 20 pixels of falling
                print(f"🪂 Moses falling: y={self.rect.y}, velocity_y={self.velocity_y}")
        
        # Update animation based on state
        self.update_animation_state()
        self.update_animation(dt)
        
        # Ground collision - ensure player stays on the ground platform
        ground_level = SCREEN_HEIGHT - 50  # Top of ground platform
        if self.rect.bottom >= ground_level:
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.on_ground = True
            self.is_jumping = False
        
        # Keep player within reasonable bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH * 5:
            self.rect.right = SCREEN_WIDTH * 5
        
        # Reset ground state (will be set by collision detection)
        if self.velocity_y > 0:
            self.on_ground = False
    
    def update_animation_state(self):
        """Update current sprite based on player state"""
        if self.is_interacting:
            self.current_sprite = 'interact'
        elif self.is_jumping or not self.on_ground:
            self.current_sprite = 'jump'
        elif self.is_walking:
            self.current_sprite = 'walk'
        else:
            self.current_sprite = 'idle'
    
    def start_interaction(self):
        """Start interaction animation"""
        self.is_interacting = True
        self.interaction_timer = 0.5  # Half second interaction pose
    
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for audio effects"""
        self.sound_manager = sound_manager
    
    def update_animation(self, dt):
        """Update animation frames"""
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            
            if self.is_jumping:
                self.current_sprite = 'jump'
            elif self.is_walking:
                self.current_sprite = 'walk'
                self.animation_frame = (self.animation_frame + 1) % 4
            else:
                self.current_sprite = 'idle'
                self.animation_frame = 0
    
    def take_damage(self, damage):
        """Take damage and check for game over"""
        self.health = max(0, self.health - damage)
        return self.health <= 0
    
    def heal(self, amount):
        """Heal the player"""
        self.health = min(self.max_health, self.health + amount)
    
    def render(self, screen, camera_offset):
        """Render the player with enhanced sprite animations"""
        render_rect = self.rect.copy()
        render_rect.x -= camera_offset[0]
        render_rect.y -= camera_offset[1]
        
        # Get current sprite based on state
        sprite = None
        if self.sprites:
            if self.is_interacting and 'interact' in self.sprites:
                sprite = self.sprites['interact']
            elif self.is_jumping and 'jump' in self.sprites:
                sprite = self.sprites['jump']
            elif self.is_walking and 'walk' in self.sprites:
                if isinstance(self.sprites['walk'], list) and len(self.sprites['walk']) > self.animation_frame:
                    sprite = self.sprites['walk'][self.animation_frame]
                elif 'walk' in self.sprites:
                    sprite = self.sprites['walk']
            elif 'idle' in self.sprites:
                sprite = self.sprites['idle']
        
        if sprite:
            # Flip sprite if facing left
            if not self.facing_right:
                sprite = pygame.transform.flip(sprite, True, False)
            screen.blit(sprite, render_rect)
        else:
            # Enhanced fallback with animation indication
            if self.is_interacting:
                color = (255, 215, 0)  # Gold for interaction
            elif self.is_jumping:
                color = (0, 255, 0)    # Green for jumping
            elif self.is_walking:
                color = (0, 100, 255)  # Blue for walking
            else:
                color = (70, 130, 180) # Default blue
            
            pygame.draw.rect(screen, color, render_rect)
            # Add a white border to make Moses stand out
            pygame.draw.rect(screen, WHITE, render_rect, 3)
            
            # Add simple directional indicator
            if self.facing_right:
                pygame.draw.polygon(screen, WHITE, [
                    (render_rect.right - 5, render_rect.centery - 3),
                    (render_rect.right - 5, render_rect.centery + 3),
                    (render_rect.right - 2, render_rect.centery)
                ])
            else:
                pygame.draw.polygon(screen, WHITE, [
                    (render_rect.left + 5, render_rect.centery - 3),
                    (render_rect.left + 5, render_rect.centery + 3),
                    (render_rect.left + 2, render_rect.centery)
                ])

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.smoothing = 0.15  # Increased smoothing for better Mario Bros feel
    
    def follow_player(self, player):
        """Mario Bros style camera following"""
        # Follow player horizontally with smooth movement
        self.target_x = player.rect.centerx - SCREEN_WIDTH // 2
        self.target_y = 0  # Keep camera at a fixed vertical position for side-scrolling
        
        # Smooth horizontal camera movement
        self.x += (self.target_x - self.x) * self.smoothing
        self.y = 0  # Lock vertical camera position
        
        # Keep camera bounds reasonable for extended palace
        self.x = max(0, min(self.x, SCREEN_WIDTH * 4))  # Allow camera to follow across the full palace
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return (int(self.x), int(self.y))

class Platform:
    def __init__(self, x, y, width, height, platform_type="stone"):
        self.rect = pygame.Rect(x, y, width, height)
        self.platform_type = platform_type

class ItemPickup:
    def __init__(self, x, y, item_type, sprites=None):
        self.rect = pygame.Rect(x, y, 24, 24)
        self.item_type = item_type
        self.sprites = sprites
        self.bob_offset = 0
        self.bob_speed = 2
    
    def update(self, dt):
        """Update item animation (bobbing effect)"""
        self.bob_offset += self.bob_speed * dt
    
    def render(self, screen, camera_offset):
        render_rect = self.rect.copy()
        render_rect.x -= camera_offset[0]
        render_rect.y -= camera_offset[1] + int(math.sin(self.bob_offset) * 3)
        
        # Get sprite
        sprite = None
        if self.sprites and 'items' in self.sprites:
            sprite = self.sprites['items'].get(self.item_type)
        
        if sprite:
            screen.blit(sprite, render_rect)
        else:
            # Fallback colors
            colors = {
                "stone": GRAY,
                "meat": BROWN,
                "water": BLUE,
                "armor_of_god": GOLD,
                "staff": BROWN,
                "bread": (210, 180, 140),
                "scroll": (245, 245, 220)
            }
            color = colors.get(self.item_type, WHITE)
            pygame.draw.rect(screen, color, render_rect)

class NPC:
    def __init__(self, x, y, npc_type, dialogue_id, sprites=None):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.interaction_rect = pygame.Rect(x - 20, y - 20, 72, 88)
        self.npc_type = npc_type
        self.dialogue_id = dialogue_id
        self.sprites = sprites
        self.facing_right = True
        
        # Don't auto-position here - let the level creation handle it
    
    def update(self, dt):
        """Update NPC state"""
        pass
    
    def render(self, screen, camera_offset):
        """Render NPC with maximum visibility and interaction prompts"""
        render_rect = self.rect.copy()
        render_rect.x -= camera_offset[0]
        render_rect.y -= camera_offset[1]
        
        # Always render NPCs if they're anywhere near the screen
        if render_rect.right > -100 and render_rect.left < SCREEN_WIDTH + 100:
            # Get sprite
            sprite = None
            if self.sprites and 'npcs' in self.sprites:
                sprite = self.sprites['npcs'].get(self.npc_type)
            
            if sprite:
                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, render_rect)
                
                # Add bright outline to make sprite more visible
                pygame.draw.rect(screen, (255, 255, 0), render_rect, 3)  # Yellow outline
            else:
                # ENHANCED fallback with maximum visibility
                colors = {
                    "palace_guard": (255, 0, 0),        # Bright Red
                    "egyptian_citizen": (255, 255, 255), # White
                    "hebrew_slave": (139, 69, 19),      # Brown
                    "priest": (255, 215, 0),            # Gold
                    "royal_servant": (0, 191, 255),     # Deep Sky Blue
                    "taskmaster": (220, 20, 60),        # Crimson
                }
                color = colors.get(self.npc_type, (255, 0, 255))  # Magenta fallback
                
                # Draw main body with bright colors
                pygame.draw.rect(screen, color, render_rect)
                pygame.draw.rect(screen, (0, 0, 0), render_rect, 4)  # Thick black border
                
                # Add character details for better identification
                # Head
                pygame.draw.circle(screen, (255, 255, 255), (render_rect.centerx, render_rect.top + 12), 8)
                pygame.draw.circle(screen, (0, 0, 0), (render_rect.centerx, render_rect.top + 12), 8, 2)
            
            # ALWAYS show NPC type label for debugging
            font = pygame.font.Font(None, 20)
            label_text = font.render(self.npc_type.replace('_', ' ').title(), True, (255, 255, 255))
            label_bg = pygame.Rect(render_rect.centerx - 40, render_rect.top - 25, 80, 20)
            pygame.draw.rect(screen, (0, 0, 0), label_bg)
            pygame.draw.rect(screen, (255, 255, 0), label_bg, 2)
            screen.blit(label_text, (label_bg.left + 5, label_bg.top + 2))
            
            # Show interaction prompt if player is nearby
            if hasattr(self, 'showing_prompt') and self.showing_prompt:
                prompt_font = pygame.font.Font(None, 24)
                prompt_text = prompt_font.render("Press E to Interact", True, (255, 255, 0))
                prompt_bg = pygame.Rect(render_rect.centerx - 60, render_rect.bottom + 5, 120, 25)
                pygame.draw.rect(screen, (0, 0, 0), prompt_bg)
                pygame.draw.rect(screen, (255, 255, 0), prompt_bg, 2)
                screen.blit(prompt_text, (prompt_bg.left + 5, prompt_bg.top + 3))
            
            # Show position for debugging
            pos_font = pygame.font.Font(None, 16)
            pos_text = pos_font.render(f"({self.rect.x},{self.rect.y})", True, (255, 255, 255))
            screen.blit(pos_text, (render_rect.left, render_rect.bottom + 30))
    
    def can_interact_with(self, player):
            # ENHANCED interaction indicator - much more visible
            indicator_y = render_rect.top - 25
            # Large white background
            pygame.draw.circle(screen, (255, 255, 255), (render_rect.centerx, indicator_y), 15)
            # Green inner circle
            pygame.draw.circle(screen, (0, 255, 0), (render_rect.centerx, indicator_y), 12)
            # Black border
            pygame.draw.circle(screen, (0, 0, 0), (render_rect.centerx, indicator_y), 15, 3)
            
            # Large "E" for interact
            font = pygame.font.Font(None, 24)
            e_text = font.render("E", True, (0, 0, 0))
            e_rect = e_text.get_rect(center=(render_rect.centerx, indicator_y))
            screen.blit(e_text, e_rect)
            
            # NPC name label - always visible
            name_font = pygame.font.Font(None, 20)
            npc_name = self.npc_type.replace('_', ' ').title()
            name_text = name_font.render(npc_name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(render_rect.centerx, indicator_y - 30))
            
            # Background for name text
            name_bg = pygame.Rect(name_rect.left - 4, name_rect.top - 2, name_rect.width + 8, name_rect.height + 4)
            pygame.draw.rect(screen, (0, 0, 0), name_bg)
            pygame.draw.rect(screen, (255, 255, 255), name_bg, 2)
            screen.blit(name_text, name_rect)
            
            # Debug: Show NPC position
            debug_font = pygame.font.Font(None, 16)
            pos_text = debug_font.render(f"({self.rect.x}, {self.rect.y})", True, (255, 255, 0))
            screen.blit(pos_text, (render_rect.left, render_rect.bottom + 5))

class Enemy:
    def __init__(self, x, y, enemy_type, sprites=None):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.enemy_type = enemy_type
        self.sprites = sprites
        self.health = 30
        self.defeated = False
        self.velocity_x = random.choice([-1, 1])
        self.patrol_distance = 100
        self.start_x = x
        self.facing_right = self.velocity_x > 0
        
        # Position enemy at the same ground level as Moses
        self.rect.bottom = SCREEN_HEIGHT - 50
    
    def update(self, dt):
        """Update enemy AI"""
        if self.defeated:
            return
        
        # Simple patrol AI
        self.rect.x += self.velocity_x
        
        # Turn around at patrol limits
        if abs(self.rect.x - self.start_x) > self.patrol_distance:
            self.velocity_x *= -1
            self.facing_right = self.velocity_x > 0
    
    def render(self, screen, camera_offset):
        if self.defeated:
            return
            
        render_rect = self.rect.copy()
        render_rect.x -= camera_offset[0]
        render_rect.y -= camera_offset[1]
        
        # Only render if on screen
        if render_rect.right > -50 and render_rect.left < SCREEN_WIDTH + 50:
            # Get sprite
            sprite = None
            if self.sprites and 'enemies' in self.sprites:
                sprite = self.sprites['enemies'].get(self.enemy_type)
            
            if sprite:
                if not self.facing_right:
                    sprite = pygame.transform.flip(sprite, True, False)
                screen.blit(sprite, render_rect)
            else:
                # Enhanced fallback with better visibility
                colors = {
                    "egyptian_soldier": (139, 0, 0),    # Dark Red
                    "wild_animal": (101, 67, 33)        # Dark Brown
                }
                color = colors.get(self.enemy_type, (139, 0, 0))
                pygame.draw.rect(screen, color, render_rect)
                pygame.draw.rect(screen, BLACK, render_rect, 3)  # Thick border
                
                # Add simple enemy indicator
                pygame.draw.circle(screen, RED, (render_rect.centerx, render_rect.top + 8), 4)
                
                # Add directional indicator
                if self.facing_right:
                    pygame.draw.polygon(screen, WHITE, [
                        (render_rect.right - 5, render_rect.centery - 2),
                        (render_rect.right - 5, render_rect.centery + 2),
                        (render_rect.right - 2, render_rect.centery)
                    ])
                else:
                    pygame.draw.polygon(screen, WHITE, [
                        (render_rect.left + 5, render_rect.centery - 2),
                        (render_rect.left + 5, render_rect.centery + 2),
                        (render_rect.left + 2, render_rect.centery)
                    ])

class ExitZone:
    def __init__(self, x, y, width, height, destination):
        self.rect = pygame.Rect(x, y, width, height)
        self.destination = destination

class LevelManager:
    def __init__(self):
        self.current_location = Location.PALACE
        self.platforms = []
        self.items = []
        self.npcs = []
        self.enemies = []
        self.exit_zones = []
        self.background = None
    
    def load_level(self, location, sprites):
        """Load a specific level"""
        self.current_location = location
        
        # Clear existing level data
        self.platforms.clear()
        self.items.clear()
        self.npcs.clear()
        self.enemies.clear()
        self.exit_zones.clear()
        
        # Load background
        if sprites and 'backgrounds' in sprites:
            self.background = sprites['backgrounds'].get(location)
        
        # Create level based on location
        if location == Location.PALACE or location == "palace" or str(location) == "Location.PALACE":
            self.create_palace_level(sprites)
        elif location == Location.EGYPT_CITY or location == "egypt_city":
            self.create_egypt_city_level(sprites)
        elif location == Location.DESERT:
            self.create_desert_level(sprites)
        elif location == Location.RED_SEA:
            self.create_red_sea_level(sprites)
        elif location == Location.WILDERNESS:
            self.create_wilderness_level(sprites)
        elif location == Location.MOUNT_SINAI:
            self.create_mount_sinai_level(sprites)
        elif location == Location.JERUSALEM:
            self.create_jerusalem_level(sprites)
    
    def create_palace_level(self, sprites):
        """Create the palace level with NPCs positioned at Moses' EXACT Y level"""
        # Extended ground platform
        ground_y = SCREEN_HEIGHT - 50  # 718
        self.platforms.append(Platform(0, ground_y, SCREEN_WIDTH * 8, 50))  # Extended for more NPCs
        
        # Elevated platforms for jumping puzzles - positioned to not interfere with ground movement
        self.platforms.append(Platform(300, SCREEN_HEIGHT - 150, 150, 20))   # After first NPC
        self.platforms.append(Platform(600, SCREEN_HEIGHT - 250, 150, 20))   # Between NPCs
        self.platforms.append(Platform(900, SCREEN_HEIGHT - 180, 150, 20))   # After second NPC
        self.platforms.append(Platform(1300, SCREEN_HEIGHT - 220, 150, 20))  # Mid-level
        self.platforms.append(Platform(1700, SCREEN_HEIGHT - 160, 150, 20))  # After priest
        self.platforms.append(Platform(2100, SCREEN_HEIGHT - 200, 150, 20))  # Between NPCs
        self.platforms.append(Platform(2500, SCREEN_HEIGHT - 140, 150, 20))  # After checkpoint
        self.platforms.append(Platform(2900, SCREEN_HEIGHT - 190, 150, 20))  # Near end
        self.platforms.append(Platform(3300, SCREEN_HEIGHT - 170, 150, 20))  # Final platform
        
        # Items positioned strategically near NPCs
        self.items.append(ItemPickup(250, SCREEN_HEIGHT - 180, "stone", sprites))
        self.items.append(ItemPickup(550, SCREEN_HEIGHT - 280, "water", sprites))
        self.items.append(ItemPickup(850, SCREEN_HEIGHT - 210, "bread", sprites))
        self.items.append(ItemPickup(1250, SCREEN_HEIGHT - 250, "scroll", sprites))
        self.items.append(ItemPickup(1650, SCREEN_HEIGHT - 190, "meat", sprites))
        self.items.append(ItemPickup(2050, SCREEN_HEIGHT - 230, "armor_of_god", sprites))
        self.items.append(ItemPickup(2450, SCREEN_HEIGHT - 170, "staff", sprites))
        self.items.append(ItemPickup(2850, SCREEN_HEIGHT - 220, "bread", sprites))
        self.items.append(ItemPickup(3250, SCREEN_HEIGHT - 200, "water", sprites))
        
        # CRITICAL FIX: Moses Y position calculation
        # Moses rect: x=150, y=670, bottom=718
        # So NPCs should be at y=670 to match Moses exactly
        moses_ground_y = 670  # Exact Y position where Moses stands
        
        # STRATEGIC NPC PLACEMENT - All at Moses' exact Y level for visibility
        
        # NPC 1: Palace Guard at x=400 (early encounter) - CLOSE TO STARTING POSITION
        npc1 = NPC(400, moses_ground_y, "palace_guard", "guard_dialogue", sprites)
        self.npcs.append(npc1)
        
        # NPC 2: Hebrew Slave at x=800 (after first platform)
        npc2 = NPC(800, moses_ground_y, "hebrew_slave", "slave_dialogue", sprites)
        self.npcs.append(npc2)
        
        # NPC 3: Egyptian Citizen at x=1200 (mid-level)
        npc3 = NPC(1200, moses_ground_y, "egyptian_citizen", "citizen_dialogue", sprites)
        self.npcs.append(npc3)
        
        # NPC 4: Priest at x=1600 (spiritual encounter)
        npc4 = NPC(1600, moses_ground_y, "priest", "priest_dialogue", sprites)
        self.npcs.append(npc4)
        
        # NPC 5: Another Hebrew Slave at x=2000 (resistance member)
        npc5 = NPC(2000, moses_ground_y, "hebrew_slave", "resistance_dialogue", sprites)
        self.npcs.append(npc5)
        
        # NPC 6: Palace Guard at x=2400 (checkpoint)
        npc6 = NPC(2400, moses_ground_y, "palace_guard", "checkpoint_dialogue", sprites)
        self.npcs.append(npc6)
        
        # NPC 7: Egyptian Citizen at x=2800 (informant)
        npc7 = NPC(2800, moses_ground_y, "egyptian_citizen", "informant_dialogue", sprites)
        self.npcs.append(npc7)
        
        # NPC 8: Final Priest at x=3200 (wisdom giver)
        npc8 = NPC(3200, moses_ground_y, "priest", "wisdom_dialogue", sprites)
        self.npcs.append(npc8)
        
        # ADD EXTRA CLOSE NPCs for immediate testing
        # NPC 9: Very close Palace Guard at x=300 (right after Moses starts)
        npc9 = NPC(300, moses_ground_y, "palace_guard", "guard_dialogue", sprites)
        self.npcs.append(npc9)
        
        # NPC 10: Hebrew Slave at x=500 (easy to reach)
        npc10 = NPC(500, moses_ground_y, "hebrew_slave", "slave_dialogue", sprites)
        self.npcs.append(npc10)
        
        # Enemies positioned between NPCs for challenge
        self.enemies.append(Enemy(600, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(1000, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(1400, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(1800, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(2200, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(2600, moses_ground_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(3000, moses_ground_y, "egyptian_soldier", sprites))
        
        # Exit to Egypt City at the far end
        self.exit_zones.append(ExitZone(SCREEN_WIDTH * 7.5, ground_y - 100, 100, 100, Location.EGYPT_CITY))
    
    def create_egypt_city_level(self, sprites):
        """Create Egypt city level with NPCs at Moses' level"""
        ground_y = SCREEN_HEIGHT - 50
        self.platforms.append(Platform(0, ground_y, SCREEN_WIDTH * 4, 50))
        
        # Building platforms - create a city-like environment
        building_heights = [120, 180, 140, 200, 160, 220, 180]
        for i, height in enumerate(building_heights):
            x = 200 + i * 250
            y = ground_y - height
            self.platforms.append(Platform(x, y, 180, 20))
            
            # Add items on some buildings
            if i % 2 == 0:
                item_types = ["meat", "stone", "scroll", "water"]
                item_type = item_types[i // 2 % len(item_types)]
                self.items.append(ItemPickup(x + 90, y - 30, item_type, sprites))
        
        # NPCs positioned at the same level as Moses
        npc_y = SCREEN_HEIGHT - 100  # Same as Moses' level
        
        # Egyptian City NPCs with authentic roles
        self.npcs.append(NPC(300, npc_y, "merchant", "merchant_dialogue", sprites))
        self.npcs.append(NPC(600, npc_y, "scribe", "scribe_dialogue", sprites))
        self.npcs.append(NPC(900, npc_y, "noble", "noble_dialogue", sprites))
        self.npcs.append(NPC(1200, npc_y, "overseer", "overseer_dialogue", sprites))
        self.npcs.append(NPC(1500, npc_y, "hebrew_slave", "city_slave_dialogue", sprites))
        self.npcs.append(NPC(1800, npc_y, "egyptian_citizen", "citizen_dialogue", sprites))
        
        # More challenging enemies at Moses' level
        enemy_y = SCREEN_HEIGHT - 100
        self.enemies.append(Enemy(500, enemy_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(1000, enemy_y, "egyptian_soldier", sprites))
        self.enemies.append(Enemy(1600, enemy_y, "egyptian_soldier", sprites))
        
        # Exit to Desert
        self.exit_zones.append(ExitZone(SCREEN_WIDTH * 3.5, ground_y - 150, 100, 100, Location.DESERT))
    
    def create_desert_level(self, sprites):
        """Create the desert level with NPCs at Moses' level"""
        # Sandy terrain with dunes
        ground_y = SCREEN_HEIGHT - 30
        self.platforms.append(Platform(0, ground_y, SCREEN_WIDTH * 5, 30))
        
        # Sand dunes as platforms
        dune_positions = [(300, SCREEN_HEIGHT - 80), (800, SCREEN_HEIGHT - 120), 
                         (1400, SCREEN_HEIGHT - 90), (2000, SCREEN_HEIGHT - 110)]
        
        for x, y in dune_positions:
            self.platforms.append(Platform(x, y, 200, 50))
        
        # Desert items
        self.items.append(ItemPickup(350, SCREEN_HEIGHT - 110, "water", sprites))
        self.items.append(ItemPickup(850, SCREEN_HEIGHT - 150, "meat", sprites))
        self.items.append(ItemPickup(1450, SCREEN_HEIGHT - 120, "staff", sprites))
        self.items.append(ItemPickup(2050, SCREEN_HEIGHT - 140, "bread", sprites))
        
        # Desert NPCs positioned at Moses' level (adjusted for desert ground)
        npc_y = SCREEN_HEIGHT - 78  # Adjusted for desert ground level
        
        self.npcs.append(NPC(500, npc_y, "bedouin", "bedouin_dialogue", sprites))
        self.npcs.append(NPC(1000, npc_y, "nomad", "nomad_dialogue", sprites))
        self.npcs.append(NPC(1600, npc_y, "desert_guide", "guide_dialogue", sprites))
        self.npcs.append(NPC(2200, npc_y, "hebrew_slave", "desert_encounter", sprites))
        
        # Wild animals and remaining soldiers at the same level
        enemy_y = SCREEN_HEIGHT - 78
        self.enemies.append(Enemy(600, enemy_y, "wild_animal", sprites))
        self.enemies.append(Enemy(1200, enemy_y, "wild_animal", sprites))
        self.enemies.append(Enemy(1800, enemy_y, "egyptian_soldier", sprites))
        
        # Exit to Red Sea
        self.exit_zones.append(ExitZone(SCREEN_WIDTH * 4.5, ground_y - 50, 100, 100, Location.RED_SEA))
    
    def create_red_sea_level(self, sprites):
        """Create the Red Sea level"""
        # Water level with special mechanics
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, 300, 50))  # Shore
        self.platforms.append(Platform(SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50, 300, 50))  # Other shore
        
        # Parted sea path (special platform)
        self.platforms.append(Platform(300, SCREEN_HEIGHT - 30, SCREEN_WIDTH - 600, 30))
        
        # Items
        self.items.append(ItemPickup(150, SCREEN_HEIGHT - 100, "armor_of_god", sprites))
        self.items.append(ItemPickup(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 100, "scroll", sprites))
        
        # Divine encounter
        self.npcs.append(NPC(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80, "priest", "divine_encounter", sprites))
        
        # Exit to Wilderness
        self.exit_zones.append(ExitZone(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 100, 100, Location.WILDERNESS))
    
    def create_wilderness_level(self, sprites):
        """Create the wilderness level"""
        # Rocky terrain
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH * 6, 50))
        
        # Rocky outcrops
        rock_positions = [(200, SCREEN_HEIGHT - 100), (600, SCREEN_HEIGHT - 150), 
                         (1200, SCREEN_HEIGHT - 120), (1800, SCREEN_HEIGHT - 180)]
        
        for x, y in rock_positions:
            self.platforms.append(Platform(x, y, 150, 50))
        
        # Wilderness items
        self.items.append(ItemPickup(250, SCREEN_HEIGHT - 130, "water", sprites))
        self.items.append(ItemPickup(650, SCREEN_HEIGHT - 180, "bread", sprites))
        self.items.append(ItemPickup(1250, SCREEN_HEIGHT - 150, "meat", sprites))
        
        # Wilderness encounters
        self.npcs.append(NPC(800, SCREEN_HEIGHT - 100, "hebrew_slave", "wilderness_dialogue", sprites))
        
        # More challenging enemies
        for i in range(4):
            x = 400 + i * 400
            self.enemies.append(Enemy(x, SCREEN_HEIGHT - 100, "wild_animal", sprites))
        
        # Exit to Mount Sinai
        self.exit_zones.append(ExitZone(SCREEN_WIDTH * 5.5, SCREEN_HEIGHT - 150, 100, 100, Location.MOUNT_SINAI))
    
    def create_mount_sinai_level(self, sprites):
        """Create Mount Sinai level"""
        # Mountain terrain
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH * 2, 50))
        
        # Mountain steps
        for i in range(8):
            x = 200 + i * 150
            y = SCREEN_HEIGHT - 100 - i * 40
            self.platforms.append(Platform(x, y, 120, 20))
        
        # Sacred items
        self.items.append(ItemPickup(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 400, "scroll", sprites))
        self.items.append(ItemPickup(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 400, "armor_of_god", sprites))
        
        # Divine encounter at the top
        self.npcs.append(NPC(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 420, "priest", "sinai_encounter", sprites))
        
        # Exit to Jerusalem
        self.exit_zones.append(ExitZone(SCREEN_WIDTH * 1.8, SCREEN_HEIGHT - 150, 100, 100, Location.JERUSALEM))
    
    def create_jerusalem_level(self, sprites):
        """Create Jerusalem level (final destination)"""
        # Holy city platforms
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH * 2, 50))
        
        # City structures
        for i in range(6):
            x = 100 + i * 200
            y = SCREEN_HEIGHT - 120 - (i % 2) * 60
            self.platforms.append(Platform(x, y, 150, 20))
        
        # Final rewards
        self.items.append(ItemPickup(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 200, "armor_of_god", sprites))
        
        # Final encounter
        self.npcs.append(NPC(SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100, "priest", "final_encounter", sprites))
    
    def update(self, dt):
        """Update level elements"""
        for item in self.items:
            item.update(dt)
        
        for npc in self.npcs:
            npc.update(dt)
        
        for enemy in self.enemies:
            enemy.update(dt)
    
    def render_background(self, screen, camera_offset):
        """Render scrolling background like Mario Bros"""
        if self.background:
            # Scale background to fit screen height
            bg_width = self.background.get_width()
            bg_height = self.background.get_height()
            
            # Scale to fit screen height while maintaining aspect ratio
            scale_factor = SCREEN_HEIGHT / bg_height
            scaled_width = int(bg_width * scale_factor)
            scaled_height = SCREEN_HEIGHT
            
            scaled_bg = pygame.transform.scale(self.background, (scaled_width, scaled_height))
            
            # Calculate how many background tiles we need to cover the screen
            tiles_needed = (SCREEN_WIDTH // scaled_width) + 2
            
            # Calculate the starting position for seamless scrolling
            start_x = -(camera_offset[0] % scaled_width)
            
            # Draw multiple background tiles to create seamless scrolling
            for i in range(tiles_needed):
                bg_x = start_x + (i * scaled_width)
                screen.blit(scaled_bg, (bg_x, 0))
                
        else:
            # Fallback: Create a repeating pattern background
            tile_size = 64
            for x in range(-tile_size, SCREEN_WIDTH + tile_size, tile_size):
                for y in range(0, SCREEN_HEIGHT, tile_size):
                    # Create a simple palace-like pattern
                    adjusted_x = x - (camera_offset[0] % tile_size)
                    color = (200, 180, 140) if (x + y) % (tile_size * 2) == 0 else (180, 160, 120)
                    pygame.draw.rect(screen, color, (adjusted_x, y, tile_size, tile_size))
                    pygame.draw.rect(screen, (160, 140, 100), (adjusted_x, y, tile_size, tile_size), 2)
    
    def render(self, screen, camera_offset):
        """Render level elements with better visibility"""
        # Render platforms with more visible colors
        for platform in self.platforms:
            render_rect = platform.rect.copy()
            render_rect.x -= camera_offset[0]
            render_rect.y -= camera_offset[1]
            
            # Only render if on screen
            if render_rect.right > 0 and render_rect.left < SCREEN_WIDTH:
                # Make platforms more visible
                pygame.draw.rect(screen, (139, 69, 19), render_rect)  # Brown
                pygame.draw.rect(screen, (101, 67, 33), render_rect, 3)  # Dark brown border
        
        # Render items
        for item in self.items:
            item.render(screen, camera_offset)
        
        # Render NPCs
        for npc in self.npcs:
            npc.render(screen, camera_offset)
        
        # Render enemies
        for enemy in self.enemies:
            enemy.render(screen, camera_offset)
    
    def get_platforms(self):
        return self.platforms
    
    def get_items(self):
        return self.items
    
    def get_npcs(self):
        return self.npcs
    
    def get_enemies(self):
        return [enemy for enemy in self.enemies if not enemy.defeated]
    
    def get_exit_zones(self):
        return self.exit_zones
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
