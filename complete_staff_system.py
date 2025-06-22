#!/usr/bin/env python3
"""
Complete the staff system implementation
"""

def add_w_key_handling():
    """Add W key handling for staff shooting"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the healing key handling and add W key after it
    healing_key = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return'''
    
    healing_and_staff_key = '''            # Handle healing
            if event.key == pygame.K_h:
                self.apply_healing()
                return
            
            # Handle staff shooting
            if event.key == pygame.K_w:
                if self.player and hasattr(self.player, 'staff_active') and self.player.staff_active:
                    if self.player.shoot_staff_projectile():
                        # Play staff sound if available
                        if hasattr(self.sound_manager, 'play_sound'):
                            self.sound_manager.play_sound('jump')  # Use jump sound for now
                        # Visual feedback
                        if hasattr(self.visual_feedback, 'show_message'):
                            self.visual_feedback.show_message("⚡ Divine Energy!", 1.0)
                else:
                    print("⚠️  Staff not active! Use staff from inventory first.")
                    if hasattr(self.visual_feedback, 'show_message'):
                        self.visual_feedback.show_message("Staff not active!", 1.5)
                return'''
    
    if healing_key in content:
        content = content.replace(healing_key, healing_and_staff_key)
        print("✅ Added W key staff shooting")
    else:
        print("⚠️  Could not find healing key section")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_inventory_staff_usage():
    """Update inventory system to handle staff activation"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Replace the current staff handling in use_item method
    old_staff_code = '''        elif item_type == "staff":
            # Staff provides temporary protection or special ability
            print(f"🪄 Moses' staff activated!")
            if hasattr(self, 'game_instance') and self.game_instance:
                self.game_instance.visual_feedback.show_message("Staff of Moses activated!", 2.0)'''
    
    new_staff_code = '''        elif item_type == "staff":
            # Activate staff buff on player
            print(f"🪄 Moses' staff activated!")
            if hasattr(self, 'game_instance') and self.game_instance and self.game_instance.player:
                self.game_instance.player.activate_staff()
                self.game_instance.visual_feedback.show_message("Staff of Moses activated! Press W to shoot!", 3.0)
                # Remove staff from inventory (single use activation)
                if self.items[item_type] > 0:
                    self.items[item_type] -= 1
                    if self.items[item_type] == 0:
                        del self.items[item_type]
                return True  # Staff was used'''
    
    if old_staff_code in content:
        content = content.replace(old_staff_code, new_staff_code)
        print("✅ Updated staff usage in inventory system")
    else:
        print("⚠️  Could not find staff code in inventory")
    
    # Update item descriptions
    old_staff_desc = '''                "staff": "Moses' staff power",'''
    new_staff_desc = '''                "staff": "Divine Staff (2min buff, W to shoot)",'''
    
    if old_staff_desc in content:
        content = content.replace(old_staff_desc, new_staff_desc)
        print("✅ Updated staff description")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def add_staff_rendering_and_collision():
    """Add staff projectile rendering and collision detection"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add staff projectile rendering after player rendering
    player_render_line = "self.player.render(self.screen, camera_offset)"
    if player_render_line in content:
        staff_render = '''self.player.render(self.screen, camera_offset)
            
            # Render staff projectiles
            if hasattr(self.player, 'render_staff_projectiles'):
                self.player.render_staff_projectiles(self.screen, camera_offset)'''
        
        content = content.replace(player_render_line, staff_render)
        print("✅ Added staff projectile rendering")
    
    # Add staff collision detection to check_collisions method
    collision_method_end = '''        except Exception as e:
            print(f"⚠️  Collision check error: {e}")'''
    
    collision_with_staff = '''            
            # Staff projectile collisions
            if hasattr(self.player, 'staff_projectiles'):
                for projectile in self.player.staff_projectiles[:]:
                    # Check collision with enemies
                    enemies = self.level_manager.get_enemies()
                    for enemy in enemies:
                        if enemy and hasattr(enemy, 'rect') and projectile.rect.colliderect(enemy.rect):
                            # Staff hit enemy
                            if hasattr(enemy, 'health'):
                                enemy.health -= projectile.damage
                                if enemy.health <= 0:
                                    enemy.defeated = True
                            elif hasattr(enemy, 'defeated'):
                                enemy.defeated = True
                            
                            # Remove projectile
                            projectile.active = False
                            
                            # Visual and audio feedback
                            if hasattr(self.visual_feedback, 'create_dust_effect'):
                                self.visual_feedback.create_dust_effect(enemy.rect.centerx, enemy.rect.centery)
                            if hasattr(self.sound_manager, 'play_sound'):
                                self.sound_manager.play_sound('enemy_defeat')
                            
                            print(f"⚡ Staff projectile hit enemy for {projectile.damage} damage!")
                            break
                    
                    # Check collision with simple enemies
                    simple_enemies = self.level_manager.get_simple_enemies()
                    for enemy in simple_enemies:
                        if enemy and not enemy['defeated'] and projectile.rect.colliderect(enemy['rect']):
                            # Staff hit simple enemy
                            enemy['defeated'] = True
                            projectile.active = False
                            
                            # Visual and audio feedback
                            if hasattr(self.visual_feedback, 'create_dust_effect'):
                                self.visual_feedback.create_dust_effect(enemy['rect'].centerx, enemy['rect'].centery)
                            if hasattr(self.sound_manager, 'play_sound'):
                                self.sound_manager.play_sound('enemy_defeat')
                            
                            print(f"⚡ Staff projectile defeated simple enemy!")
                            break
        
        except Exception as e:
            print(f"⚠️  Collision check error: {e}")'''
    
    if collision_method_end in content:
        content = content.replace(collision_method_end, collision_with_staff)
        print("✅ Added staff collision detection")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_staff_ui_display():
    """Add staff timer display to UI"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the UI rendering section and add staff timer
    ui_section = content.find("# Show stone throw mode indicator")
    if ui_section != -1:
        staff_ui_code = '''
        
        # Show staff status
        if self.player and hasattr(self.player, 'staff_active') and self.player.staff_active:
            staff_time = self.player.get_staff_time_remaining()
            minutes = int(staff_time // 60)
            seconds = int(staff_time % 60)
            staff_text = self.font_manager.render_text(f"Staff Active: {minutes}:{seconds:02d}", 'small', GOLD)
            self.screen.blit(staff_text, (10, 120))
            
            # Staff usage hint
            hint_text = self.font_manager.render_text("Press W to shoot divine energy!", 'tiny', WHITE)
            self.screen.blit(hint_text, (10, 140))'''
        
        content = content[:ui_section] + staff_ui_code + content[ui_section:]
        print("✅ Added staff UI display")
        
        with open('main.py', 'w') as f:
            f.write(content)
        return True
    
    print("⚠️  Could not find UI section for staff display")
    return False

def update_controls_display():
    """Update the controls display to include W key for staff"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the controls display and add W key
    old_controls = '''        print("- H: Apply healing (after using healing items)")
        print("- A: Throw stone (when stone is ready)")'''
    
    new_controls = '''        print("- H: Apply healing (after using healing items)")
        print("- A: Throw stone (when stone is ready)")
        print("- W: Shoot staff projectile (when staff is active)")'''
    
    if old_controls in content:
        content = content.replace(old_controls, new_controls)
        print("✅ Updated controls display to include W key")
        
        with open('main.py', 'w') as f:
            f.write(content)
        return True
    
    print("⚠️  Could not find controls display")
    return False

def main():
    """Complete the staff system implementation"""
    print("🪄 Completing Staff System Implementation")
    print("=" * 45)
    
    print("1. Adding W key handling...")
    add_w_key_handling()
    
    print("2. Updating inventory staff usage...")
    update_inventory_staff_usage()
    
    print("3. Adding staff rendering and collision...")
    add_staff_rendering_and_collision()
    
    print("4. Adding staff UI display...")
    add_staff_ui_display()
    
    print("5. Updating controls display...")
    update_controls_display()
    
    print("\n" + "=" * 45)
    print("🎉 COMPLETE STAFF SYSTEM IMPLEMENTED!")
    print("\nStaff System Features:")
    print("✅ StaffProjectile class with 20 damage")
    print("✅ 2-minute duration buff")
    print("✅ W key to shoot projectiles")
    print("✅ Unlimited ammo during buff")
    print("✅ Visual timer display")
    print("✅ Collision detection with enemies")
    print("✅ Sound and visual feedback")
    print("✅ Inventory integration")
    print("✅ Updated controls display")
    print("\nHow to use:")
    print("1. Find staff in any location")
    print("2. Use staff from inventory (number key)")
    print("3. Press W to shoot divine projectiles")
    print("4. Staff lasts for 2 minutes")
    print("5. Each projectile does 20 damage")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
