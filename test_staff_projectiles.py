#!/usr/bin/env python3
"""
Simple test for staff projectiles
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_staff_projectiles():
    """Test staff projectile creation and rendering"""
    print("🧪 Testing Staff Projectiles")
    print("=" * 30)
    
    try:
        from game_classes import Player, StaffProjectile
        from sound_manager import SoundManager
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((800, 600))
        
        # Create player and sound manager
        player = Player(100, 100, {})
        sound_manager = SoundManager()
        player.sound_manager = sound_manager
        
        print("✅ Player and sound manager created")
        
        # Test staff activation
        player.activate_staff()
        print(f"✅ Staff active: {player.staff_active}")
        
        # Test projectile creation
        print("\n🎯 Testing projectile creation:")
        success = player.shoot_staff_projectile()
        print(f"✅ Projectile shot success: {success}")
        print(f"✅ Projectiles count: {len(player.staff_projectiles)}")
        
        if len(player.staff_projectiles) > 0:
            projectile = player.staff_projectiles[0]
            print(f"✅ Projectile position: x={projectile.rect.x}, y={projectile.rect.y}")
            print(f"✅ Projectile damage: {projectile.damage}")
            print(f"✅ Projectile active: {projectile.active}")
        
        # Test projectile update
        print("\n⏱️ Testing projectile update:")
        if len(player.staff_projectiles) > 0:
            old_x = player.staff_projectiles[0].rect.x
            player.update_staff_system(0.1)  # Update for 0.1 seconds
            new_x = player.staff_projectiles[0].rect.x
            print(f"✅ Projectile moved from x={old_x} to x={new_x}")
        
        # Test projectile rendering
        print("\n🎨 Testing projectile rendering:")
        camera_offset = (0, 0)
        player.render_staff_projectiles(screen, camera_offset)
        
        print("\n" + "=" * 30)
        print("🎉 STAFF PROJECTILE TEST COMPLETED!")
        print("\nThe staff projectiles should now:")
        print("- Be created when pressing W")
        print("- Be bright and visible")
        print("- Move across the screen")
        print("- Have debug output showing their status")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_staff_projectiles()
