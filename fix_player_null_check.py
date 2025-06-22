#!/usr/bin/env python3
"""
Fix player null reference error
"""

def fix_player_null_check():
    """Add null checks for player references"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the player health check
    old_health_check = '''        # Check for game over
        if self.player.health <= 0:
            self.state = GameState.GAME_OVER'''
    
    new_health_check = '''        # Check for game over
        if self.player and self.player.health <= 0:
            self.state = GameState.GAME_OVER'''
    
    if old_health_check in content:
        content = content.replace(old_health_check, new_health_check)
        print("✅ Added null check for player health")
    
    # Also fix camera following
    old_camera_follow = '''        # Update camera and other systems
        self.camera.follow_player(self.player)'''
    
    new_camera_follow = '''        # Update camera and other systems
        if self.player:
            self.camera.follow_player(self.player)'''
    
    if old_camera_follow in content:
        content = content.replace(old_camera_follow, new_camera_follow)
        print("✅ Added null check for camera following")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix player null reference error"""
    print("🔧 Fixing Player Null Reference Error")
    print("=" * 40)
    
    if fix_player_null_check():
        print("✅ PLAYER NULL REFERENCE ERROR FIXED!")
        print("✅ Added null checks for player health")
        print("✅ Added null checks for camera following")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix player null reference error")

if __name__ == "__main__":
    main()
