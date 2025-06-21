"""
Clean Game Systems for Moses Adventure
Contains essential systems: Inventory, DialogueSystem, MoralSystem, VisualFeedback
"""

import pygame
import os
from constants import *
from font_manager import get_font_manager

class DialogueNode:
    def __init__(self, speaker, text, choices=None, moral_impact=0):
        self.speaker = speaker
        self.text = text
        self.choices = choices or []
        self.moral_impact = moral_impact

class Inventory:
    def __init__(self):
        self.items = {}
        self.active = False
        self.max_items = 20
    
    def add_item(self, item_type, quantity=1):
        if item_type in self.items:
            self.items[item_type] += quantity
        else:
            self.items[item_type] = quantity
        print(f"Added {quantity} {item_type}(s) to inventory")
    
    def use_item(self, item_type):
        if item_type in self.items and self.items[item_type] > 0:
            self.items[item_type] -= 1
            if self.items[item_type] == 0:
                del self.items[item_type]
            return True
        return False
    
    def handle_event(self, event):
        """Handle inventory events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                self.active = False
    
    def render(self, screen, ui_sprites):
        if not self.active:
            return
        
        font_manager = get_font_manager()
        
        # Inventory panel
        panel_rect = pygame.Rect(200, 150, 400, 300)
        pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 3)
        
        # Title
        title_text = font_manager.render_text("Inventory", 'large', WHITE)
        screen.blit(title_text, (panel_rect.left + 20, panel_rect.top + 20))
        
        # Items
        y_offset = 70
        for item_type, quantity in self.items.items():
            item_text = font_manager.render_text(f"{item_type}: {quantity}", 'small', WHITE)
            screen.blit(item_text, (panel_rect.left + 30, panel_rect.top + y_offset))
            y_offset += 30

class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.dialogue_data = {}
        self.text_speed = 50
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
                    "Halt! You look familiar... aren't you that Hebrew who killed the Egyptian overseer?",
                    [
                        ("I am Moses, servant of the Most High God", "moses_response"),
                        ("I'm just passing through", "neutral_response")
                    ]
                ),
                "moses_response": DialogueNode(
                    "Palace Guard",
                    "Moses! You have courage returning here. The Pharaoh seeks your life, but I sense divine purpose in you.",
                    moral_impact=1
                ),
                "neutral_response": DialogueNode(
                    "Palace Guard",
                    "Hmm... move along then, but stay out of trouble. These are dangerous times.",
                    moral_impact=0
                )
            },
            
            "slave_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Brother! Is it truly you? Moses, the one who defended us against the Egyptian?",
                    [
                        ("Yes, I have returned to free our people", "liberation_response"),
                        ("Keep your voice down", "cautious_response")
                    ]
                ),
                "liberation_response": DialogueNode(
                    "Hebrew Slave",
                    "Praise be to the God of Abraham! We have prayed for deliverance. We are ready to follow you!",
                    moral_impact=2
                ),
                "cautious_response": DialogueNode(
                    "Hebrew Slave",
                    "You're right... the walls have ears. But know that we are ready when you call upon us.",
                    moral_impact=1
                )
            },
            
            "citizen_dialogue": {
                "start": DialogueNode(
                    "Egyptian Citizen",
                    "You there! I haven't seen you around the palace before. Are you new to Pharaoh's service?",
                    [
                        ("I serve a higher power than Pharaoh", "higher_power"),
                        ("I'm here on business", "business_response")
                    ]
                ),
                "higher_power": DialogueNode(
                    "Egyptian Citizen",
                    "Blasphemy! How dare you speak against the divine Pharaoh! But... there is something about you...",
                    moral_impact=1
                ),
                "business_response": DialogueNode(
                    "Egyptian Citizen",
                    "Ah, a merchant perhaps? These are prosperous times for those who serve Egypt well.",
                    moral_impact=0
                )
            },
            
            "priest_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "The gods whisper of great changes coming to Egypt. You carry the scent of destiny about you.",
                    [
                        ("The God of Abraham speaks through me", "divine_mission"),
                        ("What do your gods tell you?", "ask_gods")
                    ]
                ),
                "divine_mission": DialogueNode(
                    "Egyptian Priest",
                    "Abraham's God... yes, I sense great power. Our gods tremble before such might.",
                    moral_impact=1
                ),
                "ask_gods": DialogueNode(
                    "Egyptian Priest",
                    "They speak of plagues, of darkness, of a great exodus. The very foundations of Egypt shall shake.",
                    moral_impact=0
                )
            },
            
            "resistance_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Moses! We've been organizing in secret. Many are ready to follow you out of Egypt!",
                    [
                        ("Tell me of your preparations", "learn_preparations"),
                        ("We must be patient and wait for God's timing", "patience_counsel")
                    ]
                ),
                "learn_preparations": DialogueNode(
                    "Hebrew Slave",
                    "We have supplies hidden, routes planned, and faithful hearts ready. Just give the word!",
                    moral_impact=1
                ),
                "patience_counsel": DialogueNode(
                    "Hebrew Slave",
                    "You are wise, Moses. We will wait for the Lord's sign, as you did at the burning bush.",
                    moral_impact=2
                )
            },
            
            "checkpoint_dialogue": {
                "start": DialogueNode(
                    "Palace Guard",
                    "This is a restricted area. State your business or turn back immediately!",
                    [
                        ("I have urgent business with Pharaoh", "pharaoh_business"),
                        ("Stand aside, I serve the Most High God", "divine_authority")
                    ]
                ),
                "pharaoh_business": DialogueNode(
                    "Palace Guard",
                    "Pharaoh sees no one without appointment. You'll need proper documentation.",
                    moral_impact=0
                ),
                "divine_authority": DialogueNode(
                    "Palace Guard",
                    "Bold words! But I sense... something about you. Pass quickly, before I change my mind.",
                    moral_impact=1
                )
            },
            
            "informant_dialogue": {
                "start": DialogueNode(
                    "Egyptian Citizen",
                    "Psst! You're Moses, aren't you? I have information that might help your cause...",
                    [
                        ("What information?", "seek_info"),
                        ("How do you know who I am?", "question_identity")
                    ]
                ),
                "seek_info": DialogueNode(
                    "Egyptian Citizen",
                    "Pharaoh plans to increase security tomorrow. If you're planning something, tonight is your chance.",
                    moral_impact=1
                ),
                "question_identity": DialogueNode(
                    "Egyptian Citizen",
                    "Word travels fast in the palace. Some of us... sympathize with your people's plight.",
                    moral_impact=1
                )
            },
            
            "wisdom_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "Moses, seeker of truth, you near the end of your palace journey. What wisdom do you seek?",
                    [
                        ("How can I convince Pharaoh to free my people?", "pharaoh_counsel"),
                        ("Bless my mission, wise one", "seek_blessing")
                    ]
                ),
                "pharaoh_counsel": DialogueNode(
                    "Egyptian Priest",
                    "Pharaoh's heart is stone, but even stone can be broken by persistent water... or divine power.",
                    moral_impact=1
                ),
                "seek_blessing": DialogueNode(
                    "Egyptian Priest",
                    "May the God of your fathers strengthen your arm and guide your steps. Go with divine favor, Moses.",
                    moral_impact=2
                )
            }
        }
    
    def start_dialogue(self, dialogue_id):
        """Start a dialogue sequence with enhanced audio"""
        if dialogue_id in self.dialogue_data:
            self.active = True
            self.current_dialogue = dialogue_id
            self.current_node = self.dialogue_data[dialogue_id]["start"]
            self.full_text = self.current_node.text
            self.displayed_text = ""
            self.text_timer = 0
            self.waiting_for_input = False
            self.is_typing = True
            
            # Lower background music volume for dialogue
            if self.sound_manager:
                self.sound_manager.lower_music_volume()
                self.sound_manager.play_typing_sound_loop()
            
            print(f"✅ Started dialogue: {dialogue_id}")
            return True
        else:
            print(f"❌ Dialogue '{dialogue_id}' not found!")
            return False
    
    def update(self, dt):
        """Update dialogue system with smart typing sound"""
        if not self.active or self.waiting_for_input:
            return
        
        # Animate text appearance
        if len(self.displayed_text) < len(self.full_text):
            self.text_timer += dt
            chars_to_show = int(self.text_timer * self.text_speed)
            new_displayed_text = self.full_text[:chars_to_show]
            
            # Check if we just finished typing
            if len(new_displayed_text) >= len(self.full_text):
                self.displayed_text = self.full_text
                self.waiting_for_input = True
                self.is_typing = False
                
                # Stop typing sound when text is fully displayed
                if self.sound_manager:
                    self.sound_manager.stop_typing_sound()
                    print("🔇 Text fully displayed - stopped typing sound")
            else:
                self.displayed_text = new_displayed_text
    
    def end_dialogue(self):
        """End the current dialogue and restore audio"""
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.is_typing = False
        
        # Stop typing sound and restore background music volume
        if self.sound_manager:
            self.sound_manager.stop_typing_sound()
            self.sound_manager.restore_music_volume()
        
        print("✅ Dialogue ended - audio restored")
    
    def set_sound_manager(self, sound_manager):
        """Set the sound manager for audio effects"""
        self.sound_manager = sound_manager
    
    def handle_event(self, event):
        """Handle dialogue events"""
        if not self.active:
            return
            
        if event.type == pygame.KEYDOWN:
            if self.waiting_for_input:
                if self.current_node and self.current_node.choices:
                    # Handle choice selection
                    if event.key == pygame.K_1 and len(self.current_node.choices) >= 1:
                        self.choose_option(0)
                    elif event.key == pygame.K_2 and len(self.current_node.choices) >= 2:
                        self.choose_option(1)
                    elif event.key == pygame.K_3 and len(self.current_node.choices) >= 3:
                        self.choose_option(2)
                else:
                    # Continue to next dialogue or end
                    if event.key == pygame.K_SPACE:
                        self.end_dialogue()
    
    def choose_option(self, option_index):
        """Choose a dialogue option"""
        if self.current_node and self.current_node.choices:
            if 0 <= option_index < len(self.current_node.choices):
                choice_text, next_node_id = self.current_node.choices[option_index]
                print(f"💬 Chose: {choice_text}")
                
                # Apply moral impact and health effects
                if self.current_node.moral_impact != 0:
                    print(f"⚖️  Moral impact: {self.current_node.moral_impact}")
                    
                    # Health effects based on choices
                    if hasattr(self, 'game_instance') and self.game_instance and hasattr(self.game_instance, 'player'):
                        if self.current_node.moral_impact < 0:
                            # Bad choice - lose health
                            damage = abs(self.current_node.moral_impact) * 10
                            self.game_instance.player.health -= damage
                            print(f"💔 Health reduced by {damage}! Current health: {self.game_instance.player.health}")
                        elif self.current_node.moral_impact > 0:
                            # Good choice - gain health
                            healing = self.current_node.moral_impact * 5
                            self.game_instance.player.health = min(100, self.game_instance.player.health + healing)
                            print(f"💚 Health increased by {healing}! Current health: {self.game_instance.player.health}")
                
                # Move to next node or end dialogue
                if next_node_id in self.dialogue_data[self.current_dialogue]:
                    self.current_node = self.dialogue_data[self.current_dialogue][next_node_id]
                    self.full_text = self.current_node.text
                    self.displayed_text = ""
                    self.text_timer = 0
                    self.waiting_for_input = False
                    self.is_typing = True
                    
                    # Restart typing sound
                    if self.sound_manager:
                        self.sound_manager.play_typing_sound_loop()
                else:
                    self.end_dialogue()
    
    def render(self, screen, sprites=None):
        """Render enhanced dialogue UI"""
        if not self.active or not self.current_node:
            return
        
        font_manager = get_font_manager()
        
        # Enhanced dialogue panel
        panel_height = 220
        panel_rect = pygame.Rect(40, SCREEN_HEIGHT - panel_height - 40, SCREEN_WIDTH - 80, panel_height)
        
        # Draw background
        pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 4)  # Golden border
        
        # Speaker name
        if self.current_node.speaker:
            speaker_rect = pygame.Rect(panel_rect.left + 20, panel_rect.top + 15, 200, 30)
            pygame.draw.rect(screen, (218, 165, 32), speaker_rect)
            
            speaker_text = font_manager.render_text(self.current_node.speaker, 'medium', WHITE)
            screen.blit(speaker_text, (speaker_rect.left + 10, speaker_rect.top + 5))
        
        # Dialogue text
        text_lines = self.wrap_text(self.displayed_text, font_manager.get_font('small'), panel_rect.width - 40)
        y_offset = 60
        for line in text_lines:
            if y_offset + 25 <= panel_rect.bottom - 60:
                line_surface = font_manager.render_text(line, 'small', WHITE)
                screen.blit(line_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                y_offset += 25
        
        # Choices
        if self.waiting_for_input and self.current_node.choices:
            choice_start_y = panel_rect.top + 160
            for i, (choice_text, _) in enumerate(self.current_node.choices):
                choice_rect = pygame.Rect(panel_rect.left + 30, choice_start_y + i * 25, panel_rect.width - 60, 20)
                pygame.draw.rect(screen, (60, 40, 30), choice_rect)
                pygame.draw.rect(screen, (218, 165, 32), choice_rect, 2)
                
                choice_surface = font_manager.render_text(f"{i+1}. {choice_text}", 'tiny', WHITE)
                screen.blit(choice_surface, (choice_rect.left + 5, choice_rect.top + 2))
        
        # Continue prompt
        elif self.waiting_for_input:
            prompt_text = font_manager.render_text("Press SPACE to continue...", 'tiny', GOLD)
            screen.blit(prompt_text, (panel_rect.right - 200, panel_rect.bottom - 25))
    
    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

class MoralSystem:
    def __init__(self):
        self.moral_score = 0
        self.actions = []
    
    def add_moral_action(self, action, impact):
        self.moral_score += impact
        self.actions.append((action, impact))
        print(f"⚖️  Moral action: {action} (Impact: {impact}, Total: {self.moral_score})")
    
    def get_moral_standing(self):
        """Get the current moral standing based on score"""
        if self.moral_score >= 10:
            return "Righteous Leader"
        elif self.moral_score >= 5:
            return "Faithful Servant"
        elif self.moral_score >= 0:
            return "Seeking Truth"
        elif self.moral_score >= -5:
            return "Conflicted Soul"
        else:
            return "Lost Path"
    
    def get_moral_color(self):
        """Get color representing current moral standing"""
        if self.moral_score >= 10:
            return (255, 215, 0)  # Gold
        elif self.moral_score >= 5:
            return (0, 255, 0)    # Green
        elif self.moral_score >= 0:
            return (255, 255, 255)  # White
        elif self.moral_score >= -5:
            return (255, 165, 0)  # Orange
        else:
            return (255, 0, 0)    # Red

class VisualFeedback:
    def __init__(self):
        self.messages = []
        self.effects = []
    
    def show_message(self, text, duration=2.0):
        self.messages.append({
            'text': text,
            'timer': duration,
            'y_offset': 0
        })
    
    def show_interaction_prompt(self, x, y):
        # Simple interaction prompt
        pass
    
    def clear_interaction_prompt(self):
        # Clear interaction prompt
        pass
    
    def update(self, dt):
        # Update messages
        for message in self.messages[:]:
            message['timer'] -= dt
            if message['timer'] <= 0:
                self.messages.remove(message)
    
    def render(self, screen):
        """Render visual feedback"""
        font_manager = get_font_manager()
        
        # Render messages
        y_offset = 100
        for message in self.messages:
            text_surface = font_manager.render_text(message['text'], 'small', WHITE)
            screen.blit(text_surface, (50, y_offset))
            y_offset += 30
