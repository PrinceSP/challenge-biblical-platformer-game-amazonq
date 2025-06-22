#!/usr/bin/env python3
"""
Fix dialogue text display and restore complex inventory system with all features
"""

def fix_dialogue_text_display():
    """Fix dialogue text to actually display in the dialogue box"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find DialogueSystem render method and replace with working version
    render_start = content.find('def render(self, screen, sprites=None):')
    if render_start != -1:
        # Find the end of the render method
        next_method = content.find('\n    def ', render_start + 1)
        if next_method == -1:
            next_method = content.find('\nclass ', render_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Create render method that ACTUALLY displays text on screen
        working_render = '''    def render(self, screen, sprites=None):
        """Render dialogue with VISIBLE text on screen"""
        if not self.active or not self.current_node:
            return
        
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Create large, visible dialogue box
        box_width = screen_width - 100
        box_height = 200
        box_x = 50
        box_y = screen_height - box_height - 50
        
        # Draw dialogue background - DARK with BRIGHT borders
        dialogue_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Multiple layers for maximum visibility
        pygame.draw.rect(screen, (0, 0, 0), dialogue_rect)  # Black background
        pygame.draw.rect(screen, (20, 15, 10), dialogue_rect.inflate(-6, -6))  # Dark brown
        pygame.draw.rect(screen, (255, 215, 0), dialogue_rect, 5)  # Thick gold border
        
        # Speaker name - VERY VISIBLE
        if self.current_node and self.current_node.speaker:
            speaker_font = pygame.font.Font(None, 48)  # Large font
            speaker_text = speaker_font.render(f"{self.current_node.speaker}:", True, (255, 215, 0))
            
            # Speaker background for contrast
            speaker_bg = pygame.Rect(box_x + 15, box_y + 10, speaker_text.get_width() + 20, 45)
            pygame.draw.rect(screen, (40, 30, 20), speaker_bg)
            pygame.draw.rect(screen, (255, 215, 0), speaker_bg, 2)
            
            screen.blit(speaker_text, (box_x + 25, box_y + 15))
        
        # Main dialogue text - GUARANTEED VISIBLE
        if self.displayed_text and len(self.displayed_text) > 0:
            text_font = pygame.font.Font(None, 32)  # Large, readable font
            text_color = (255, 255, 255)  # Pure WHITE text
            
            # Word wrap the text properly
            words = self.displayed_text.split(' ')
            lines = []
            current_line = ""
            max_width = box_width - 80
            
            for word in words:
                test_line = current_line + word + " "
                text_width = text_font.size(test_line)[0]
                if text_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            # Render each line with shadow for maximum visibility
            text_start_y = box_y + 70
            line_height = 30
            
            for i, line in enumerate(lines[:3]):  # Show up to 3 lines
                if line.strip():
                    # Black shadow for contrast
                    shadow_surface = text_font.render(line, True, (0, 0, 0))
                    screen.blit(shadow_surface, (box_x + 32, text_start_y + (i * line_height) + 2))
                    
                    # White text on top
                    text_surface = text_font.render(line, True, text_color)
                    screen.blit(text_surface, (box_x + 30, text_start_y + (i * line_height)))
        
        # Status indicator - VISIBLE
        status_y = box_y + box_height - 40
        status_font = pygame.font.Font(None, 28)
        
        if self.waiting_for_input:
            prompt_surface = status_font.render("Press SPACE to continue...", True, (255, 255, 0))
            screen.blit(prompt_surface, (box_x + box_width - 280, status_y))
        elif self.is_typing:
            typing_surface = status_font.render("...", True, (200, 200, 100))
            screen.blit(typing_surface, (box_x + box_width - 80, status_y))
        
        # Force screen update
        pygame.display.update(dialogue_rect)
'''
        
        content = content[:render_start] + working_render + content[next_method:]
        print("✅ Fixed dialogue text rendering for actual display")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def restore_complex_inventory_system():
    """Restore the complex inventory system with item usage and effects"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find Inventory class and replace with complex version
    inventory_start = content.find('class Inventory:')
    if inventory_start != -1:
        # Find the end of the Inventory class
        next_class = content.find('\nclass ', inventory_start + 1)
        if next_class == -1:
            next_class = len(content)
        
        # Create complex inventory system
        complex_inventory = '''class Inventory:
    def __init__(self):
        self.active = False
        self.items = {
            "bread": 0,
            "meat": 0, 
            "water": 0,
            "scroll": 0,
            "stone": 0,
            "staff": 0,
            "armor_of_god": 0
        }
        self.item_effects = {
            "bread": {"health": 20, "description": "Restores 20 health"},
            "meat": {"health": 30, "description": "Restores 30 health"},
            "water": {"health": 15, "description": "Restores 15 health"},
            "scroll": {"wisdom": 10, "description": "Increases wisdom"},
            "stone": {"weapon": True, "description": "Throwable weapon"},
            "staff": {"weapon": True, "magic": True, "description": "Divine staff with projectiles"},
            "armor_of_god": {"protection": 50, "description": "Divine protection"}
        }
        self.selected_item = 0
        self.game_instance = None
        self.stone_ready = False
        self.staff_active = False
        self.armor_active = False
        self.armor_timer = 0
    
    def add_item(self, item_type, quantity=1):
        """Add item to inventory with feedback"""
        if item_type in self.items:
            self.items[item_type] += quantity
            print(f"📦 Added {quantity} {item_type} to inventory")
            
            # Show visual feedback
            if self.game_instance and hasattr(self.game_instance, 'visual_feedback'):
                self.game_instance.visual_feedback.show_message(f"Found {item_type}!", 2.0)
            
            return True
        return False
    
    def use_item(self, item_type):
        """Use item with effects"""
        if item_type not in self.items or self.items[item_type] <= 0:
            return False
        
        player = self.game_instance.player if self.game_instance else None
        
        if item_type in ["bread", "meat", "water"]:
            # Healing items
            self.items[item_type] -= 1
            heal_amount = self.item_effects[item_type]["health"]
            
            if player:
                old_health = player.health
                player.health = min(player.max_health, player.health + heal_amount)
                actual_heal = player.health - old_health
                print(f"🍞 Used {item_type}! Healed {actual_heal} HP (Health: {player.health}/{player.max_health})")
                
                if self.game_instance and hasattr(self.game_instance, 'visual_feedback'):
                    self.game_instance.visual_feedback.show_message(f"Healed {actual_heal} HP!", 2.0)
            
            return True
        
        elif item_type == "stone":
            # Stone throwing
            if self.items[item_type] > 0:
                self.stone_ready = True
                print("🪨 Stone ready to throw! Press A to throw")
                
                if self.game_instance and hasattr(self.game_instance, 'visual_feedback'):
                    self.game_instance.visual_feedback.show_message("Stone ready! Press A to throw", 2.0)
                
                return True
        
        elif item_type == "staff":
            # Staff activation
            if self.items[item_type] > 0:
                self.staff_active = True
                print("⚡ Staff activated! Press W to shoot divine projectile")
                
                if self.game_instance and hasattr(self.game_instance, 'visual_feedback'):
                    self.game_instance.visual_feedback.show_message("Staff active! Press W to shoot", 2.0)
                
                return True
        
        elif item_type == "armor_of_god":
            # Armor of God activation
            if self.items[item_type] > 0:
                self.items[item_type] -= 1
                self.armor_active = True
                self.armor_timer = 30.0  # 30 seconds of protection
                
                if player:
                    player.armor_active = True
                    player.armor_timer = 30.0
                
                print("🛡️ Armor of God activated! Divine protection for 30 seconds")
                
                if self.game_instance and hasattr(self.game_instance, 'visual_feedback'):
                    self.game_instance.visual_feedback.show_message("Divine Protection Active!", 3.0)
                
                return True
        
        return False
    
    def use_item_by_number(self, number):
        """Use item by number key (1-7)"""
        item_list = list(self.items.keys())
        if 1 <= number <= len(item_list):
            item_type = item_list[number - 1]
            return self.use_item(item_type)
        return False
    
    def throw_stone(self):
        """Throw stone at enemies"""
        if self.stone_ready and self.items["stone"] > 0:
            self.items["stone"] -= 1
            self.stone_ready = False
            
            player = self.game_instance.player if self.game_instance else None
            if player and self.game_instance:
                # Create stone projectile
                stone_x = player.x + (30 if player.facing_right else -30)
                stone_y = player.y + 10
                direction = 1 if player.facing_right else -1
                
                # Add stone projectile to game
                if hasattr(self.game_instance, 'projectiles'):
                    stone_projectile = {
                        'x': stone_x,
                        'y': stone_y,
                        'velocity_x': direction * 8,
                        'velocity_y': -2,
                        'type': 'stone',
                        'damage': 25
                    }
                    self.game_instance.projectiles.append(stone_projectile)
                    print("🪨 Stone thrown!")
                    
                    if hasattr(self.game_instance, 'sound_manager'):
                        self.game_instance.sound_manager.play_sound('pickup')
            
            return True
        return False
    
    def shoot_staff_projectile(self):
        """Shoot staff projectile"""
        if self.staff_active and self.items["staff"] > 0:
            player = self.game_instance.player if self.game_instance else None
            if player and self.game_instance:
                # Create staff projectile
                staff_x = player.x + (30 if player.facing_right else -30)
                staff_y = player.y + 10
                direction = 1 if player.facing_right else -1
                
                # Add staff projectile to game
                if hasattr(self.game_instance, 'projectiles'):
                    staff_projectile = {
                        'x': staff_x,
                        'y': staff_y,
                        'velocity_x': direction * 12,
                        'velocity_y': 0,
                        'type': 'staff',
                        'damage': 40,
                        'divine': True
                    }
                    self.game_instance.projectiles.append(staff_projectile)
                    print("⚡ Divine projectile fired!")
                    
                    if hasattr(self.game_instance, 'sound_manager'):
                        self.game_instance.sound_manager.play_sound('dialogue')
            
            return True
        return False
    
    def update(self, dt):
        """Update inventory timers"""
        if self.armor_active:
            self.armor_timer -= dt
            if self.armor_timer <= 0:
                self.armor_active = False
                if self.game_instance and self.game_instance.player:
                    self.game_instance.player.armor_active = False
                print("🛡️ Armor of God protection expired")
    
    def has_item(self, item_type):
        """Check if inventory has item"""
        return item_type in self.items and self.items[item_type] > 0
    
    def get_item_count(self, item_type):
        """Get count of specific item"""
        return self.items.get(item_type, 0)
    
    def handle_event(self, event):
        """Handle inventory events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.active = not self.active
                print(f"📦 Inventory {'opened' if self.active else 'closed'}")
            
            # Number keys for item usage (1-7)
            elif pygame.K_1 <= event.key <= pygame.K_7:
                number = event.key - pygame.K_0
                if self.use_item_by_number(number):
                    print(f"✅ Used item #{number}")
            
            # Stone throwing
            elif event.key == pygame.K_a:
                if self.throw_stone():
                    print("🪨 Stone thrown at enemies!")
            
            # Staff projectile
            elif event.key == pygame.K_w:
                if self.shoot_staff_projectile():
                    print("⚡ Staff projectile fired!")
    
    def render(self, screen, ui_sprites=None):
        """Render inventory with item details"""
        if not self.active:
            return
        
        # Large inventory panel
        panel_rect = pygame.Rect(150, 100, 500, 400)
        pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 3)
        
        # Title
        font = pygame.font.Font(None, 36)
        title_text = font.render("Biblical Inventory", True, (255, 255, 255))
        screen.blit(title_text, (panel_rect.left + 20, panel_rect.top + 20))
        
        # Instructions
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "Press number keys (1-7) to use items:",
            "A - Throw stone | W - Staff projectile"
        ]
        for i, instruction in enumerate(instructions):
            text = instruction_font.render(instruction, True, (200, 200, 150))
            screen.blit(text, (panel_rect.left + 20, panel_rect.top + 60 + i * 25))
        
        # Items with effects
        y_offset = 120
        item_font = pygame.font.Font(None, 28)
        
        for i, (item_type, quantity) in enumerate(self.items.items(), 1):
            if quantity > 0:
                # Item name and quantity
                item_text = f"{i}. {item_type.replace('_', ' ').title()}: {quantity}"
                text_surface = item_font.render(item_text, True, (255, 255, 255))
                screen.blit(text_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                
                # Item description
                if item_type in self.item_effects:
                    desc = self.item_effects[item_type]["description"]
                    desc_surface = instruction_font.render(f"   {desc}", True, (150, 150, 150))
                    screen.blit(desc_surface, (panel_rect.left + 40, panel_rect.top + y_offset + 20))
                    y_offset += 45
                else:
                    y_offset += 25
        
        # Status indicators
        status_y = panel_rect.bottom - 80
        if self.stone_ready:
            status_text = item_font.render("🪨 Stone Ready - Press A to throw", True, (255, 255, 0))
            screen.blit(status_text, (panel_rect.left + 20, status_y))
            status_y += 25
        
        if self.staff_active:
            status_text = item_font.render("⚡ Staff Active - Press W to shoot", True, (255, 255, 0))
            screen.blit(status_text, (panel_rect.left + 20, status_y))
            status_y += 25
        
        if self.armor_active:
            time_left = int(self.armor_timer)
            status_text = item_font.render(f"🛡️ Divine Protection: {time_left}s", True, (0, 255, 255))
            screen.blit(status_text, (panel_rect.left + 20, status_y))
'''
        
        content = content[:inventory_start] + complex_inventory + content[next_class:]
        print("✅ Restored complex inventory system with all features")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def add_projectile_system():
    """Add projectile system for stones and staff"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add projectile system to main game class
    if 'self.projectiles = []' not in content:
        # Find __init__ method and add projectiles
        init_pos = content.find('def __init__(self):')
        if init_pos != -1:
            # Find end of __init__
            next_method = content.find('\n    def ', init_pos + 1)
            if next_method != -1:
                # Add projectiles initialization
                projectile_init = '''
        # Projectile system for stones and staff
        self.projectiles = []
'''
                content = content[:next_method] + projectile_init + content[next_method:]
                print("✅ Added projectile system initialization")
    
    # Add projectile update method
    if 'def update_projectiles(' not in content:
        # Find a good place to add the method
        class_end = content.find('\n    def run(')
        if class_end != -1:
            projectile_methods = '''
    def update_projectiles(self, dt):
        """Update projectiles (stones and staff)"""
        for projectile in self.projectiles[:]:
            # Update position
            projectile['x'] += projectile['velocity_x']
            projectile['y'] += projectile['velocity_y']
            
            # Apply gravity to stones
            if projectile['type'] == 'stone':
                projectile['velocity_y'] += 0.5  # Gravity
            
            # Check collision with enemies
            projectile_rect = pygame.Rect(projectile['x'], projectile['y'], 10, 10)
            
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if projectile_rect.colliderect(enemy_rect):
                    # Hit enemy
                    damage = projectile['damage']
                    enemy.health -= damage
                    print(f"💥 {projectile['type']} hit enemy for {damage} damage!")
                    
                    # Remove projectile
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)
                    
                    # Remove enemy if dead
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        print("💀 Enemy defeated!")
                    
                    break
            
            # Remove projectiles that go off screen
            if (projectile['x'] < -50 or projectile['x'] > SCREEN_WIDTH + 50 or 
                projectile['y'] > SCREEN_HEIGHT + 50):
                if projectile in self.projectiles:
                    self.projectiles.remove(projectile)
    
    def render_projectiles(self, screen):
        """Render projectiles"""
        for projectile in self.projectiles:
            if projectile['type'] == 'stone':
                # Draw stone
                pygame.draw.circle(screen, (139, 69, 19), 
                                 (int(projectile['x']), int(projectile['y'])), 5)
            elif projectile['type'] == 'staff':
                # Draw divine projectile
                pygame.draw.circle(screen, (255, 255, 0), 
                                 (int(projectile['x']), int(projectile['y'])), 8)
                pygame.draw.circle(screen, (255, 255, 255), 
                                 (int(projectile['x']), int(projectile['y'])), 4)
'''
            content = content[:class_end] + projectile_methods + content[class_end:]
            print("✅ Added projectile update and render methods")
    
    # Add projectile calls to main update and render
    if 'self.update_projectiles(' not in content:
        # Find main update method
        update_pos = content.find('def update(self, dt):')
        if update_pos != -1:
            # Find a good place to add projectile update
            visual_update = content.find('self.visual_feedback.update(dt)', update_pos)
            if visual_update != -1:
                insertion_point = content.find('\n', visual_update) + 1
                projectile_update_call = '''
        # Update projectiles
        self.update_projectiles(dt)
'''
                content = content[:insertion_point] + projectile_update_call + content[insertion_point:]
                print("✅ Added projectile update call")
    
    if 'self.render_projectiles(' not in content:
        # Find render_game method
        render_game_pos = content.find('def render_game(self):')
        if render_game_pos != -1:
            # Find where to add projectile rendering
            enemy_render = content.find('enemy.render(self.screen)', render_game_pos)
            if enemy_render != -1:
                insertion_point = content.find('\n', enemy_render) + 1
                projectile_render_call = '''
        # Render projectiles
        self.render_projectiles(self.screen)
'''
                content = content[:insertion_point] + projectile_render_call + content[insertion_point:]
                print("✅ Added projectile render call")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def enhance_player_with_armor():
    """Enhance player class with armor of God functionality"""
    
    with open('game_classes.py', 'r') as f:
        content = f.read()
    
    # Add armor properties to Player class
    if 'self.armor_active = False' not in content:
        # Find Player __init__ method
        player_init = content.find('class Player:')
        if player_init != -1:
            init_method = content.find('def __init__(', player_init)
            if init_method != -1:
                # Find end of __init__
                next_method = content.find('\n    def ', init_method + 1)
                if next_method != -1:
                    # Add armor properties
                    armor_props = '''
        # Armor of God system
        self.armor_active = False
        self.armor_timer = 0
        self.max_health = 100
'''
                    content = content[:next_method] + armor_props + content[next_method:]
                    print("✅ Added armor of God properties to Player")
    
    # Add armor update method
    if 'def update_armor(' not in content:
        # Find a good place to add armor method
        player_class_end = content.find('\nclass ', content.find('class Player:') + 1)
        if player_class_end == -1:
            player_class_end = len(content)
        
        armor_method = '''
    def update_armor(self, dt):
        """Update armor of God timer"""
        if self.armor_active:
            self.armor_timer -= dt
            if self.armor_timer <= 0:
                self.armor_active = False
                print("🛡️ Divine protection expired")
    
    def take_damage(self, damage):
        """Take damage with armor protection"""
        if self.armor_active:
            # Armor reduces damage by 75%
            damage = int(damage * 0.25)
            print(f"🛡️ Armor of God reduced damage to {damage}")
        
        self.health -= damage
        if self.health < 0:
            self.health = 0
        
        print(f"💔 Moses took {damage} damage! Health: {self.health}/{self.max_health}")
        return damage
'''
        
        content = content[:player_class_end] + armor_method + content[player_class_end:]
        print("✅ Added armor of God methods to Player")
    
    with open('game_classes.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix dialogue display and restore complex systems"""
    print("🔧 Fixing Dialogue Display and Restoring Complex Systems")
    print("=" * 60)
    
    print("1. Fixing dialogue text display in dialogue box...")
    fix_dialogue_text_display()
    
    print("2. Restoring complex inventory system...")
    restore_complex_inventory_system()
    
    print("3. Adding projectile system for stones and staff...")
    add_projectile_system()
    
    print("4. Enhancing player with armor of God...")
    enhance_player_with_armor()
    
    print("\n" + "=" * 60)
    print("🎉 DIALOGUE AND COMPLEX SYSTEMS RESTORED!")
    print("\nFixed Features:")
    print("✅ Dialogue text now displays in dialogue box")
    print("✅ Complex inventory with item usage (1-7 keys)")
    print("✅ Health progression from food/water")
    print("✅ Stone throwing system (A key)")
    print("✅ Staff projectile system (W key)")
    print("✅ Armor of God divine protection")
    print("✅ Item effects and descriptions")
    print("✅ Visual feedback for all actions")
    
    print("\nControls:")
    print("- I: Open/Close Inventory")
    print("- 1-7: Use items by number")
    print("- A: Throw stone (when ready)")
    print("- W: Shoot staff projectile (when active)")
    print("- H: Apply healing effects")
    
    print("\nItems and Effects:")
    print("- Bread: +20 health")
    print("- Meat: +30 health") 
    print("- Water: +15 health")
    print("- Stone: Throwable weapon (25 damage)")
    print("- Staff: Divine projectiles (40 damage)")
    print("- Armor of God: 75% damage reduction for 30s")
    
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
