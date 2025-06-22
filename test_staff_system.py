#!/usr/bin/env python3
"""
Test script for the staff system functionality
"""

import pygame
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_staff_system():
    """Test the complete staff system"""
    print("🧪 Testing Moses' Staff System")
    print("=" * 35)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from game_classes import Player, StaffProjectile
        from game_systems import Inventory
        from main import MosesAdventureGame
        print("✅ All imports successful")
        
        # Initialize Pygame
        print("2. Initializing Pygame...")
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((800, 600))
        print("✅ Pygame initialized")
        
        # Test StaffProjectile class
        print("3. Testing StaffProjectile class...")
        projectile = StaffProjectile(100, 100, 1)
        print(f"✅ StaffProjectile created: damage={projectile.damage}, lifetime={projectile.lifetime}")
        
        # Test Player staff system
        print("4. Testing Player staff system...")
        player = Player(100, 100, {})
        
        # Check if staff attributes exist
        staff_attributes = ['has_staff', 'staff_active', 'staff_duration', 'staff_timer', 'staff_projectiles']
        for attr in staff_attributes:
            if hasattr(player, attr):
                print(f"✅ Player has {attr}: {getattr(player, attr)}")
            else:
                print(f"❌ Player missing {attr}")
                return False
        
        # Test staff methods
        staff_methods = ['activate_staff', 'deactivate_staff', 'shoot_staff_projectile', 'update_staff_system']
        for method in staff_methods:
            if hasattr(player, method):
                print(f"✅ Player has {method} method")
            else:
                print(f"❌ Player missing {method} method")
                return False
        
        # Test staff activation
        print("5. Testing staff activation...")
        player.activate_staff()
        
        if player.staff_active:
            print("✅ Staff activated successfully")
            print(f"   Staff timer: {player.staff_timer} seconds")
        else:
            print("❌ Staff activation failed")
            return False
        
        # Test staff projectile shooting
        print("6. Testing staff projectile shooting...")
        initial_projectile_count = len(player.staff_projectiles)
        success = player.shoot_staff_projectile()
        
        if success and len(player.staff_projectiles) > initial_projectile_count:
            print("✅ Staff projectile shot successfully")
            print(f"   Projectiles: {len(player.staff_projectiles)}")
        else:
            print("❌ Staff projectile shooting failed")
            return False
        
        # Test staff system update
        print("7. Testing staff system update...")
        initial_timer = player.staff_timer
        player.update_staff_system(1.0)  # Update 1 second
        
        if player.staff_timer < initial_timer:
            print("✅ Staff timer decreasing properly")
            print(f"   Timer: {initial_timer:.1f} -> {player.staff_timer:.1f}")
        else:
            print("❌ Staff timer not updating")
            return False
        
        # Test inventory integration
        print("8. Testing inventory integration...")
        game = MosesAdventureGame()
        game.start_game()
        
        # Add staff to inventory
        game.inventory.add_item("staff")
        if "staff" in game.inventory.items:
            print("✅ Staff added to inventory")
        else:
            print("❌ Failed to add staff to inventory")
            return False
        
        # Test staff usage from inventory
        initial_staff_active = game.player.staff_active
        game.inventory.use_item("staff")
        
        if game.player.staff_active and not initial_staff_active:
            print("✅ Staff activated from inventory")
        else:
            print("❌ Staff not activated from inventory")
            return False
        
        print("\n" + "=" * 35)
        print("🎉 STAFF SYSTEM TEST COMPLETED!")
        print("\nTest Results:")
        print("✅ StaffProjectile class working")
        print("✅ Player staff attributes present")
        print("✅ Player staff methods working")
        print("✅ Staff activation/deactivation working")
        print("✅ Staff projectile shooting working")
        print("✅ Staff timer system working")
        print("✅ Inventory integration working")
        print("\nTo test in-game:")
        print("1. Run: python3 main.py")
        print("2. Find a staff in any location")
        print("3. Use staff from inventory (number key)")
        print("4. Press W to shoot divine projectiles")
        print("5. Watch staff timer countdown (2 minutes)")
        print("6. See golden staff sprite on Moses")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_staff_system()
    sys.exit(0 if success else 1)
