"""
Game Systems for Moses Adventure - Clean Working Version
"""

import pygame
from constants import *

class DialogueNode:
    def __init__(self, speaker, text, choices=None, moral_impact=0):
        self.speaker = speaker
        self.text = text
        self.choices = choices or []
        self.moral_impact = moral_impact

class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.dialogue_data = {}
        self.text_speed = 30
        self.displayed_text = ""
        self.text_timer = 0
        self.full_text = ""
        self.waiting_for_input = False
        self.is_typing = False
        self.sound_manager = None
        self.load_dialogue_data()
    
    def load_dialogue_data(self):
        self.dialogue_data = {
            "opening": {
                "start": DialogueNode(
                    "Narrator",
                    "Moses, having fled Egypt after killing an Egyptian taskmaster, has returned by God's command to free His people from bondage.",
                    [("Continue", "moses_intro")]
                ),
                "moses_intro": DialogueNode(
                    "Moses",
                    "The Lord has sent me to lead you out of bondage. But first, I must navigate this palace and gather allies for the great exodus.",
                    moral_impact=1
                )
            },
            "guard_dialogue": {
                "start": DialogueNode(
                    "Palace Guard",
                    "Halt! What business do you have in Pharaoh's palace, Hebrew?",
                    [("I seek an audience with Pharaoh", "audience_request")]
                ),
                "audience_request": DialogueNode(
                    "Palace Guard",
                    "Pharaoh does not see common folk. Be gone from here!",
                    moral_impact=-1
                )
            },
            "slave_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Brother Moses! We have heard of your return. Will you truly lead us from this bondage?",
                    [("Yes, I will free our people", "promise_freedom")]
                ),
                "promise_freedom": DialogueNode(
                    "Hebrew Slave",
                    "Blessed be the Lord! We will follow you, Moses!",
                    moral_impact=2
                )
            }
        }
    
    def start_dialogue(self, dialogue_id):
        if dialogue_id in self.dialogue_data:
            self.active = True
            self.current_dialogue = dialogue_id
            self.current_node = self.dialogue_data[dialogue_id]["start"]
            self.full_text = self.current_node.text
            self.displayed_text = ""
            self.text_timer = 0
            self.waiting_for_input = False
            self.is_typing = True
            
            if self.sound_manager:
                self.sound_manager.lower_music_volume()
                self.sound_manager.play_typing_sound_loop()
            
            print(f"✅ Started dialogue: {dialogue_id}")
            print(f"🎭 Full text ready: '{self.full_text}'")
            print(f"🎭 Speaker: {self.current_node.speaker}")
            return True
        return False
    
    def update(self, dt):
        if not self.active or not self.current_node:
            return
        
        if not self.full_text:
            self.full_text = self.current_node.text
        
        if self.is_typing and self.full_text:
            self.text_timer += dt
            chars_to_show = int(self.text_timer * self.text_speed)
            
            if chars_to_show >= len(self.full_text):
                self.displayed_text = self.full_text
                self.is_typing = False
                self.waiting_for_input = True
                
                if self.sound_manager:
                    self.sound_manager.stop_typing_sound()
                
                print(f"🎭 TYPING COMPLETE: '{self.displayed_text}'")
            else:
                self.displayed_text = self.full_text[:chars_to_show]
                print(f"🎭 TYPING: '{self.displayed_text}' ({chars_to_show}/{len(self.full_text)})")
    
    def handle_event(self, event):
        if not self.active:
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.is_typing:
                    self.displayed_text = self.full_text
                    self.is_typing = False
                    self.waiting_for_input = True
                    if self.sound_manager:
                        self.sound_manager.stop_typing_sound()
                    print("🎭 Skipped typing animation")
                elif self.waiting_for_input:
                    if self.current_node.choices:
                        choice_key = self.current_node.choices[0][1]
                        if choice_key in self.dialogue_data[self.current_dialogue]:
                            self.current_node = self.dialogue_data[self.current_dialogue][choice_key]
                            self.full_text = self.current_node.text
                            self.displayed_text = ""
                            self.text_timer = 0
                            self.is_typing = True
                            self.waiting_for_input = False
                            
                            if self.sound_manager:
                                self.sound_manager.play_typing_sound_loop()
                            print("🎭 Advanced to next dialogue")
                        else:
                            self.end_dialogue()
                    else:
                        self.end_dialogue()
    
    def end_dialogue(self):
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.displayed_text = ""
        self.is_typing = False
        self.waiting_for_input = False
        
        if self.sound_manager:
            self.sound_manager.stop_typing_sound()
            self.sound_manager.restore_music_volume()
        
        print("✅ Dialogue ended with typing effect - audio restored")
    
    def render(self, screen, sprites=None):
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

    def set_sound_manager(self, sound_manager):
        self.sound_manager = sound_manager

class Inventory:
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
                return True
            
            # Number keys for item usage (1-7)
            elif pygame.K_1 <= event.key <= pygame.K_7:
                if self.active:  # Only when inventory is open
                    number = event.key - pygame.K_0
                    if self.use_item_by_number(number):
                        print(f"✅ Used item #{number}")
                        return True
            
            # Combat keys
            elif event.key == pygame.K_a:
                if self.throw_stone():
                    print("🪨 Stone thrown!")
                    return True
            
            elif event.key == pygame.K_w:
                if self.shoot_staff_projectile():
                    print("⚡ Staff projectile fired!")
                    return True
        
        return False


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

class MoralSystem:
    def __init__(self):
        self.moral_score = 0
    
    def add_moral_impact(self, impact):
        self.moral_score += impact
    
    def get_moral_standing(self):
        if self.moral_score >= 10:
            return "Righteous"
        elif self.moral_score >= 5:
            return "Good"
        elif self.moral_score >= 0:
            return "Neutral"
        else:
            return "Questionable"
    
    def get_moral_color(self):
        if self.moral_score >= 5:
            return (0, 255, 0)
        elif self.moral_score >= 0:
            return (255, 255, 255)
        else:
            return (255, 0, 0)

class VisualFeedback:
    def __init__(self):
        self.messages = []
    
    def show_message(self, text, duration=2.0):
        self.messages.append({"text": text, "timer": duration})
    
    def update(self, dt):
        for msg in self.messages[:]:
            msg["timer"] -= dt
            if msg["timer"] <= 0:
                self.messages.remove(msg)
    
    def render(self, screen):
        font = pygame.font.Font(None, 24)
        y_offset = 50
        for msg in self.messages:
            text_surface = font.render(msg["text"], True, (255, 255, 255))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30
    
    def create_dust_effect(self, x, y):
        pass
    
    def clear_interaction_prompt(self):
        pass
    
    def show_interaction_prompt(self, text):
        self.show_message(text, 2.0)
