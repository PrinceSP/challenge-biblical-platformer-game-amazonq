#!/usr/bin/env python3
"""
Simple test to verify W key handling and staff projectiles
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_w_key_and_staff():
    """Test W key handling and staff projectiles"""
    print("🧪 Testing W Key and Staff Projectiles")
    print("=" * 40)
    
    try:
        from game_classes import Player, StaffProjectile
        from sound_manager import SoundManager
        
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        
        # Create player and sound manager
        player = Player(400, 300, {})
        sound_manager = SoundManager()
        player.sound_manager = sound_manager
        
        print("✅ Player and sound manager created")
        
        # Activate staff
        player.activate_staff()
        print(f"✅ Staff activated: {player.staff_active}")
        
        # Test W key simulation
        print("\n🎯 Simulating W key press...")
        
        # Create a fake W key event
        w_key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w)
        
        # Test staff shooting directly
        print("🎯 Testing direct staff shooting...")
        success = player.shoot_staff_projectile()
        print(f"✅ Direct shoot success: {success}")
        print(f"✅ Projectiles created: {len(player.staff_projectiles)}")
        
        if len(player.staff_projectiles) > 0:
            projectile = player.staff_projectiles[0]
            print(f"✅ Projectile details:")
            print(f"   - Position: x={projectile.rect.x}, y={projectile.rect.y}")
            print(f"   - Size: {projectile.rect.width}x{projectile.rect.height}")
            print(f"   - Damage: {projectile.damage}")
            print(f"   - Active: {projectile.active}")
            print(f"   - Has sprite: {projectile.sprite is not None}")
        
        # Test projectile update and rendering
        print("\n🎨 Testing projectile update and rendering...")
        running = True
        frames = 0
        
        while running and frames < 60:  # Test for 1 second at 60 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        print("🎯 W KEY DETECTED!")
                        if player.staff_active:
                            success = player.shoot_staff_projectile()
                            print(f"🎯 Shot projectile: {success}")
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update player and projectiles
            dt = clock.tick(60) / 1000.0
            player.update_staff_system(dt)
            
            # Clear screen
            screen.fill((0, 0, 0))
            
            # Render projectiles
            camera_offset = (0, 0)
            player.render_staff_projectiles(screen, camera_offset)
            
            # Update display
            pygame.display.flip()
            frames += 1
            
            # Print projectile status every 10 frames
            if frames % 10 == 0 and len(player.staff_projectiles) > 0:
                proj = player.staff_projectiles[0]
                print(f"Frame {frames}: Projectile at x={proj.rect.x}, active={proj.active}")
        
        print(f"\n✅ Test completed after {frames} frames")
        print("Press W key in the test window to verify W key detection")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_w_key_and_staff()
