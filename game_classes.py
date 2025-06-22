import pygame
import random
import math
import os
from enum import Enum
from typing import Dict, List, Tuple, Optional
from enemy_class import Enemy

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

class Stone:
    """Stone projectile for combat"""
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 8, 8)
        self.velocity_x = direction * 300  # Fast horizontal movement
        self.velocity_y = -50  # Slight upward arc
        self.gravity = 200  # Falls down
        self.active = True
        self.lifetime = 3.0  # Disappear after 3 seconds
        
    def update(self, dt):
        """Update stone physics"""
        if not self.active:
            return
            
        # Apply physics
        self.rect.x += self.velocity_x * dt
        self.rect.y += self.velocity_y * dt
        self.velocity_y += self.gravity * dt  # Gravity
        
        # Remove if off screen or hit ground
        if (self.rect.x < -50 or self.rect.x > SCREEN_WIDTH + 50 or 
            self.rect.y > SCREEN_HEIGHT):
            self.active = False
            
        # Lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.active = False
    
    def render(self, screen, camera_offset):
        """Render the stone"""
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Draw stone as small brown circle
        pygame.draw.circle(screen, (139, 69, 19), (render_x + 4, render_y + 4), 4)
        pygame.draw.circle(screen, (101, 67, 33), (render_x + 4, render_y + 4), 4, 1)


class StaffProjectile:
    """Staff projectile using diamond yellow shape - SIMPLE AND RELIABLE"""
    def __init__(self, x, y, direction):
        import pygame  # Import pygame at the top
        
        self.rect = pygame.Rect(x, y, 16, 16)  # 16x16 diamond size
        self.velocity_x = direction * 450  # Fast movement
        self.velocity_y = 0  # Straight horizontal
        self.active = True
        self.lifetime = 3.0  # 3 seconds lifetime
        self.damage = 20  # 20 damage per hit
        self.direction = direction
        
        print(f"⚡ CREATED DIAMOND staff projectile at x={x}, y={y}, direction={direction}")
        
    def update(self, dt):
        """Update staff projectile physics"""
        if not self.active:
            return
            
        # Move horizontally
        old_x = self.rect.x
        self.rect.x += self.velocity_x * dt
        
        # Debug movement every 50 pixels
        if abs(self.rect.x - old_x) > 0 and int(self.rect.x) % 50 == 0:
            print(f"⚡ Diamond projectile moving: x={self.rect.x}, y={self.rect.y}")
        
        # Remove if off screen
        if (self.rect.x < -100 or self.rect.x > 2000):
            print(f"⚡ Diamond projectile off screen at x={self.rect.x}")
            self.active = False
            
        # Lifetime countdown
        self.lifetime -= dt
        if self.lifetime <= 0:
            print("⚡ Diamond projectile expired")
            self.active = False
    
    def render(self, screen, camera_offset):
        """Render the staff projectile as a bright yellow diamond"""
        import pygame  # Import pygame at the top
        
        if not self.active:
            return
            
        render_x = self.rect.x - camera_offset[0]
        render_y = self.rect.y - camera_offset[1]
        
        # Only render if on screen
        if render_x < -50 or render_x > 850:
            return
        
        print(f"⚡ RENDERING DIAMOND staff projectile at screen x={render_x}, y={render_y}")
        print(f"⚡ Diamond direction: {self.direction}, center: ({center_x}, {center_y})")
        
        # Calculate diamond points (centered on the rect)
        center_x = render_x + 8  # Half of 16
        center_y = render_y + 8  # Half of 16
        
        # Diamond points (top, right, bottom, left)
        diamond_points = [
            (center_x, center_y - 8),      # Top point
            (center_x + 8, center_y),     # Right point  
            (center_x, center_y + 8),     # Bottom point
            (center_x - 8, center_y)      # Left point
        ]
        
        # Draw bright yellow diamond with glow effect and direction indicator
        # Create glow surface
        glow_surface = pygame.Surface((32, 32))
        glow_surface.set_alpha(80)
        glow_surface.fill((255, 255, 0))  # Yellow
        screen.blit(glow_surface, (render_x - 8, render_y - 8))
        
                # SIMPLE BRIGHT TRAIL - Draw before diamond for visibility
        trail_length = 16
        if self.direction > 0:  # Moving right, trail behind (left)
            # Draw bright yellow trail rectangles
            pygame.draw.rect(screen, (255, 255, 0), (center_x - trail_length, center_y - 2, trail_length - 4, 4))
            pygame.draw.rect(screen, (255, 255, 255), (center_x - trail_length + 2, center_y - 1, trail_length - 8, 2))
        else:  # Moving left, trail behind (right)
            # Draw bright yellow trail rectangles
            pygame.draw.rect(screen, (255, 255, 0), (center_x + 4, center_y - 2, trail_length, 4))
            pygame.draw.rect(screen, (255, 255, 255), (center_x + 6, center_y - 1, trail_length - 4, 2))
        
        # Draw main diamond (bright yellow)
        pygame.draw.polygon(screen, (255, 255, 0), diamond_points)  # Bright yellow
        
        # Draw inner diamond (white center for brightness)
        inner_points = [
            (center_x, center_y - 4),      # Top point (smaller)
            (center_x + 4, center_y),     # Right point (smaller)
            (center_x, center_y + 4),     # Bottom point (smaller)
            (center_x - 4, center_y)      # Left point (smaller)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), inner_points)  # White center
        
        # Draw diamond outline for definition
        pygame.draw.polygon(screen, (255, 215, 0), diamond_points, 2)  # Gold outline
        
        # Add directional trail effect to show movement direction
        trail_length = 12
        if self.direction > 0:  # Moving right
            # Trail behind (to the left)
            trail_points = [
                (center_x - trail_length, center_y - 2),
                (center_x - 4, center_y),
                (center_x - trail_length, center_y + 2)
            ]
        else:  # Moving left
            # Trail behind (to the right)
            trail_points = [
                (center_x + trail_length, center_y - 2),
                (center_x + 4, center_y),
                (center_x + trail_length, center_y + 2)
            ]
        
        # Draw HIGHLY VISIBLE trail with multiple effects
        # Method 1: Bright solid trail rectangles
        trail_width = 20
        trail_height = 6
        
        if self.direction > 0:  # Moving right, trail on left
            # Multiple trail segments for motion blur effect
            for i in range(3):
                trail_x = center_x - trail_length - (i * 6)
                trail_alpha = 255 - (i * 60)  # Fade out
                
                # Create bright trail segment
                trail_rect = pygame.Rect(trail_x - 8, center_y - 3, trail_width - (i * 4), trail_height)
                pygame.draw.rect(screen, (255, 255, 0), trail_rect)  # Bright yellow
                pygame.draw.rect(screen, (255, 255, 255), (trail_x - 6, center_y - 1, trail_width - (i * 4) - 4, 2))  # White center
        else:  # Moving left, trail on right
            # Multiple trail segments for motion blur effect
            for i in range(3):
                trail_x = center_x + trail_length + (i * 6)
                trail_alpha = 255 - (i * 60)  # Fade out
                
                # Create bright trail segment
                trail_rect = pygame.Rect(trail_x - 4, center_y - 3, trail_width - (i * 4), trail_height)
                pygame.draw.rect(screen, (255, 255, 0), trail_rect)  # Bright yellow
                pygame.draw.rect(screen, (255, 255, 255), (trail_x - 2, center_y - 1, trail_width - (i * 4) - 4, 2))  # White center
        
        # Method 2: Additional particle trail effect
        import random
        for i in range(5):  # 5 trail particles
            if self.direction > 0:  # Moving right
                particle_x = center_x - 8 - (i * 4) + random.randint(-2, 2)
                particle_y = center_y + random.randint(-3, 3)
            else:  # Moving left
                particle_x = center_x + 8 + (i * 4) + random.randint(-2, 2)
                particle_y = center_y + random.randint(-3, 3)
            
            # Draw bright particle
            pygame.draw.circle(screen, (255, 255, 100), (particle_x, particle_y), 2)
        
        print(f"⚡ RENDERING TRAIL for direction {self.direction} at center ({center_x}, {center_y})")

class Player:
    def __init__(self, x, y, sprites):
        self.rect = pygame.Rect(x, y, 32, 48)
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = True  # Start on ground
        self.health = 100
        self.max_health = 100
        self.facing_right = True
        
        # Combat system (removed direct stone management)
        self.can_attack = True
        self.attack_cooldown = 0
        self.attack_cooldown_time = 0.5  # Half second between attacks
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_time = 1.0  # 1 second of invulnerability after taking damage
        
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
        
        # Enhanced movement tracking for realistic step sounds
        self.step_timer = 0
        self.step_interval = 0.5  # Time between steps (0.5 seconds = realistic walking pace)
        self.is_step_sound_playing = False
        
        # Position Moses properly on the ground
        self.rect.bottom = SCREEN_HEIGHT - 50 + 1  # Slightly overlap with ground platform
        self.on_ground = True  # Ensure Moses starts on ground for jumping
                
        # Staff system
        self.has_staff = False
        self.staff_active = False
        self.staff_duration = 120.0  # 2 minutes in seconds
        self.staff_timer = 0.0
        self.staff_cooldown = 0.0
        self.staff_cooldown_time = 0.3  # 0.3 seconds between staff shots
        self.staff_projectiles = []
        
        # Armor of God system
        self.has_armor_buff = False
        self.armor_buff = 0
        self.max_health_with_armor = self.max_health

    def update(self, dt):
        """Update player state with enhanced physics and smart sound system"""
        keys = pygame.key.get_pressed()
        
        # Handle interaction state
        if self.is_interacting:
            self.interaction_timer -= dt
            if self.interaction_timer <= 0:
                self.is_interacting = False
        
        # Handle combat timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt
            if self.attack_cooldown <= 0:
                self.can_attack = True
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
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
        
        # FIXED: IMMEDIATE step sound system - plays instantly on key press
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            # Initialize previous walking state if not exists
            if not hasattr(self, '_was_walking_last_frame'):
                self._was_walking_last_frame = False
            
            # IMMEDIATE RESPONSE: Check if we just started walking (key press moment)
            if self.is_walking and not self._was_walking_last_frame:
                # Just pressed arrow key - play step sound IMMEDIATELY
                self.sound_manager.play_single_step()
                self.step_timer = 0
                print("🚶 Arrow key pressed - IMMEDIATE step sound!")
            elif self.is_walking and self._was_walking_last_frame:
                # Continue walking - play step sounds at intervals
                self.step_timer += dt
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0
            elif not self.is_walking and self._was_walking_last_frame:
                # Just stopped walking (released arrow key)
                self.step_timer = 0
                print("🛑 Arrow key released - stopped walking")
            
            # Remember walking state for next frame
            self._was_walking_last_frame = self.is_walking
        
        # Jumping with sound effect - UP arrow only
        if keys[pygame.K_UP]:
            if self.on_ground:
                self.velocity_y = JUMP_STRENGTH
                self.on_ground = False
                self.is_jumping = True
                print(f"🦘 Moses jumping! y={self.rect.y}, velocity_y={JUMP_STRENGTH}")
                # Play jump sound if sound manager is available
                if hasattr(self, 'sound_manager') and self.sound_manager:
                    self.sound_manager.play_jump_sound()
            else:
                print(f"❌ Can't jump: on_ground={self.on_ground}, velocity_y={self.velocity_y}")
        
        # Debug: Show current state occasionally
        if keys[pygame.K_UP] or (hasattr(self, '_debug_counter') and self._debug_counter % 60 == 0):
            print(f"🔍 Moses state: y={self.rect.y}, on_ground={self.on_ground}, velocity_y={self.velocity_y}")
        
        if not hasattr(self, '_debug_counter'):
            self._debug_counter = 0
        self._debug_counter += 1
        
        # IMPROVED GRAVITY SYSTEM
        # Always apply gravity when not on ground
        if not self.on_ground:
            self.velocity_y += GRAVITY
            # Terminal velocity to prevent infinite acceleration
            if self.velocity_y > 15:
                self.velocity_y = 15
        else:
            # On ground - stop falling
            if self.velocity_y > 0:
                self.velocity_y = 0
        
        # Store old position for collision detection
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Update horizontal position
        self.rect.x += self.velocity_x
        
        # FIXED: Check if player walked off a platform
        if self.on_ground and self.velocity_x != 0:
            self.check_platform_support()
        
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
        
        # Platform collision detection - FIXED VERSION
        platform_collision = False
        
        # OPTIMIZED: Check if we have platforms (reduced debug output)
        if hasattr(self, 'game_platforms') and self.game_platforms:
            # Only check platforms near the player for better performance
            player_x = self.rect.centerx
            nearby_platforms = [p for p in self.game_platforms 
                              if abs(p['x'] + p['width']/2 - player_x) < 500]  # Only check nearby platforms
            
            for platform in nearby_platforms:
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                
                # OPTIMIZED: Check if player is falling onto platform
                if (self.velocity_y >= 0 and  # Falling or stationary
                    self.rect.bottom >= platform_rect.top - 5 and  # Player bottom near platform top
                    self.rect.bottom <= platform_rect.top + 15 and  # Generous landing tolerance
                    self.rect.right > platform_rect.left + 2 and  # Horizontal overlap (small margin)
                    self.rect.left < platform_rect.right - 2):  # Horizontal overlap (small margin)
                    
                    # Land on platform
                    self.rect.bottom = platform_rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                    platform_collision = True
                    # Reduced debug output for performance
                    if hasattr(self, 'debug_collision') and self.debug_collision:
                        print(f"🏗️  ✅ MOSES LANDED ON PLATFORM at x={platform['x']}, y={platform['y']}")
                    break
        
        # Ground collision - ensure player stays on the ground platform (fallback)
        if not platform_collision:
            ground_level = SCREEN_HEIGHT - 50  # Top of ground platform
            if self.rect.bottom >= ground_level - 2:  # Allow 2 pixel tolerance
                self.rect.bottom = ground_level
                self.velocity_y = 0
                self.on_ground = True
                self.is_jumping = False
                if not hasattr(self, '_ground_landing_logged'):
                    print(f"🏠 Moses landed on ground level at y={self.rect.y}")
                    self._ground_landing_logged = True
        
        # Keep player within reasonable bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH * 5:
            self.rect.right = SCREEN_WIDTH * 5
        
        # Update staff system
        if hasattr(self, 'update_staff_system'):
            self.update_staff_system(dt)
    
    def check_platform_support(self):
        """Check if player is still supported by a platform after horizontal movement"""
        self.needs_platform_check = True
    
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
    
    def set_walking_pace(self, pace="normal"):
        """Set the walking pace for step sounds"""
        if pace == "slow":
            self.step_interval = 0.7  # Slower steps
        elif pace == "fast":
            self.step_interval = 0.3  # Faster steps
        else:  # normal
            self.step_interval = 0.5  # Normal walking pace
        
        print(f"🚶 Walking pace set to {pace} (interval: {self.step_interval}s)")
    
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
        """Take damage with invulnerability period"""
        if not self.invulnerable:
            self.health = max(0, self.health - damage)
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerable_time
            
            # Play hurt sound
            if hasattr(self, 'sound_manager') and self.sound_manager:
                self.sound_manager.play_sound('player_hurt')
            
            print(f"💔 Moses took {damage} damage! Health: {self.health}/{self.max_health}")
            return self.health <= 0
        return False
    
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


    def activate_staff(self):
        """Activate the staff buff"""
        self.has_staff = True
        self.staff_active = True
        self.staff_timer = self.staff_duration
        print("🪄 Moses' Staff activated! Press W to shoot divine projectiles!")
        print(f"⏰ Staff will last for {self.staff_duration/60:.1f} minutes")
    
    def deactivate_staff(self):
        """Deactivate the staff buff"""
        self.staff_active = False
        self.staff_timer = 0.0
        print("⏰ Moses' Staff power has expired")
    
    def shoot_staff_projectile(self):
        """Shoot a staff projectile - ENHANCED DEBUG VERSION"""
        if not self.staff_active:
            print("❌ Staff not active - cannot shoot")
            return False
            
        if self.staff_cooldown > 0:
            print(f"❌ Staff on cooldown: {self.staff_cooldown:.2f}s remaining")
            return False
        
        # Create projectile in front of player
        direction = 1 if self.facing_right else -1
        
        # Position projectile in front of player (further out for better visibility)
        if self.facing_right:
            projectile_x = self.rect.right + 10  # 10 pixels in front when facing right
        else:
            projectile_x = self.rect.left - 26   # 26 pixels in front when facing left (16 for diamond width + 10 spacing)
        
        # Position at player's center height
        projectile_y = self.rect.centery - 8  # Center the 16px diamond on player center
        
        print(f"⚡ Creating staff projectile at player pos x={self.rect.centerx}, y={self.rect.centery}")
        print(f"⚡ Player facing: {'RIGHT' if self.facing_right else 'LEFT'}")
        print(f"⚡ Projectile spawn: x={projectile_x}, y={projectile_y}, direction={direction}")
        
        projectile = StaffProjectile(projectile_x, projectile_y, direction)
        self.staff_projectiles.append(projectile)
        
        print(f"⚡ Total staff projectiles: {len(self.staff_projectiles)}")
        
        # Set cooldown
        self.staff_cooldown = self.staff_cooldown_time
        
        print("⚡ Moses shoots divine energy!")
        return True
    
    def update_staff_system(self, dt):
        """Update staff system timers and projectiles"""
        # Update staff duration
        if self.staff_active:
            self.staff_timer -= dt
            if self.staff_timer <= 0:
                self.deactivate_staff()
        
        # Update staff cooldown
        if self.staff_cooldown > 0:
            self.staff_cooldown -= dt
        
        # Update staff projectiles
        for projectile in self.staff_projectiles[:]:
            projectile.update(dt)
            if not projectile.active:
                self.staff_projectiles.remove(projectile)
    
    def render_staff_projectiles(self, screen, camera_offset):
        """Render all staff projectiles - ENHANCED DEBUG VERSION"""
        if len(self.staff_projectiles) > 0:
            print(f"⚡ Rendering {len(self.staff_projectiles)} staff projectiles")
        
        for i, projectile in enumerate(self.staff_projectiles):
            if projectile.active:
                print(f"⚡ Rendering projectile {i}: x={projectile.rect.x}, y={projectile.rect.y}")
                projectile.render(screen, camera_offset)
            else:
                print(f"⚡ Projectile {i} is inactive")
    
    def get_staff_time_remaining(self):
        """Get remaining staff time in seconds"""
        return max(0, self.staff_timer) if self.staff_active else 0

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.smoothing = 0.1
        self.vertical_smoothing = 0.08  # Slightly slower vertical movement for comfort
        self.vertical_deadzone = 50  # Pixels of movement before camera follows vertically
    
    def follow_player(self, player):
        """Follow the player both horizontally AND vertically for platform jumping"""
        if not player:
            return
        
        # Horizontal following (existing)
        self.target_x = player.rect.centerx - SCREEN_WIDTH // 2
        
        # VERTICAL FOLLOWING - Camera follows Moses up and down platforms
        self.target_y = player.rect.centery - SCREEN_HEIGHT // 2
        
        # Smooth horizontal camera movement
        self.x += (self.target_x - self.x) * self.smoothing
        
        # Smooth vertical camera movement with deadzone
        y_diff = self.target_y - self.y
        if abs(y_diff) > self.vertical_deadzone:  # Only move if significant vertical movement
            self.y += y_diff * self.vertical_smoothing
        
        # Keep camera within reasonable bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH * 5))  # Horizontal bounds
        
        # Extended vertical bounds for platform exploration
        # Allow camera to go higher for platforms, but not too low
        self.y = max(-500, min(self.y, 200))  # Extended vertical range
        
        # OPTIMIZED: Reduced debug output for better performance
        if hasattr(self, 'debug_camera') and self.debug_camera and abs(y_diff) > self.vertical_deadzone:
            print(f"📹 Camera following Moses vertically: player_y={player.rect.centery}, camera_y={self.y}")
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return (int(self.x), int(self.y))

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
                
                # Removed yellow outline for cleaner look
                # pygame.draw.rect(screen, (255, 255, 0), render_rect, 3)
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
            
            # Show NPC type label only when nearby (less intrusive)
            # Only show if player is close enough to interact
            if hasattr(self, 'showing_prompt') and self.showing_prompt:
                font = pygame.font.Font(None, 18)  # Smaller font
                label_text = font.render(self.npc_type.replace('_', ' ').title(), True, (255, 255, 255))
                label_bg = pygame.Rect(render_rect.centerx - 35, render_rect.top - 22, 70, 18)
                pygame.draw.rect(screen, (0, 0, 0, 180), label_bg)  # Semi-transparent
                pygame.draw.rect(screen, (200, 200, 200), label_bg, 1)  # Subtle gray border
                screen.blit(label_text, (label_bg.left + 3, label_bg.top + 1))
            
            # Show interaction prompt with more subtle styling
            if hasattr(self, 'showing_prompt') and self.showing_prompt:
                prompt_font = pygame.font.Font(None, 22)
                prompt_text = prompt_font.render("Press E to Interact", True, (255, 255, 255))
                prompt_bg = pygame.Rect(render_rect.centerx - 55, render_rect.bottom + 5, 110, 22)
                pygame.draw.rect(screen, (0, 0, 0, 200), prompt_bg)  # Semi-transparent black
                pygame.draw.rect(screen, (100, 200, 100), prompt_bg, 2)  # Subtle green border
                screen.blit(prompt_text, (prompt_bg.left + 3, prompt_bg.top + 2))
            
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
        self.simple_enemies = []  # Simple enemy blocks
        self.stones = []  # Active stone projectiles
        self.exit_zones = []
        self.background = None
    
    def load_level(self, location, sprites):
        """Load a specific level"""
        self.current_location = location
        self.sprites = sprites  # Store sprites for enemy rendering
        
        # Clear existing level data
        self.platforms.clear()
        self.items.clear()
        self.npcs.clear()
        self.enemies.clear()
        self.simple_enemies.clear()  # Clear simple enemies too
        self.stones.clear()  # Clear stones too
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
        # Note: Using fallback enemy creation since Enemy class has import issues
        # These will be simple moving blocks until Enemy class is fixed
        print("⚠️ Creating simple enemy blocks (Enemy class needs fixing)")
        
        # Create simple enemy rectangles as moving obstacles
        for i, x_pos in enumerate([600, 1000, 1400, 1800, 2200, 2600, 3000]):
            enemy_rect = pygame.Rect(x_pos, moses_ground_y, 32, 32)
            # Store as simple dict for now
            simple_enemy = {
                'rect': enemy_rect,
                'type': 'egyptian_soldier',
                'health': 30,
                'current_health': 30,  # Track current health
                'defeated': False,
                'direction': 1 if i % 2 == 0 else -1,
                'start_x': x_pos,
                'speed': 1
            }
            self.simple_enemies.append(simple_enemy)
        
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
        print("⚠️ Creating simple enemy blocks for Egypt City")
        
        for i, x_pos in enumerate([500, 1000, 1600]):
            enemy_rect = pygame.Rect(x_pos, enemy_y, 32, 32)
            simple_enemy = {
                'rect': enemy_rect,
                'type': 'egyptian_soldier',
                'health': 30,
                'current_health': 30,
                'defeated': False,
                'direction': 1 if i % 2 == 0 else -1,
                'start_x': x_pos,
                'speed': 1
            }
            self.simple_enemies.append(simple_enemy)
        
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
        print("⚠️ Creating simple enemy blocks for Desert")
        
        for i, (x_pos, enemy_type) in enumerate([(600, 'wild_animal'), (1200, 'wild_animal'), (1800, 'egyptian_soldier')]):
            enemy_rect = pygame.Rect(x_pos, enemy_y, 32, 32)
            simple_enemy = {
                'rect': enemy_rect,
                'type': enemy_type,
                'health': 20 if enemy_type == 'wild_animal' else 30,
                'current_health': 20 if enemy_type == 'wild_animal' else 30,
                'defeated': False,
                'direction': 1 if i % 2 == 0 else -1,
                'start_x': x_pos,
                'speed': 2 if enemy_type == 'wild_animal' else 1
            }
            self.simple_enemies.append(simple_enemy)
        
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
        # Wild animals scattered throughout
        print("⚠️ Creating simple enemy blocks for Red Sea")
        for i in range(4):
            x = 400 + i * 400
            enemy_rect = pygame.Rect(x, SCREEN_HEIGHT - 100, 32, 32)
            simple_enemy = {
                'rect': enemy_rect,
                'type': 'wild_animal',
                'health': 20,
                'current_health': 20,
                'defeated': False,
                'direction': 1 if i % 2 == 0 else -1,
                'start_x': x,
                'speed': 2
            }
            self.simple_enemies.append(simple_enemy)
        
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
        # Render platforms with consistent brown colors (supports both dict and object formats)
        for platform in self.platforms:
            # Handle dict format (new platform system)
            if isinstance(platform, dict):
                render_x = platform['x'] - camera_offset[0]
                render_y = platform['y'] - camera_offset[1]
                render_rect = pygame.Rect(render_x, render_y, platform['width'], platform['height'])
            # Handle object format (legacy system)
            elif hasattr(platform, 'rect'):
                render_rect = platform.rect.copy()
                render_rect.x -= camera_offset[0]
                render_rect.y -= camera_offset[1]
            else:
                continue  # Skip invalid platform data
            
            # Only render if on screen
            if render_rect.right > 0 and render_rect.left < SCREEN_WIDTH:
                # Consistent brown stone platforms
                pygame.draw.rect(screen, (139, 69, 19), render_rect)    # Brown stone
                pygame.draw.rect(screen, (101, 67, 33), render_rect, 3) # Dark brown border
                pygame.draw.rect(screen, (160, 82, 45), (render_rect.x + 2, render_rect.y + 2, render_rect.width - 4, 4))  # Highlight
        
        # Render items
        for item in self.items:
            item.render(screen, camera_offset)
        
        # Render NPCs
        for npc in self.npcs:
            npc.render(screen, camera_offset)
        
        # Render enemies (original)
        for enemy in self.enemies:
            enemy.render(screen, camera_offset)
        
        # Render simple enemies
        self.render_simple_enemies(screen, camera_offset)
        
        # Render stone projectiles
        self.render_stones(screen, camera_offset)
    
    def get_platforms(self):
        return self.platforms
    
    def get_items(self):
        return self.items
    
    def get_npcs(self):
        return self.npcs
    
    def get_enemies(self):
        return [enemy for enemy in self.enemies if not enemy.defeated]
    
    def get_simple_enemies(self):
        """Get active simple enemies"""
        return [enemy for enemy in self.simple_enemies if not enemy['defeated']]
    
    def update_simple_enemies(self, dt):
        """Update simple enemy blocks"""
        for enemy in self.simple_enemies:
            if enemy['defeated']:
                continue
                
            # Simple AI: move back and forth
            enemy['rect'].x += enemy['direction'] * enemy['speed']
            
            # Bounce off boundaries (100 pixels from start position)
            if abs(enemy['rect'].x - enemy['start_x']) > 100:
                enemy['direction'] *= -1
    
    def render_simple_enemies(self, screen, camera_offset):
        """Render simple enemy blocks with actual sprites"""
        for enemy in self.simple_enemies:
            if enemy['defeated']:
                continue
                
            # Calculate screen position
            screen_x = enemy['rect'].x - camera_offset[0]
            screen_y = enemy['rect'].y - camera_offset[1]
            
            # Only render if on screen
            if -50 < screen_x < SCREEN_WIDTH + 50:
                # Try to get actual sprite first
                sprite = None
                if hasattr(self, 'sprites') and self.sprites and 'enemies' in self.sprites:
                    sprite = self.sprites['enemies'].get(enemy['type'])
                
                if sprite:
                    # Use actual sprite
                    sprite_rect = pygame.Rect(screen_x, screen_y, enemy['rect'].width, enemy['rect'].height)
                    
                    # Flip sprite based on direction for more dynamic look
                    if enemy['direction'] < 0:
                        sprite = pygame.transform.flip(sprite, True, False)
                    
                    screen.blit(sprite, sprite_rect)
                    
                    # Add subtle health indicator (small red bar if damaged)
                    if enemy.get('current_health', enemy['health']) < enemy['health']:
                        health_percent = enemy.get('current_health', enemy['health']) / enemy['health']
                        bar_width = 30
                        bar_height = 4
                        bar_x = screen_x + (enemy['rect'].width - bar_width) // 2
                        bar_y = screen_y - 8
                        
                        # Background
                        pygame.draw.rect(screen, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                        # Health
                        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, int(bar_width * health_percent), bar_height))
                else:
                    # Fallback to colored rectangles if sprites not available
                    if enemy['type'] == 'wild_animal':
                        color = (139, 69, 19)  # Brown for animals
                    else:
                        color = (139, 0, 0)    # Dark red for soldiers
                    
                    # Draw enemy as colored rectangle
                    pygame.draw.rect(screen, color, (screen_x, screen_y, 32, 32))
                    # Add simple border
                    pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, 32, 32), 2)
    
    def check_simple_enemy_collisions(self, player):
        """Check collisions with simple enemies - solid collision + damage"""
        for enemy in self.simple_enemies:
            if enemy['defeated']:
                continue
                
            if player.rect.colliderect(enemy['rect']):
                # Handle solid collision physics first
                self.handle_enemy_collision_physics(player, enemy)
                
                # Then handle damage
                damage = 20 if enemy['type'] == 'wild_animal' else 15
                game_over = player.take_damage(damage)
                
                print(f"💥 Player hit {enemy['type']} for {damage} damage!")
                
                if game_over:
                    print("💀 Game Over! Moses has fallen!")
                    return 'game_over'
                
                return 'damage_taken'
        
        return False
    
    def handle_enemy_collision_physics(self, player, enemy):
        """Handle solid collision physics with enemies"""
        # Calculate overlap
        overlap_x = min(player.rect.right - enemy['rect'].left, 
                       enemy['rect'].right - player.rect.left)
        overlap_y = min(player.rect.bottom - enemy['rect'].top, 
                       enemy['rect'].bottom - player.rect.top)
        
        # Push player away from enemy based on smallest overlap
        if overlap_x < overlap_y:
            # Horizontal collision - push left or right
            if player.rect.centerx < enemy['rect'].centerx:
                # Player is to the left, push left
                player.rect.right = enemy['rect'].left - 1
                player.velocity_x = min(player.velocity_x, 0)  # Stop rightward movement
            else:
                # Player is to the right, push right
                player.rect.left = enemy['rect'].right + 1
                player.velocity_x = max(player.velocity_x, 0)  # Stop leftward movement
        else:
            # Vertical collision - push up or down
            if player.rect.centery < enemy['rect'].centery:
                # Player is above, push up
                player.rect.bottom = enemy['rect'].top - 1
                player.velocity_y = min(player.velocity_y, 0)  # Stop downward movement
                player.on_ground = True  # Player can stand on enemies
            else:
                # Player is below, push down
                player.rect.top = enemy['rect'].bottom + 1
                player.velocity_y = max(player.velocity_y, 0)  # Stop upward movement
    
    def get_exit_zones(self):
        return self.exit_zones
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
    
    def add_stone(self, stone):
        """Add a stone projectile"""
        self.stones.append(stone)
    
    def update_stones(self, dt):
        """Update all stone projectiles"""
        for stone in self.stones[:]:  # Copy list to avoid modification during iteration
            stone.update(dt)
            if not stone.active:
                self.stones.remove(stone)
    
    def check_stone_enemy_collisions(self):
        """Check if stones hit enemies"""
        hits = 0
        for stone in self.stones[:]:
            if not stone.active:
                continue
                
            for enemy in self.simple_enemies:
                if enemy['defeated']:
                    continue
                    
                if stone.rect.colliderect(enemy['rect']):
                    # Stone hits enemy - deal damage
                    stone_damage = 15  # Each stone does 15 damage
                    enemy['current_health'] -= stone_damage
                    
                    # Remove stone
                    stone.active = False
                    self.stones.remove(stone)
                    hits += 1
                    
                    if enemy['current_health'] <= 0:
                        # Enemy defeated
                        enemy['defeated'] = True
                        print(f"🎯 Stone defeated {enemy['type']}!")
                    else:
                        # Enemy damaged but still alive
                        print(f"🎯 Stone hit {enemy['type']} for {stone_damage} damage! Health: {enemy['current_health']}/{enemy['health']}")
                    
                    break
        
        return hits
    
    def render_stones(self, screen, camera_offset):
        """Render all stone projectiles"""
        for stone in self.stones:
            stone.render(screen, camera_offset)
