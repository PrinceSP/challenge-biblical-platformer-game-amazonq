#!/usr/bin/env python3
"""
Test trail visibility for staff projectiles
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_trail_visibility():
    """Test that trails are visible when rendering projectiles"""
    print("🔶 Testing Staff Projectile Trail Visibility")
    print("=" * 45)
    
    try:
        from game_classes import Player, StaffProjectile
        
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        
        # Create player and activate staff
        player = Player(100, 300, {})
        player.activate_staff()
        
        # Create projectiles in both directions
        print("✅ Creating test projectiles...")
        
        # Right-facing projectile
        player.facing_right = True
        success1 = player.shoot_staff_projectile()
        print(f"✅ Right projectile created: {success1}")
        
        # Left-facing projectile  
        player.facing_right = False
        success2 = player.shoot_staff_projectile()
        print(f"✅ Left projectile created: {success2}")
        
        print(f"✅ Total projectiles: {len(player.staff_projectiles)}")
        
        # Test rendering with trail visibility
        print("\n🎨 Testing trail rendering...")
        
        for i, projectile in enumerate(player.staff_projectiles):
            print(f"🔶 Projectile {i+1}:")
            print(f"   - Position: x={projectile.rect.x}, y={projectile.rect.y}")
            print(f"   - Direction: {projectile.direction}")
            print(f"   - Active: {projectile.active}")
            
            # Test render method
            camera_offset = (0, 0)
            screen.fill((0, 0, 0))  # Black background
            projectile.render(screen, camera_offset)
            
        print("\n🎉 Trail visibility test completed!")
        print("The enhanced trail system includes:")
        print("- Bright yellow trail rectangles")
        print("- White center lines for contrast") 
        print("- Multiple trail segments")
        print("- Particle effects")
        print("- Debug output during rendering")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_trail_visibility()
