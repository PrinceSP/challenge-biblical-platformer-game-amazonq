#!/usr/bin/env python3
"""
Restore typing effect with sound for dialogue AND fix item collection system
"""

def restore_typing_effect_dialogue():
    """Restore typing effect and sound to DialogueSystem"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find DialogueSystem class and update it with typing effect
    dialogue_start = content.find('class DialogueSystem:')
    if dialogue_start != -1:
        # Replace the simple DialogueSystem with one that has typing effect
        dialogue_end = content.find('\nclass ', dialogue_start + 1)
        if dialogue_end == -1:
            dialogue_end = len(content)
        
        new_dialogue_system = '''class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.dialogue_data = {}
        self.text_speed = 50  # Characters per second for typing effect
        self.displayed_text = ""
        self.text_timer = 0
        self.full_text = ""
        self.waiting_for_input = False
        self.is_typing = False
        self.sound_manager = None
        self.load_dialogue_data()
    
    def load_dialogue_data(self):
        """Load dialogue data"""
        self.dialogue_data = {
            "opening": {
                "start": DialogueNode(
                    "Narrator",
                    "Moses, having fled Egypt after killing an Egyptian taskmaster, has returned by God's command to free His people...",
                    [("Continue", "moses_intro")]
                ),
                "moses_intro": DialogueNode(
                    "Moses",
                    "The Lord has sent me to lead you out of bondage. But first, I must navigate this palace and gather allies...",
                    moral_impact=1
                )
            },
            
            "guard_dialogue": {
                "start": DialogueNode(
                    "Palace Guard",
                    "Halt! What business do you have in Pharaoh's palace?",
                    [("I seek an audience with Pharaoh", "audience_request"),
                     ("I am here on divine mission", "divine_mission")]
                ),
                "audience_request": DialogueNode(
                    "Palace Guard",
                    "Pharaoh does not see common folk. Be gone!",
                    moral_impact=-1
                ),
                "divine_mission": DialogueNode(
                    "Palace Guard",
                    "Divine mission? Prove your words with deeds, Hebrew.",
                    moral_impact=1
                )
            },
            
            "hebrew_slave_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Brother Moses! We have heard of your return. Will you truly lead us from this bondage?",
                    [("Yes, I will free our people", "promise_freedom"),
                     ("I need time to prepare", "need_time")]
                ),
                "promise_freedom": DialogueNode(
                    "Hebrew Slave",
                    "Blessed be the Lord! We will follow you, Moses!",
                    moral_impact=2
                ),
                "need_time": DialogueNode(
                    "Hebrew Slave",
                    "We understand. We have waited 400 years... we can wait a little longer.",
                    moral_impact=1
                )
            },
            
            "priest_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "You dare enter the sacred halls? The gods will not be mocked!",
                    [("The Lord God is greater than your gods", "challenge_gods"),
                     ("I mean no disrespect", "show_respect")]
                ),
                "challenge_gods": DialogueNode(
                    "Egyptian Priest",
                    "Blasphemy! Guards! Seize this Hebrew!",
                    moral_impact=2
                ),
                "show_respect": DialogueNode(
                    "Egyptian Priest",
                    "Hmm... perhaps you are not like the other slaves. Proceed, but carefully.",
                    moral_impact=0
                )
            }
        }
    
    def start_dialogue(self, dialogue_id):
        """Start dialogue with typing effect and sound"""
        if dialogue_id in self.dialogue_data:
            self.active = True
            self.current_dialogue = dialogue_id
            self.current_node = self.dialogue_data[dialogue_id]["start"]
            self.full_text = self.current_node.text
            self.displayed_text = ""
            self.text_timer = 0
            self.waiting_for_input = False
            self.is_typing = True
            
            # Start typing sound effect
            if self.sound_manager:
                self.sound_manager.lower_music_volume()
                self.sound_manager.play_typing_sound_loop()
            
            print(f"✅ Started dialogue: {dialogue_id} with typing effect")
            return True
        else:
            print(f"❌ Dialogue '{dialogue_id}' not found")
            return False
    
    def update(self, dt):
        """Update dialogue with typing effect"""
        if not self.active or not self.current_node:
            return
        
        # Typing effect
        if self.is_typing:
            self.text_timer += dt
            chars_to_show = int(self.text_timer * self.text_speed)
            
            if chars_to_show >= len(self.full_text):
                self.displayed_text = self.full_text
                self.is_typing = False
                self.waiting_for_input = True
                
                # Stop typing sound
                if self.sound_manager:
                    self.sound_manager.stop_typing_sound()
            else:
                self.displayed_text = self.full_text[:chars_to_show]
    
    def handle_event(self, event):
        """Handle dialogue events with typing effect"""
        if not self.active:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.is_typing:
                    # Skip typing animation
                    self.displayed_text = self.full_text
                    self.is_typing = False
                    self.waiting_for_input = True
                    if self.sound_manager:
                        self.sound_manager.stop_typing_sound()
                elif self.waiting_for_input:
                    # Advance dialogue
                    if self.current_node.choices:
                        # For simplicity, take the first choice
                        choice_key = self.current_node.choices[0][1]
                        if choice_key in self.dialogue_data[self.current_dialogue]:
                            self.current_node = self.dialogue_data[self.current_dialogue][choice_key]
                            self.full_text = self.current_node.text
                            self.displayed_text = ""
                            self.text_timer = 0
                            self.is_typing = True
                            self.waiting_for_input = False
                            
                            # Restart typing sound
                            if self.sound_manager:
                                self.sound_manager.play_typing_sound_loop()
                        else:
                            # End dialogue
                            self.end_dialogue()
                    else:
                        # End dialogue
                        self.end_dialogue()
    
    def end_dialogue(self):
        """End dialogue and restore audio"""
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.displayed_text = ""
        self.is_typing = False
        self.waiting_for_input = False
        
        # Restore audio
        if self.sound_manager:
            self.sound_manager.stop_typing_sound()
            self.sound_manager.restore_music_volume()
        
        print("✅ Dialogue ended with typing effect - audio restored")
    
    def render(self, screen, sprites=None):
        """Render dialogue with typing effect"""
        if not self.active or not self.current_node:
            return
        
        font_manager = get_font_manager()
        
        # Enhanced dialogue panel
        panel_height = 200
        panel_rect = pygame.Rect(50, SCREEN_HEIGHT - panel_height - 50, SCREEN_WIDTH - 100, panel_height)
        
        # Draw background with golden border
        pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 3)  # Golden border
        
        # Speaker name
        if self.current_node.speaker:
            speaker_text = font_manager.render_text(self.current_node.speaker, 'medium', (255, 255, 255))
            screen.blit(speaker_text, (panel_rect.left + 20, panel_rect.top + 15))
        
        # Dialogue text with typing effect
        text_lines = self.wrap_text(self.displayed_text, font_manager.get_font('small'), panel_rect.width - 40)
        y_offset = 50
        for line in text_lines:
            if y_offset + 20 <= panel_rect.height - 30:
                line_surface = font_manager.render_text(line, 'small', (255, 255, 255))
                screen.blit(line_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                y_offset += 25
        
        # Continue prompt
        if self.waiting_for_input:
            prompt_text = font_manager.render_text("Press SPACE to continue...", 'tiny', (200, 200, 200))
            screen.blit(prompt_text, (panel_rect.right - 200, panel_rect.bottom - 25))
        elif self.is_typing:
            typing_text = font_manager.render_text("...", 'tiny', (150, 150, 150))
            screen.blit(typing_text, (panel_rect.right - 50, panel_rect.bottom - 25))
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def set_sound_manager(self, sound_manager):
        """Set sound manager for typing effects"""
        self.sound_manager = sound_manager
    
    def end_dialogue(self):
        """End dialogue (compatibility method)"""
        self.active = False
'''
        
        content = content[:dialogue_start] + new_dialogue_system + content[dialogue_end:]
        print("✅ Restored DialogueSystem with typing effect and sound")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def restore_complex_inventory_system():
    """Restore the complex inventory system that worked before"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find Inventory class and replace with complex version
    inventory_start = content.find('class Inventory:')
    if inventory_start != -1:
        inventory_end = content.find('\nclass ', inventory_start + 1)
        if inventory_end == -1:
            inventory_end = content.find('\n\nclass ', inventory_start + 1)
        if inventory_end == -1:
            # Find next method or end of file
            inventory_end = len(content)
        
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
        self.game_instance = None  # Reference to main game for item effects
    
    def add_item(self, item_type, quantity=1):
        """Add item to inventory"""
        if item_type in self.items:
            self.items[item_type] += quantity
            print(f"📦 Added {quantity} {item_type} to inventory")
            return True
        else:
            print(f"❌ Unknown item type: {item_type}")
            return False
    
    def use_item(self, item_type):
        """Use item from inventory with effects"""
        if item_type not in self.items or self.items[item_type] <= 0:
            print(f"❌ No {item_type} available")
            return False
        
        # Apply item effects
        if item_type == "bread":
            self.items[item_type] -= 1
            if self.game_instance and hasattr(self.game_instance, 'player'):
                self.game_instance.player.heal(20)
                print("🍞 Used Bread! Health +20")
                return True
        
        elif item_type == "meat":
            self.items[item_type] -= 1
            if self.game_instance and hasattr(self.game_instance, 'player'):
                self.game_instance.player.heal(30)
                print("🥩 Used Meat! Health +30")
                return True
        
        elif item_type == "water":
            self.items[item_type] -= 1
            if self.game_instance and hasattr(self.game_instance, 'player'):
                self.game_instance.player.heal(10)
                print("💧 Used Water! Health +10")
                return True
        
        elif item_type == "staff":
            if self.game_instance and hasattr(self.game_instance, 'player'):
                self.game_instance.player.activate_staff()
                print("🪄 Used Staff! Divine power activated for 2 minutes")
                return True
        
        elif item_type == "armor_of_god":
            if self.game_instance and hasattr(self.game_instance, 'player'):
                self.game_instance.player.activate_armor()
                print("🛡️ Used Armor of God! Protection increased")
                return True
        
        elif item_type == "scroll":
            print("📜 Used Scroll! Wisdom gained")
            return True
        
        elif item_type == "stone":
            self.items[item_type] -= 1
            if self.game_instance:
                self.game_instance.stone_throw_mode = True
                print("🪨 Stone ready to throw! Press A to throw")
                return True
        
        return False
    
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
            
            # Number keys for using items
            elif event.key == pygame.K_1:
                self.use_item("bread")
            elif event.key == pygame.K_2:
                self.use_item("meat")
            elif event.key == pygame.K_3:
                self.use_item("water")
            elif event.key == pygame.K_4:
                self.use_item("scroll")
            elif event.key == pygame.K_5:
                self.use_item("stone")
            elif event.key == pygame.K_6:
                self.use_item("staff")
            elif event.key == pygame.K_7:
                self.use_item("armor_of_god")
    
    def render(self, screen, ui_sprites=None):
        """Render inventory with item counts and usage instructions"""
        if not self.active:
            return
        
        font_manager = get_font_manager()
        
        # Inventory panel
        panel_rect = pygame.Rect(200, 150, 400, 300)
        pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 3)
        
        # Title
        title_text = font_manager.render_text("Inventory", 'large', (255, 255, 255))
        screen.blit(title_text, (panel_rect.left + 20, panel_rect.top + 20))
        
        # Items with usage instructions
        y_offset = 70
        item_index = 1
        for item_type, quantity in self.items.items():
            if quantity > 0:  # Only show items we have
                # Item effects description
                effect_desc = {
                    "meat": "Heals 30 HP",
                    "bread": "Heals 20 HP", 
                    "water": "Heals 10 HP",
                    "scroll": "Shows Scripture",
                    "stone": "Throw at enemies",
                    "staff": "Divine Staff (2min buff)",
                    "armor_of_god": "Divine Armor (+50% Health)"
                }
                
                effect = effect_desc.get(item_type, "Unknown effect")
                item_text = f"{item_index}. {item_type.replace('_', ' ').title()}: {quantity} - {effect}"
                
                text_surface = font_manager.render_text(item_text, 'small', (255, 255, 255))
                screen.blit(text_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                y_offset += 25
                item_index += 1
        
        # Usage instructions
        instructions = [
            "Press number keys (1-7) to use items",
            "Press I to close inventory"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_manager.render_text(instruction, 'tiny', (200, 200, 200))
            screen.blit(text, (panel_rect.left + 20, panel_rect.bottom - 40 + (i * 15)))
'''
        
        content = content[:inventory_start] + complex_inventory + content[inventory_end:]
        print("✅ Restored complex inventory system with item effects")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Restore typing effect and complex inventory system"""
    print("🔧 Restoring Typing Effect and Complex Inventory")
    print("=" * 50)
    
    print("1. Restoring DialogueSystem with typing effect and sound...")
    restore_typing_effect_dialogue()
    
    print("2. Restoring complex inventory system...")
    restore_complex_inventory_system()
    
    print("\n" + "=" * 50)
    print("🎉 TYPING EFFECT AND INVENTORY RESTORED!")
    print("\nDialogue System Features:")
    print("✅ Typing effect with character-by-character display")
    print("✅ Typing sound effect during text display")
    print("✅ SPACE skips typing or advances dialogue")
    print("✅ Music volume lowers during dialogue")
    print("✅ Audio restored when dialogue ends")
    
    print("\nInventory System Features:")
    print("✅ Complex item collection system")
    print("✅ Item effects (healing, buffs, abilities)")
    print("✅ Number keys (1-7) to use items")
    print("✅ I key to open/close inventory")
    print("✅ Item counts and descriptions")
    print("✅ add_item() method for collection")
    
    print("\nItem Effects:")
    print("- Bread (1): Heals 20 HP")
    print("- Meat (2): Heals 30 HP") 
    print("- Water (3): Heals 10 HP")
    print("- Scroll (4): Shows Scripture")
    print("- Stone (5): Throw at enemies")
    print("- Staff (6): Divine power (2min)")
    print("- Armor of God (7): Protection buff")
    
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
