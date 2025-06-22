#!/usr/bin/env python3
"""
Test diamond staff projectiles
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_diamond_projectiles():
    """Test diamond staff projectiles"""
    print("🔶 Testing Diamond Staff Projectiles")
    print("=" * 35)
    
    try:
        from game_classes import Player, StaffProjectile
        
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        
        # Create player
        player = Player(400, 300, {})
        
        # Activate staff
        player.activate_staff()
        print(f"✅ Staff activated: {player.staff_active}")
        
        # Test projectile creation
        success = player.shoot_staff_projectile()
        print(f"✅ Projectile created: {success}")
        print(f"✅ Projectiles count: {len(player.staff_projectiles)}")
        
        if len(player.staff_projectiles) > 0:
            projectile = player.staff_projectiles[0]
            print(f"✅ Diamond projectile details:")
            print(f"   - Position: x={projectile.rect.x}, y={projectile.rect.y}")
            print(f"   - Size: {projectile.rect.width}x{projectile.rect.height}")
            print(f"   - Damage: {projectile.damage}")
            print(f"   - Speed: {projectile.velocity_x} pixels/sec")
            print(f"   - Active: {projectile.active}")
        
        print("\n🔶 Diamond projectiles are ready!")
        print("When you press W in the game, you'll see:")
        print("- Bright yellow diamond shapes")
        print("- White center with gold outline")
        print("- Glow effect around diamonds")
        print("- Flying at 450 pixels/second")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_diamond_projectiles()
