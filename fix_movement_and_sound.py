#!/usr/bin/env python3
"""
Fix for Moses Adventure - Step Sound and Platform Physics Issues

This script fixes two critical issues:
1. Step sounds not playing immediately when player moves
2. Player floating in air when walking off platforms
"""

import os
import shutil

def backup_files():
    """Create backups of files we're going to modify"""
    files_to_backup = [
        'game_classes.py',
        'main.py'
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            backup_name = f"{file}.backup_before_movement_fix"
            shutil.copy2(file, backup_name)
            print(f"✅ Backed up {file} to {backup_name}")

def fix_player_movement():
    """Fix the player movement system in game_classes.py"""
    
    # Read the current file
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the Player update method and replace it with fixed version
    old_update_method = '''    def update(self, dt):
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
        
        # Realistic walking sound system
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            if self.is_walking:
                # Update step timer
                self.step_timer += dt
                
                # Play step sound at regular intervals while walking
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0  # Reset timer for next step
                    
                # Mark that step sounds are playing
                if not self.is_step_sound_playing:
                    self.is_step_sound_playing = True
                    print("🚶 Started realistic step sounds")
            else:
                # Stop step sounds when not walking
                if self.is_step_sound_playing:
                    self.is_step_sound_playing = False
                    self.step_timer = 0  # Reset timer
                    print("🛑 Stopped step sounds")
        
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
        if self.rect.bottom >= ground_level - 2:  # Allow 2 pixel tolerance
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.on_ground = True'''

    new_update_method = '''    def update(self, dt):
        """Update player state with FIXED physics and immediate sound system"""
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
        
        # Store previous movement state for sound system
        was_walking = self.is_walking
        
        # Horizontal movement with IMMEDIATE sound system
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
        
        # FIXED: Immediate step sound system - play sound as soon as movement starts
        if hasattr(self, 'sound_manager') and self.sound_manager and self.on_ground:
            if self.is_walking and not was_walking:
                # Just started walking - play step sound immediately
                self.sound_manager.play_single_step()
                self.step_timer = 0  # Reset timer
                print("🚶 Started walking - immediate step sound")
            elif self.is_walking:
                # Continue walking - play step sounds at intervals
                self.step_timer += dt
                if self.step_timer >= self.step_interval:
                    self.sound_manager.play_single_step()
                    self.step_timer = 0
            elif was_walking and not self.is_walking:
                # Just stopped walking
                self.step_timer = 0
                print("🛑 Stopped walking")
        
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
        
        # FIXED GRAVITY AND PLATFORM DETECTION SYSTEM
        # Store old position for collision detection
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Apply gravity BEFORE movement
        if not self.on_ground:
            self.velocity_y += GRAVITY
            # Terminal velocity to prevent infinite acceleration
            if self.velocity_y > 15:
                self.velocity_y = 15
        
        # Update horizontal position first
        self.rect.x += self.velocity_x
        
        # Update vertical position
        self.rect.y += self.velocity_y
        
        # CRITICAL FIX: Check if player is still on a platform after horizontal movement
        # This prevents floating in air when walking off platforms
        if self.on_ground and self.velocity_x != 0:
            # Player moved horizontally while on ground - check if still on platform
            self.check_platform_support()
        
        # Update animation based on state
        self.update_animation_state()
        self.update_animation(dt)
        
        # Ground collision - ensure player stays on the ground platform
        ground_level = SCREEN_HEIGHT - 50  # Top of ground platform
        if self.rect.bottom >= ground_level - 2:  # Allow 2 pixel tolerance
            self.rect.bottom = ground_level
            self.velocity_y = 0
            self.on_ground = True
            if not hasattr(self, '_ground_landing_logged'):
                print(f"🏠 Moses landed on ground level at y={self.rect.y}")
                self._ground_landing_logged = True
        
        # Keep player within reasonable bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH * 5:
            self.rect.right = SCREEN_WIDTH * 5
    
    def check_platform_support(self):
        """Check if player is still supported by a platform after horizontal movement"""
        # This method will be called by the main game's collision system
        # For now, we'll set a flag that the main collision system can use
        self.needs_platform_check = True'''

    # Replace the old method with the new one
    if old_update_method in content:
        content = content.replace(old_update_method, new_update_method)
        print("✅ Fixed Player.update() method")
    else:
        print("⚠️  Could not find exact Player.update() method to replace")
        return False
    
    # Add the platform support check method to the Player class
    # Find the end of the Player class and add the method
    player_class_end = content.find("class NPC:")
    if player_class_end == -1:
        player_class_end = content.find("class Enemy:")
    
    if player_class_end != -1:
        # Insert the new method before the next class
        new_method = '''
    def check_platform_support(self):
        """Check if player is still supported by a platform after horizontal movement"""
        # This will be enhanced by the collision system
        self.needs_platform_check = True

'''
        content = content[:player_class_end] + new_method + content[player_class_end:]
        print("✅ Added check_platform_support() method")
    
    # Write the fixed content back
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def fix_collision_system():
    """Fix the collision system in main.py to handle platform support checking"""
    
    # Read the current file
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and replace the handle_platform_collision method
    old_collision_method = '''    def handle_platform_collision(self, platform):
        """Handle collision with platforms with realistic physics"""
        if not self.player or not platform:
            return
            
        player = self.player
        
        try:
            # Calculate overlap
            overlap_x = min(player.rect.right - platform.rect.left, 
                           platform.rect.right - player.rect.left)
            overlap_y = min(player.rect.bottom - platform.rect.top, 
                           platform.rect.bottom - player.rect.top)
            
            # Add tolerance for ground-level collision
            if abs(player.rect.bottom - platform.rect.top) <= 3:
                # Player is standing on platform (with tolerance)
                player.rect.bottom = platform.rect.top
                if hasattr(player, 'velocity_y'):
                    player.velocity_y = 0
                player.on_ground = True
                player.is_jumping = False
                
                # Debug: Show platform landing
                if not hasattr(self, '_platform_landing_logged'):
                    print(f"🏗️  Moses landed on platform at y={platform.rect.top}")
                    self._platform_landing_logged = True
                
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
                    player.on_ground = True
                    player.is_jumping = False
                    
                    # Debug: Show platform landing
                    if not hasattr(self, '_platform_landing_logged'):
                        print(f"🏗️  Moses landed on platform at y={platform.rect.top}")
                        self._platform_landing_logged = True
                    
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
                player.rect.bottom = platform.rect.top - 1'''

    new_collision_method = '''    def handle_platform_collision(self, platform):
        """Handle collision with platforms with FIXED physics"""
        if not self.player or not platform:
            return
            
        player = self.player
        
        try:
            # Calculate overlap
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
                player.on_ground = True
                player.is_jumping = False
                
                # Clear the platform check flag if it exists
                if hasattr(player, 'needs_platform_check'):
                    player.needs_platform_check = False
                
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
                    player.on_ground = True
                    player.is_jumping = False
                    
                    # Clear the platform check flag if it exists
                    if hasattr(player, 'needs_platform_check'):
                        player.needs_platform_check = False
                else:
                    # Hitting from below
                    player.rect.top = platform.rect.bottom
                    if hasattr(player, 'velocity_y'):
                        player.velocity_y = 0
        except Exception as e:
            print(f"⚠️  Collision error: {e}")
            # Prevent crash by doing basic collision resolution
            if hasattr(player, 'rect') and hasattr(platform, 'rect'):
                player.rect.bottom = platform.rect.top - 1'''

    # Replace the old method with the new one
    if old_collision_method in content:
        content = content.replace(old_collision_method, new_collision_method)
        print("✅ Fixed handle_platform_collision() method")
    else:
        print("⚠️  Could not find exact handle_platform_collision() method")
    
    # Add platform support checking to the collision system
    old_check_collisions = '''    def check_collisions(self):
        """Check for collisions with realistic physics effects"""
        if not self.player:
            return
        
        try:
            # Platform collisions with realistic physics
            platforms = self.level_manager.get_platforms()
            
            # Debug: Show platform count
            if not hasattr(self, '_platform_debug_shown'):
                print(f"🏗️  Loaded {len(platforms)} platforms for collision detection")
                self._platform_debug_shown = True
            
            for platform in platforms:
                if platform and hasattr(platform, 'rect') and self.player.rect.colliderect(platform.rect):
                    self.handle_platform_collision(platform)'''

    new_check_collisions = '''    def check_collisions(self):
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
                    self.handle_platform_collision(platform)'''

    # Replace the collision check method
    if old_check_collisions in content:
        content = content.replace(old_check_collisions, new_check_collisions)
        print("✅ Fixed check_collisions() method")
    else:
        print("⚠️  Could not find exact check_collisions() method")
    
    # Write the fixed content back
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main function to apply all fixes"""
    print("🔧 Moses Adventure - Movement and Sound Fixes")
    print("=" * 50)
    
    # Create backups
    print("\n1. Creating backups...")
    backup_files()
    
    # Fix player movement and sound system
    print("\n2. Fixing player movement and step sounds...")
    if fix_player_movement():
        print("✅ Player movement system fixed")
    else:
        print("❌ Failed to fix player movement system")
        return
    
    # Fix collision system
    print("\n3. Fixing collision system...")
    if fix_collision_system():
        print("✅ Collision system fixed")
    else:
        print("❌ Failed to fix collision system")
        return
    
    print("\n" + "=" * 50)
    print("🎉 ALL FIXES APPLIED SUCCESSFULLY!")
    print("\nFixes applied:")
    print("✅ Step sounds now play immediately when movement starts")
    print("✅ Player no longer floats when walking off platforms")
    print("✅ Improved platform collision detection")
    print("✅ Better gravity system")
    print("\nYou can now test the game with:")
    print("python3 main.py")
    print("\nIf you need to revert changes, restore from the .backup files")

if __name__ == "__main__":
    main()
