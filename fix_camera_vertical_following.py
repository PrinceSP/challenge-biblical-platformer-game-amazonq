#!/usr/bin/env python3
"""
Fix camera to add vertical following for platform jumping
"""

def add_vertical_camera_following():
    """Replace the Camera class with vertical following capability"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Find and replace the entire Camera class
    old_camera_class = '''class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.smoothing = 0.1
    
    def follow_player(self, player):
        """Follow the player horizontally only - keep ground at bottom"""
        if not player:
            return
        
        # Only follow player horizontally (like classic platformers)
        self.target_x = player.rect.centerx - SCREEN_WIDTH // 2
        # Keep camera at ground level (no vertical following)
        self.target_y = 0
        
        # Smooth horizontal camera movement
        self.x += (self.target_x - self.x) * self.smoothing
        # No vertical movement - ground stays at bottom
        self.y = 0
        
        # Keep camera within reasonable bounds
        self.x = max(0, min(self.x, SCREEN_WIDTH * 5))  # Allow scrolling up to 5 screen widths
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return (int(self.x), int(self.y))'''
    
    new_camera_class = '''class Camera:
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
        
        # Debug output for camera tracking
        if abs(y_diff) > self.vertical_deadzone:
            print(f"📹 Camera following Moses vertically: player_y={player.rect.centery}, camera_y={self.y}")
    
    def get_offset(self):
        """Get camera offset for rendering"""
        return (int(self.x), int(self.y))'''
    
    if old_camera_class in content:
        content = content.replace(old_camera_class, new_camera_class)
        print("✅ Updated Camera class with vertical following")
    else:
        print("⚠️  Could not find Camera class to update")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def ensure_camera_update_in_game_loop():
    """Ensure camera is updated in the main game loop"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the main game update method
    if "def update(self, dt):" in content:
        # Look for existing camera update
        if "self.camera.follow_player" not in content:
            # Find where to add camera update
            player_update_pos = content.find("self.player.update(dt)")
            if player_update_pos != -1:
                # Add camera update after player update
                insertion_point = content.find('\n', player_update_pos) + 1
                camera_update = '''        
        # Update camera to follow Moses vertically and horizontally
        if hasattr(self, 'camera') and hasattr(self, 'player'):
            self.camera.follow_player(self.player)
'''
                content = content[:insertion_point] + camera_update + content[insertion_point:]
                print("✅ Added camera update to main game loop")
        else:
            print("✅ Camera update already exists in game loop")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix camera to add vertical following"""
    print("📹 Adding Vertical Camera Following")
    print("=" * 35)
    
    print("1. Adding vertical following to Camera class...")
    add_vertical_camera_following()
    
    print("2. Ensuring camera update in game loop...")
    ensure_camera_update_in_game_loop()
    
    print("\n" + "=" * 35)
    print("🎉 VERTICAL CAMERA FOLLOWING ADDED!")
    print("\nCamera Features:")
    print("✅ Follows Moses horizontally (existing)")
    print("✅ Follows Moses vertically when jumping between platforms")
    print("✅ Smooth vertical movement with deadzone (50px)")
    print("✅ Extended vertical range (-500 to +200)")
    print("✅ Debug output shows camera tracking")
    print("✅ Comfortable viewing during platform exploration")
    print("\nCamera Behavior:")
    print("- Horizontal: Smooth following for side-scrolling")
    print("- Vertical: Follows Moses up/down platforms with 50px deadzone")
    print("- Smooth interpolation prevents jarring camera movement")
    print("- Extended range allows full platform exploration")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
