#!/usr/bin/env python3
"""
Fix platform height spacing and add vertical camera following
"""

def increase_platform_height_spacing():
    """Increase height between old platforms and new platforms for better spacing"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the current platform system and increase height spacing
    old_platform_system = '''        # Create platform system with INCREASED SPACING and HIGHER POSITIONING
        # Old platforms are around y=608-670, new platforms positioned well above them
        # 400px horizontal spacing, 140px vertical spacing between levels
        self.game_platforms = [
            # Base level - HIGHER above old platforms (y=550-580) - Clear separation
            {'x': 400, 'y': 560, 'width': 120, 'height': 20},   # 400px spacing between platforms
            {'x': 800, 'y': 570, 'width': 110, 'height': 20},   # 400px spacing - no overlap
            {'x': 1200, 'y': 565, 'width': 120, 'height': 20},  # 400px spacing - clear separation
            {'x': 1600, 'y': 575, 'width': 110, 'height': 20},  # 400px spacing - well spaced
            {'x': 2000, 'y': 560, 'width': 120, 'height': 20},  # 400px spacing - good distance
            {'x': 2400, 'y': 570, 'width': 110, 'height': 20},  # 400px spacing - final base platform
            
            # Level 1 - First elevated platforms (y=420-460) - 140px above base level
            {'x': 300, 'y': 430, 'width': 100, 'height': 20},   # Offset start, 400px spacing
            {'x': 700, 'y': 440, 'width': 95, 'height': 20},    # 400px spacing - good distance
            {'x': 1100, 'y': 435, 'width': 100, 'height': 20},  # 400px spacing - clear separation
            {'x': 1500, 'y': 445, 'width': 95, 'height': 20},   # 400px spacing - well spaced
            {'x': 1900, 'y': 430, 'width': 100, 'height': 20},  # 400px spacing - good distance
            {'x': 2300, 'y': 440, 'width': 95, 'height': 20},   # 400px spacing - final level 1
            
            # Level 2 - Second elevated platforms (y=280-320) - 140px above Level 1
            {'x': 200, 'y': 290, 'width': 85, 'height': 20},    # Offset start, 400px spacing
            {'x': 600, 'y': 300, 'width': 90, 'height': 20},    # 400px spacing - good distance
            {'x': 1000, 'y': 295, 'width': 85, 'height': 20},   # 400px spacing - clear separation
            {'x': 1400, 'y': 305, 'width': 90, 'height': 20},   # 400px spacing - well spaced
            {'x': 1800, 'y': 290, 'width': 85, 'height': 20},   # 400px spacing - good distance
            {'x': 2200, 'y': 300, 'width': 90, 'height': 20},   # 400px spacing - final level 2
            
            # Level 3 - Third elevated platforms (y=140-180) - 140px above Level 2
            {'x': 500, 'y': 150, 'width': 75, 'height': 20},    # Centered start, 400px spacing
            {'x': 900, 'y': 160, 'width': 80, 'height': 20},    # 400px spacing - good distance
            {'x': 1300, 'y': 155, 'width': 75, 'height': 20},   # 400px spacing - clear separation
            {'x': 1700, 'y': 165, 'width': 80, 'height': 20},   # 400px spacing - well spaced
            {'x': 2100, 'y': 150, 'width': 75, 'height': 20},   # 400px spacing - final level 3
            
            # Level 4 - Top platforms (y=20-60) - 120px above Level 3 - Ultimate challenge
            {'x': 700, 'y': 30, 'width': 70, 'height': 20},     # Centered, 500px spacing
            {'x': 1200, 'y': 40, 'width': 75, 'height': 20},    # 500px spacing - maximum challenge
            {'x': 1700, 'y': 35, 'width': 70, 'height': 20},    # 500px spacing - expert level
        ]'''
    
    # Create new platform system with much more height spacing
    new_platform_system = '''        # Create platform system with MUCH MORE HEIGHT SPACING from old platforms
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
        ]'''
    
    if old_platform_system in content:
        content = content.replace(old_platform_system, new_platform_system)
        print("✅ Increased height spacing between old and new platforms")
    else:
        print("⚠️  Could not find platform system to update")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_vertical_camera_following():
    """Add vertical camera following to track Moses as he jumps between platforms"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find the Camera class and enhance it with vertical following
    camera_class_marker = "class Camera:"
    camera_pos = content.find(camera_class_marker)
    
    if camera_pos != -1:
        # Find the Camera update method
        update_method_marker = "def update(self, target_rect):"
        update_pos = content.find(update_method_marker, camera_pos)
        
        if update_pos != -1:
            # Find the end of the current update method
            next_method = content.find("\n    def ", update_pos + 1)
            if next_method == -1:
                next_method = content.find("\nclass ", update_pos + 1)
            
            if next_method != -1:
                # Replace the current update method with vertical following
                old_update_method = content[update_pos:next_method]
                
                new_update_method = '''    def update(self, target_rect):
        """Update camera position to follow target with VERTICAL FOLLOWING"""
        # Horizontal following (existing)
        self.x = target_rect.centerx - SCREEN_WIDTH // 2
        
        # VERTICAL FOLLOWING - Camera follows Moses up and down platforms
        target_y = target_rect.centery - SCREEN_HEIGHT // 2
        
        # Smooth vertical camera movement
        camera_speed = 3.0  # Adjust for smoother/faster camera movement
        y_diff = target_y - self.y
        
        if abs(y_diff) > 10:  # Only move camera if significant vertical movement
            self.y += y_diff * camera_speed * 0.016  # Smooth interpolation (assuming 60fps)
        
        # Clamp camera to reasonable bounds
        # Allow camera to go higher for platform exploration
        self.y = max(-400, min(self.y, SCREEN_HEIGHT - 100))  # Extended vertical range
        
        print(f"📹 Camera following Moses: target_y={target_rect.centery}, camera_y={self.y}")
'''
                
                content = content[:update_pos] + new_update_method + content[next_method:]
                print("✅ Added vertical camera following to Camera class")
    
    # Also enhance the camera update call in the main game loop
    if "self.camera.update(self.player.rect)" in content:
        # The camera update call is already there, just need to make sure it's called frequently
        print("✅ Camera update call already exists")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def enhance_camera_integration():
    """Ensure camera is properly integrated with the game loop"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the game update method and ensure camera is updated
    if "def update(self, dt):" in content:
        # Look for camera update in the main game update
        if "self.camera.update" not in content:
            # Find where to add camera update
            update_method_pos = content.find("def update(self, dt):")
            if update_method_pos != -1:
                # Find the player update line
                player_update_pos = content.find("self.player.update(dt)", update_method_pos)
                if player_update_pos != -1:
                    # Add camera update after player update
                    insertion_point = content.find('\n', player_update_pos) + 1
                    camera_update = '''        
        # Update camera to follow Moses vertically and horizontally
        if hasattr(self, 'camera') and hasattr(self, 'player'):
            self.camera.update(self.player.rect)
'''
                    content = content[:insertion_point] + camera_update + content[insertion_point:]
                    print("✅ Added camera update to main game loop")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_items_for_new_heights():
    """Update item positions to match the new platform heights"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and update item positions for new platform heights
    old_items = '''        # Create strategic items on NEW SPACED platforms (positioned on platform centers)
        self.game_items = [
            # Base level items (y=550-580) - On well-spaced platforms
            {'x': 460, 'y': 540, 'type': 'stone'},      # On platform at x=400
            {'x': 860, 'y': 550, 'type': 'water'},      # On platform at x=800
            {'x': 1260, 'y': 545, 'type': 'bread'},     # On platform at x=1200
            {'x': 1660, 'y': 555, 'type': 'scroll'},    # On platform at x=1600
            {'x': 2060, 'y': 540, 'type': 'meat'},      # On platform at x=2000
            {'x': 2460, 'y': 550, 'type': 'armor_of_god'}, # On platform at x=2400
            
            # Level 1 items (y=420-460) - On elevated platforms
            {'x': 360, 'y': 410, 'type': 'water'},      # On platform at x=300
            {'x': 760, 'y': 420, 'type': 'bread'},      # On platform at x=700
            {'x': 1160, 'y': 415, 'type': 'scroll'},    # On platform at x=1100
            {'x': 1560, 'y': 425, 'type': 'meat'},      # On platform at x=1500
            {'x': 1960, 'y': 410, 'type': 'armor_of_god'}, # On platform at x=1900
            {'x': 2360, 'y': 420, 'type': 'staff'},     # On platform at x=2300
            
            # Level 2 items (y=280-320) - On higher platforms
            {'x': 260, 'y': 270, 'type': 'scroll'},     # On platform at x=200
            {'x': 660, 'y': 280, 'type': 'meat'},       # On platform at x=600
            {'x': 1060, 'y': 275, 'type': 'armor_of_god'}, # On platform at x=1000
            {'x': 1460, 'y': 285, 'type': 'staff'},     # On platform at x=1400
            {'x': 1860, 'y': 270, 'type': 'stone'},     # On platform at x=1800
            {'x': 2260, 'y': 280, 'type': 'water'},     # On platform at x=2200
            
            # Level 3 items (y=140-180) - On challenging platforms
            {'x': 560, 'y': 130, 'type': 'armor_of_god'}, # On platform at x=500
            {'x': 960, 'y': 140, 'type': 'staff'},      # On platform at x=900
            {'x': 1360, 'y': 135, 'type': 'meat'},      # On platform at x=1300
            {'x': 1760, 'y': 145, 'type': 'scroll'},    # On platform at x=1700
            {'x': 2160, 'y': 130, 'type': 'stone'},     # On platform at x=2100
            
            # Level 4 items (y=20-60) - Premium rewards on top platforms
            {'x': 760, 'y': 10, 'type': 'staff'},       # On platform at x=700 - Ultimate reward
            {'x': 1260, 'y': 20, 'type': 'armor_of_god'}, # On platform at x=1200 - Ultimate reward
            {'x': 1760, 'y': 15, 'type': 'meat'},       # On platform at x=1700 - Ultimate reward
        ]'''
    
    new_items = '''        # Create strategic items on HIGHER SPACED platforms (positioned on platform centers)
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
        ]'''
    
    if old_items in content:
        content = content.replace(old_items, new_items)
        print("✅ Updated item positions for new platform heights")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix platform height spacing and add vertical camera following"""
    print("🏗️  Fixing Platform Height and Adding Vertical Camera Following")
    print("=" * 65)
    
    print("1. Increasing height spacing between old and new platforms...")
    increase_platform_height_spacing()
    
    print("2. Adding vertical camera following...")
    add_vertical_camera_following()
    
    print("3. Enhancing camera integration...")
    enhance_camera_integration()
    
    print("4. Updating item positions for new heights...")
    update_items_for_new_heights()
    
    print("\n" + "=" * 65)
    print("🎉 PLATFORM HEIGHT AND CAMERA FOLLOWING FIXED!")
    print("\nHeight Spacing Improvements:")
    print("✅ Base platforms moved to y=480-520 (88-128px above old platforms)")
    print("✅ Level 1 platforms at y=320-360 (160px above base)")
    print("✅ Level 2 platforms at y=160-200 (160px above Level 1)")
    print("✅ Level 3 platforms at y=20-60 (140px above Level 2)")
    print("✅ Much clearer separation from old platforms")
    print("\nVertical Camera Following:")
    print("✅ Camera now follows Moses vertically as he jumps")
    print("✅ Smooth camera interpolation for comfortable viewing")
    print("✅ Extended vertical range for platform exploration")
    print("✅ Camera bounds prevent excessive movement")
    print("✅ Debug output shows camera tracking")
    print("\nNew Platform Layout:")
    print("🏠 Base Level (y=480-520): 6 platforms - Much higher above old platforms")
    print("🏢 Level 1 (y=320-360): 6 platforms - 160px above base")
    print("🏔️  Level 2 (y=160-200): 6 platforms - 160px above Level 1")
    print("⛰️  Level 3 (y=20-60): 5 platforms - 140px above Level 2")
    print("\nCamera Features:")
    print("- Follows Moses up and down as he jumps between platforms")
    print("- Smooth movement prevents jarring camera changes")
    print("- Extended vertical range for full platform exploration")
    print("- Maintains horizontal following for side-scrolling")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
