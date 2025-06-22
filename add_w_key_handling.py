#!/usr/bin/env python3
"""
Add proper W key handling for staff projectiles
"""

def add_w_key_handling():
    """Add W key handling after the healing key handling"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the healing key handling and add W key after it
    healing_section = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return
            

            

            
            if event.key == pygame.K_i:'''
    
    healing_and_staff_section = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return
            
            # Handle staff shooting - COMPREHENSIVE DEBUG VERSION
            if event.key == pygame.K_w:
                print("🎯 W KEY PRESSED!")
                if self.player:
                    print(f"🎯 Player exists: {self.player is not None}")
                    if hasattr(self.player, 'staff_active'):
                        print(f"🎯 Staff active: {self.player.staff_active}")
                        if self.player.staff_active:
                            print("🎯 Attempting to shoot staff projectile...")
                            success = self.player.shoot_staff_projectile()
                            print(f"🎯 Shoot success: {success}")
                            if success:
                                # Play staff sound if available
                                if hasattr(self.sound_manager, 'play_sound'):
                                    self.sound_manager.play_sound('jump')
                                # Visual feedback
                                if hasattr(self.visual_feedback, 'show_message'):
                                    self.visual_feedback.show_message("⚡ Divine Energy!", 1.0)
                                print("🎯 Staff projectile should be created and visible!")
                            else:
                                print("❌ Failed to shoot staff projectile")
                        else:
                            print("❌ Staff not active! Use staff from inventory first.")
                            if hasattr(self.visual_feedback, 'show_message'):
                                self.visual_feedback.show_message("Staff not active!", 1.5)
                    else:
                        print("❌ Player has no staff_active attribute")
                else:
                    print("❌ No player found")
                return
            
            if event.key == pygame.K_i:'''
    
    if healing_section in content:
        content = content.replace(healing_section, healing_and_staff_section)
        print("✅ Added W key handling for staff shooting")
        
        with open('main.py', 'w') as f:
            f.write(content)
        return True
    else:
        print("⚠️  Could not find healing section to add W key handling")
        return False

def main():
    """Add W key handling"""
    print("🔧 Adding W Key Handling for Staff")
    print("=" * 35)
    
    if add_w_key_handling():
        print("\n✅ W KEY HANDLING ADDED!")
        print("\nNow when you press W:")
        print("- Debug messages will show W key press")
        print("- Staff projectile creation will be logged")
        print("- Sparkle sprites should appear and fly")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Failed to add W key handling")

if __name__ == "__main__":
    main()
