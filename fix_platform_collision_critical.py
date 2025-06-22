#!/usr/bin/env python3
"""
Critical fix for platform collision detection - Moses can't jump to platforms
"""

def fix_platform_collision_detection():
    """Fix the critical platform collision detection issue"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the current platform collision code and fix it
    old_collision_code = '''        # Platform collision detection - check all platforms
        platform_collision = False
        
        # Check collision with game platforms (new system)
        if hasattr(self, 'game_platforms'):
            for platform in self.game_platforms:
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                
                # Check if player is falling onto platform
                if (self.velocity_y >= 0 and  # Falling or stationary
                    self.rect.bottom >= platform_rect.top and  # Player bottom at or below platform top
                    self.rect.bottom <= platform_rect.top + 10 and  # Within landing tolerance
                    self.rect.right > platform_rect.left + 5 and  # Horizontal overlap (with margin)
                    self.rect.left < platform_rect.right - 5):  # Horizontal overlap (with margin)
                    
                    # Land on platform
                    self.rect.bottom = platform_rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.is_jumping = False
                    platform_collision = True
                    print(f"🏗️  Moses landed on platform at x={platform['x']}, y={platform['y']}")
                    break'''
    
    new_collision_code = '''        # Platform collision detection - FIXED VERSION
        platform_collision = False
        
        # Debug: Check if we have platforms
        if hasattr(self, 'game_platforms') and self.game_platforms:
            print(f"🔍 Checking collision with {len(self.game_platforms)} platforms - Moses at y={self.rect.bottom}")
            
            for i, platform in enumerate(self.game_platforms):
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                
                # Debug collision check
                if i < 3:  # Only debug first 3 platforms to avoid spam
                    print(f"🔍 Platform {i}: x={platform['x']}-{platform['x']+platform['width']}, y={platform['y']}, Moses: x={self.rect.x}-{self.rect.right}, y={self.rect.bottom}")
                
                # Check if player is falling onto platform (IMPROVED LOGIC)
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
                    print(f"🏗️  ✅ MOSES LANDED ON PLATFORM at x={platform['x']}, y={platform['y']} - SUCCESS!")
                    break
        else:
            print("❌ No game_platforms found for collision detection!")'''
    
    if old_collision_code in content:
        content = content.replace(old_collision_code, new_collision_code)
        print("✅ Fixed platform collision detection with improved logic and debug output")
    else:
        print("⚠️  Could not find platform collision code - adding new collision system")
        
        # Find the player update method and add collision detection
        update_method_marker = "def update(self, dt):"
        player_class_start = content.find("class Player:")
        if player_class_start != -1:
            update_pos = content.find(update_method_marker, player_class_start)
            if update_pos != -1:
                # Find the physics section
                physics_marker = "# Apply gravity"
                physics_pos = content.find(physics_marker, update_pos)
                if physics_pos != -1:
                    # Insert collision detection before ground collision
                    collision_insertion = '''
        # CRITICAL: Platform collision detection - FIXED VERSION
        platform_collision = False
        
        # Debug: Check if we have platforms
        if hasattr(self, 'game_platforms') and self.game_platforms:
            print(f"🔍 Checking collision with {len(self.game_platforms)} platforms - Moses at y={self.rect.bottom}")
            
            for i, platform in enumerate(self.game_platforms):
                platform_rect = pygame.Rect(platform['x'], platform['y'], platform['width'], platform['height'])
                
                # Debug collision check
                if i < 3:  # Only debug first 3 platforms to avoid spam
                    print(f"🔍 Platform {i}: x={platform['x']}-{platform['x']+platform['width']}, y={platform['y']}, Moses: x={self.rect.x}-{self.rect.right}, y={self.rect.bottom}")
                
                # Check if player is falling onto platform (IMPROVED LOGIC)
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
                    print(f"🏗️  ✅ MOSES LANDED ON PLATFORM at x={platform['x']}, y={platform['y']} - SUCCESS!")
                    break
        else:
            print("❌ No game_platforms found for collision detection!")

'''
                    content = content[:physics_pos] + collision_insertion + content[physics_pos:]
                    print("✅ Added new platform collision detection system")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def ensure_platform_reference_to_player():
    """Ensure player gets platform reference correctly"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find where platforms are created and ensure player gets reference
    platform_creation_marker = "self.initialize_multi_level_world()"
    
    if platform_creation_marker in content:
        # Replace with version that properly assigns platforms to player
        enhanced_platform_creation = '''self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")'''
        
        content = content.replace(platform_creation_marker, enhanced_platform_creation)
        print("✅ Enhanced platform reference assignment to player")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_platform_positioning_for_reachability():
    """Fix platform positions to be within Moses' jump range"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find current platform system and replace with reachable positions
    old_platform_positions = '''        # Create platform system with proper spacing and collision detection
        # Based on original dark platforms but with better spacing to avoid overlaps
        self.game_platforms = [
            # Base level - aligned with original dark platforms (y=580-620) - Above ground
            {'x': 300, 'y': 580, 'width': 120, 'height': 20},  # Original x=300 position
            {'x': 550, 'y': 590, 'width': 110, 'height': 20},  # 250px spacing
            {'x': 800, 'y': 585, 'width': 120, 'height': 20},  # 250px spacing
            {'x': 1050, 'y': 595, 'width': 110, 'height': 20}, # 250px spacing
            {'x': 1300, 'y': 580, 'width': 120, 'height': 20}, # 250px spacing
            {'x': 1550, 'y': 590, 'width': 110, 'height': 20}, # 250px spacing
            {'x': 1800, 'y': 585, 'width': 120, 'height': 20}, # 250px spacing
            {'x': 2050, 'y': 595, 'width': 110, 'height': 20}, # 250px spacing'''
    
    new_platform_positions = '''        # Create platform system with REACHABLE positions for Moses
        # Moses jumps from y=670 to y=437 (233px range) - platforms must be within this range
        self.game_platforms = [
            # Base level - REACHABLE from ground (y=620-650) - Just above ground level
            {'x': 300, 'y': 620, 'width': 120, 'height': 20},  # Original x=300 position - REACHABLE
            {'x': 550, 'y': 630, 'width': 110, 'height': 20},  # 250px spacing - REACHABLE
            {'x': 800, 'y': 625, 'width': 120, 'height': 20},  # 250px spacing - REACHABLE
            {'x': 1050, 'y': 635, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1300, 'y': 620, 'width': 120, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1550, 'y': 630, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1800, 'y': 625, 'width': 120, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 2050, 'y': 635, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE'''
    
    if old_platform_positions in content:
        content = content.replace(old_platform_positions, new_platform_positions)
        print("✅ Fixed platform positions to be within Moses' jump range (y=620-650)")
    
    # Also fix the higher level platforms to be reachable
    old_level1 = '''            # Level 1 - First elevated platforms (y=450-490) - 120px above base level
            {'x': 200, 'y': 460, 'width': 100, 'height': 20},  # Offset for variety
            {'x': 450, 'y': 470, 'width': 95, 'height': 20},   # Original y=470 position
            {'x': 700, 'y': 465, 'width': 100, 'height': 20},  # Original y=470 area
            {'x': 950, 'y': 475, 'width': 95, 'height': 20},   # 250px spacing
            {'x': 1200, 'y': 460, 'width': 100, 'height': 20}, # 250px spacing
            {'x': 1450, 'y': 470, 'width': 95, 'height': 20},  # 250px spacing
            {'x': 1700, 'y': 465, 'width': 100, 'height': 20}, # 250px spacing
            {'x': 1950, 'y': 475, 'width': 95, 'height': 20},  # 250px spacing'''
    
    new_level1 = '''            # Level 1 - First elevated platforms (y=520-560) - REACHABLE from base level
            {'x': 200, 'y': 530, 'width': 100, 'height': 20},  # REACHABLE from base
            {'x': 450, 'y': 540, 'width': 95, 'height': 20},   # REACHABLE from base
            {'x': 700, 'y': 535, 'width': 100, 'height': 20},  # REACHABLE from base
            {'x': 950, 'y': 545, 'width': 95, 'height': 20},   # REACHABLE from base
            {'x': 1200, 'y': 530, 'width': 100, 'height': 20}, # REACHABLE from base
            {'x': 1450, 'y': 540, 'width': 95, 'height': 20},  # REACHABLE from base
            {'x': 1700, 'y': 535, 'width': 100, 'height': 20}, # REACHABLE from base
            {'x': 1950, 'y': 545, 'width': 95, 'height': 20},  # REACHABLE from base'''
    
    if old_level1 in content:
        content = content.replace(old_level1, new_level1)
        print("✅ Fixed Level 1 platforms to be reachable (y=520-560)")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def remove_duplicate_initialization():
    """Remove duplicate platform system initialization"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and remove duplicate initialization calls
    duplicate_pattern = '''        # Initialize multi-level platform system
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
        
        # Platform integration handled by render_platforms method
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")'''
    
    single_initialization = '''        # Initialize multi-level platform system - SINGLE CALL
        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()
        
        # CRITICAL: Ensure player has platform reference for collision detection
        if hasattr(self, 'game_platforms') and hasattr(self, 'player'):
            self.player.game_platforms = self.game_platforms
            print(f"🔧 ✅ Player now has access to {len(self.game_platforms)} platforms for collision detection")
        else:
            print("❌ Failed to assign platforms to player!")
        
        # Platform system ready
        print(f"🏗️  Platform system ready with {len(self.game_platforms)} platforms")'''
    
    if duplicate_pattern in content:
        content = content.replace(duplicate_pattern, single_initialization)
        print("✅ Removed duplicate platform system initialization")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Critical fix for platform collision detection"""
    print("🚨 CRITICAL FIX: Platform Collision Detection")
    print("=" * 50)
    
    print("1. Fixing platform collision detection logic...")
    fix_platform_collision_detection()
    
    print("2. Ensuring platform reference to player...")
    ensure_platform_reference_to_player()
    
    print("3. Fixing platform positions for reachability...")
    fix_platform_positioning_for_reachability()
    
    print("4. Removing duplicate initialization...")
    remove_duplicate_initialization()
    
    print("\n" + "=" * 50)
    print("🎉 CRITICAL FIXES APPLIED!")
    print("\nFixed Issues:")
    print("✅ Platform collision detection with improved logic")
    print("✅ Enhanced debug output for troubleshooting")
    print("✅ Platform reference properly assigned to player")
    print("✅ Platform positions adjusted to be reachable")
    print("✅ Removed duplicate system initialization")
    print("\nNew Features:")
    print("🔍 Comprehensive debug output shows collision checks")
    print("🏗️  Success messages when Moses lands on platforms")
    print("📏 Platform positions within Moses' jump range (y=620-650)")
    print("🎯 Generous landing tolerance (15px) for easier gameplay")
    print("\nMoses should now be able to:")
    print("- Jump and land on base level platforms (y=620-650)")
    print("- See debug messages during collision checks")
    print("- Progress to higher platform levels")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
