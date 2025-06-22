"""
Simple Game Systems for Moses Adventure
"""

import pygame

# Screen constants for dialogue rendering
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
from constants import *
from font_manager import get_font_manager

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
        self.text_speed = 30  # Characters per second for typing effect
        self.displayed_text = ""
        self.text_timer = 0
        self.full_text = ""
        self.waiting_for_input = False
        self.is_typing = False
        self.sound_manager = None
        self.load_dialogue_data()
    
    def load_dialogue_data(self):
        """Load dialogue data for all characters"""
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
                    [("I seek an audience with Pharaoh", "audience_request"),
                     ("I am here on divine mission", "divine_mission")]
                ),
                "audience_request": DialogueNode(
                    "Palace Guard",
                    "Pharaoh does not see common folk. Be gone from here!",
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
            
            "slave_dialogue": {
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
        """Start dialogue with typing effect and synchronized sound"""
        if dialogue_id in self.dialogue_data:
            self.active = True
            self.current_dialogue = dialogue_id
            self.current_node = self.dialogue_data[dialogue_id]["start"]
            self.full_text = self.current_node.text
            self.displayed_text = ""  # Start with empty text
            self.text_timer = 0
            self.waiting_for_input = False
            self.is_typing = True  # Start typing immediately
            
            # Start typing sound when text first appears
            if self.sound_manager:
                self.sound_manager.lower_music_volume()
                self.sound_manager.play_typing_sound_loop()
            
            print(f"✅ Started dialogue: {dialogue_id}")
            print(f"🎭 Full text to type: '{self.full_text}'")
            return True
        else:
            print(f"❌ Dialogue '{dialogue_id}' not found")
            return False

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
                    print("🎭 Skipped typing animation")
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
                            print("🎭 Advanced to next dialogue")
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
        """Render dialogue with VISIBLE text on screen"""
        if not self.active or not self.current_node:
            return
        
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Create dialogue box - LARGE and VISIBLE
        box_width = screen_width - 100
        box_height = 180
        box_x = 50
        box_y = screen_height - box_height - 50
        
        # Draw dialogue background - DARK with WHITE text
        dialogue_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Dark background for contrast
        pygame.draw.rect(screen, (20, 15, 10), dialogue_rect)  # Very dark brown
        pygame.draw.rect(screen, (255, 215, 0), dialogue_rect, 4)  # Gold border
        
        # Speaker name - VISIBLE
        if self.current_node and self.current_node.speaker:
            speaker_font = pygame.font.Font(None, 42)
            speaker_text = speaker_font.render(f"{self.current_node.speaker}:", True, (255, 215, 0))
            screen.blit(speaker_text, (box_x + 20, box_y + 15))
        
        # Main dialogue text - WHITE on DARK background
        if self.displayed_text:
            # Use large, readable font
            text_font = pygame.font.Font(None, 30)
            text_color = (255, 255, 255)  # Pure WHITE text
            
            # Split text into lines that fit
            words = self.displayed_text.split(' ')
            lines = []
            current_line = ""
            max_width = box_width - 60
            
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
            
            # Render each line of text - GUARANTEED VISIBLE
            text_start_y = box_y + 65
            line_height = 28
            
            for i, line in enumerate(lines[:3]):  # Show up to 3 lines
                if line.strip():
                    # Create text surface
                    text_surface = text_font.render(line, True, text_color)
                    # Draw text on screen
                    screen.blit(text_surface, (box_x + 30, text_start_y + (i * line_height)))
        
        # Status indicator at bottom
        status_y = box_y + box_height - 35
        status_font = pygame.font.Font(None, 26)
        
        if self.waiting_for_input:
            # Show continue prompt
            prompt_surface = status_font.render("Press SPACE to continue...", True, (255, 255, 0))
            screen.blit(prompt_surface, (box_x + box_width - 250, status_y))
        elif self.is_typing:
            # Show typing indicator
            typing_surface = status_font.render("...", True, (200, 200, 100))
            screen.blit(typing_surface, (box_x + box_width - 60, status_y))
        
        # Force screen update to ensure visibility
        pygame.display.flip()

    def set_sound_manager(self, sound_manager):
        """Set sound manager for typing effects"""
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
        title_text = self.render_text("Inventory", 'large', (255, 255, 255))
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
                
                text_surface = self.render_text(item_text, 'small', (255, 255, 255))
                screen.blit(text_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                y_offset += 25
                item_index += 1
        
        # Usage instructions
        instructions = [
            "Press number keys (1-7) to use items",
            "Press I to close inventory"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.render_text(instruction, 'tiny', (200, 200, 200))
            screen.blit(text, (panel_rect.left + 20, panel_rect.bottom - 40 + (i * 15)))

class MoralSystem:
    def __init__(self):
        self.moral_score = 0
    
    def add_moral_impact(self, impact):
        self.moral_score += impact

    def get_moral_standing(self):
        """Get moral standing description"""
        if self.moral_score >= 10:
            return "Righteous"
        elif self.moral_score >= 5:
            return "Good"
        elif self.moral_score >= 0:
            return "Neutral"
        elif self.moral_score >= -5:
            return "Questionable"
        else:
            return "Wicked"

    def get_moral_color(self):
        """Get color for moral standing display"""
        if self.moral_score >= 5:
            return (0, 255, 0)  # Green for good
        elif self.moral_score >= 0:
            return (255, 255, 255)  # White for neutral
        else:
            return (255, 0, 0)  # Red for bad

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
    
    
    def render_text(self, text, font_size, color):
        """Simple text rendering method"""
        font_sizes = {'tiny': 16, 'small': 24, 'medium': 32, 'large': 48}
        size = font_sizes.get(font_size, 24)
        font = pygame.font.Font(None, size)
        return font.render(text, True, color)
    
    def render(self, screen):
        font = pygame.font.Font(None, 24)
        y_offset = 50
        for msg in self.messages:
            text_surface = font.render(msg["text"], True, (255, 255, 255))
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30

    def create_dust_effect(self, x, y):
        """Create dust effect (simple version)"""
        pass
    
    def clear_interaction_prompt(self):
        """Clear interaction prompt (simple version)"""
        pass
    
    def show_interaction_prompt(self, text):
        """Show interaction prompt (simple version)"""
        self.show_message(text, 2.0)

    def get_moral_color(self):
        """Get color for moral standing display"""
        if self.moral_score >= 5:
            return (0, 255, 0)  # Green for good
        elif self.moral_score >= 0:
            return (255, 255, 255)  # White for neutral
        else:
            return (255, 0, 0)  # Red for bad

