import pygame
import random
import math
import os
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from font_manager import get_font_manager

# Import constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
PLAYER_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)

@dataclass
class DialogueNode:
    speaker: str
    text: str
    choices: List[Tuple[str, str]] = None  # (choice_text, next_node_id)
    moral_impact: int = 0  # -1 to 1 scale

class Inventory:
    def __init__(self):
        self.items = {}
        self.active = False
        self.selected_slot = 0
        self.slots_per_row = 8
        self.max_slots = 32
    
    def add_item(self, item_type, quantity=1):
        """Add item to inventory"""
        if item_type in self.items:
            self.items[item_type] += quantity
        else:
            self.items[item_type] = quantity
    
    def has_item(self, item_type, quantity=1):
        """Check if inventory has item"""
        return self.items.get(item_type, 0) >= quantity
    
    def use_item(self, item_type, quantity=1):
        """Use/remove item from inventory"""
        if self.has_item(item_type, quantity):
            self.items[item_type] -= quantity
            if self.items[item_type] <= 0:
                del self.items[item_type]
            return True
        return False
    
    def get_item_count(self, item_type):
        """Get count of specific item"""
        return self.items.get(item_type, 0)
    
    def handle_event(self, event):
        """Handle inventory events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                self.active = False
            elif event.key == pygame.K_LEFT:
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_slot = min(len(self.items) - 1, self.selected_slot + 1)
            elif event.key == pygame.K_RETURN:
                self.use_selected_item()
    
    def use_selected_item(self):
        """Use the currently selected item"""
        if self.items:
            item_list = list(self.items.keys())
            if 0 <= self.selected_slot < len(item_list):
                item_type = item_list[self.selected_slot]
                # Implement item usage logic here
                print(f"Used {item_type}")
    
    def render(self, screen, ui_sprites):
        """Render inventory UI"""
        if not self.active:
            return
        
        font_manager = get_font_manager()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Inventory panel with proper sizing
        panel_width = 600
        panel_height = 400
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        pygame.draw.rect(screen, BROWN, panel_rect)
        pygame.draw.rect(screen, WHITE, panel_rect, 3)
        
        # Title with custom font
        title = font_manager.render_text("Inventory", 'medium', WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, panel_y + 30))
        screen.blit(title, title_rect)
        
        # Item slots with proper spacing
        slot_size = 50
        slot_margin = 10
        start_x = panel_x + 20
        start_y = panel_y + 70
        
        slot_sprite = ui_sprites.get('inventory_slot')
        
        row = 0
        col = 0
        for i, (item_type, quantity) in enumerate(self.items.items()):
            x = start_x + col * (slot_size + slot_margin)
            y = start_y + row * (slot_size + slot_margin)
            
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            
            # Highlight selected slot
            if i == self.selected_slot:
                pygame.draw.rect(screen, GOLD, slot_rect, 3)
            
            # Draw slot background
            if slot_sprite:
                scaled_slot = pygame.transform.scale(slot_sprite, (slot_size, slot_size))
                screen.blit(scaled_slot, slot_rect)
            else:
                pygame.draw.rect(screen, GRAY, slot_rect)
                pygame.draw.rect(screen, WHITE, slot_rect, 2)
            
            # Draw item (simplified representation)
            item_colors = {
                "stone": GRAY,
                "meat": BROWN,
                "water": BLUE,
                "armor_of_god": GOLD,
                "staff": BROWN,
                "bread": (210, 180, 140),
                "scroll": (245, 245, 220)
            }
            
            item_color = item_colors.get(item_type, WHITE)
            item_rect = pygame.Rect(x + 10, y + 10, slot_size - 20, slot_size - 20)
            pygame.draw.rect(screen, item_color, item_rect)
            
            # Draw quantity with custom font
            if quantity > 1:
                qty_text = font_manager.render_text(str(quantity), 'tiny', WHITE)
                screen.blit(qty_text, (x + slot_size - 15, y + slot_size - 15))
            
            col += 1
            if col >= self.slots_per_row:
                col = 0
                row += 1
        
        # Item description with custom font
        if self.items:
            item_list = list(self.items.keys())
            if 0 <= self.selected_slot < len(item_list):
                selected_item = item_list[self.selected_slot]
                
                # Item descriptions
                descriptions = {
                    "stone": "Smooth stones for David's sling",
                    "meat": "Dried meat for sustenance in the wilderness",
                    "water": "Fresh water from the well",
                    "armor_of_god": "Divine protection from the Almighty",
                    "staff": "The staff of Moses, symbol of God's power",
                    "bread": "Bread for the journey",
                    "scroll": "Sacred scrolls containing God's word"
                }
                
                desc_text = descriptions.get(selected_item, "A mysterious item")
                desc_surface = font_manager.render_text(desc_text, 'small', WHITE)
                desc_rect = desc_surface.get_rect(center=(SCREEN_WIDTH//2, panel_y + panel_height - 50))
                screen.blit(desc_surface, desc_rect)
        
        # Instructions with custom font
        instructions = [
            "Arrow Keys: Navigate | Enter: Use Item",
            "I or ESC: Close Inventory"
        ]
        
        y_offset = panel_y + panel_height - 30
        for instruction in instructions:
            text = font_manager.render_text(instruction, 'tiny', WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 20

class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.dialogue_data = {}
        self.text_speed = 50  # Characters per second
        self.displayed_text = ""
        self.text_timer = 0
        self.full_text = ""
        self.waiting_for_input = False
        self.is_typing = False  # Track if text is being typed
        self.sound_manager = None
        self.load_dialogue_data()
    
    def load_dialogue_data(self):
        """Load comprehensive dialogue data with multiple choice interactions"""
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
                        ("I'm just passing through", "neutral_response"),
                        ("You must be mistaken", "deceptive_response")
                    ]
                ),
                "moses_response": DialogueNode(
                    "Palace Guard",
                    "Moses! You have courage returning here. The Pharaoh seeks your life, but... I've heard whispers of your divine mission.",
                    [("God will protect me", "faithful_response"), ("Will you help me?", "request_help")],
                    moral_impact=1
                ),
                "neutral_response": DialogueNode(
                    "Palace Guard",
                    "Hmm... move along then, but stay out of trouble. These are dangerous times.",
                    moral_impact=0
                ),
                "deceptive_response": DialogueNode(
                    "Palace Guard",
                    "Perhaps... but I'll be watching you. Don't cause any disturbances.",
                    moral_impact=-1
                ),
                "faithful_response": DialogueNode(
                    "Palace Guard",
                    "Your faith is strong. May your God indeed watch over you, Moses.",
                    moral_impact=1
                ),
                "request_help": DialogueNode(
                    "Palace Guard",
                    "I... I cannot openly defy Pharaoh, but I will not hinder your path. Go quickly.",
                    moral_impact=1
                )
            },
            
            "slave_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Brother! Is it truly you? Moses, the one who defended us against the Egyptian?",
                    [
                        ("Yes, I have returned to free our people", "liberation_response"),
                        ("Keep your voice down", "cautious_response"),
                        ("I'm not who you think I am", "denial_response")
                    ]
                ),
                "liberation_response": DialogueNode(
                    "Hebrew Slave",
                    "Praise be to the God of Abraham! We have prayed for deliverance. What would you have us do?",
                    [("Prepare yourselves, freedom comes soon", "prepare_response"), ("Spread word quietly among the faithful", "spread_word")],
                    moral_impact=2
                ),
                "cautious_response": DialogueNode(
                    "Hebrew Slave",
                    "You're right... the walls have ears. But know that we are ready when you call upon us.",
                    moral_impact=1
                ),
                "denial_response": DialogueNode(
                    "Hebrew Slave",
                    "I... I understand. These are dangerous times. But my eyes do not deceive me.",
                    moral_impact=-1
                ),
                "prepare_response": DialogueNode(
                    "Hebrew Slave",
                    "We will be ready, Moses. The Lord's deliverance is at hand!",
                    moral_impact=2
                ),
                "spread_word": DialogueNode(
                    "Hebrew Slave",
                    "It shall be done. The faithful will know that hope has returned to Egypt.",
                    moral_impact=2
                )
            },
            
            "citizen_dialogue": {
                "start": DialogueNode(
                    "Egyptian Citizen",
                    "You there! I haven't seen you around the palace before. Are you new to Pharaoh's service?",
                    [
                        ("I serve a higher power than Pharaoh", "higher_power"),
                        ("I'm here on business", "business_response"),
                        ("Yes, I'm new here", "lie_response")
                    ]
                ),
                "higher_power": DialogueNode(
                    "Egyptian Citizen",
                    "Blasphemy! How dare you speak against the divine Pharaoh! Guards should hear of this!",
                    [("The God of the Hebrews is the one true God", "truth_response"), ("I meant no offense", "apologize")],
                    moral_impact=1
                ),
                "business_response": DialogueNode(
                    "Egyptian Citizen",
                    "Ah, a merchant perhaps? These are prosperous times for those who serve Egypt well.",
                    moral_impact=0
                ),
                "lie_response": DialogueNode(
                    "Egyptian Citizen",
                    "Welcome then. Serve Pharaoh faithfully and you will be rewarded.",
                    moral_impact=-1
                ),
                "truth_response": DialogueNode(
                    "Egyptian Citizen",
                    "You speak madness! But... there is something in your eyes. I will not call the guards... this time.",
                    moral_impact=2
                ),
                "apologize": DialogueNode(
                    "Egyptian Citizen",
                    "See that you watch your tongue. Pharaoh's ears are everywhere.",
                    moral_impact=0
                )
            },
            
            "priest_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "The gods whisper of great changes coming to Egypt. You... you carry the scent of destiny about you.",
                    [
                        ("The God of Abraham speaks through me", "divine_mission"),
                        ("What do your gods tell you?", "ask_gods"),
                        ("I don't believe in omens", "skeptical")
                    ]
                ),
                "divine_mission": DialogueNode(
                    "Egyptian Priest",
                    "Abraham's God... yes, I sense great power. Our gods tremble before such might. What does He command?",
                    [("Freedom for His people", "freedom_command"), ("Judgment upon Egypt", "judgment_warning")],
                    moral_impact=1
                ),
                "ask_gods": DialogueNode(
                    "Egyptian Priest",
                    "They speak of plagues, of darkness, of a great exodus. The very foundations of Egypt shall shake.",
                    moral_impact=0
                ),
                "skeptical": DialogueNode(
                    "Egyptian Priest",
                    "Perhaps... but the wise man heeds the signs, whether he believes or not.",
                    moral_impact=0
                ),
                "freedom_command": DialogueNode(
                    "Egyptian Priest",
                    "Then may the gods have mercy on us all. I will not stand in your way, Moses.",
                    moral_impact=2
                ),
                "judgment_warning": DialogueNode(
                    "Egyptian Priest",
                    "I fear you speak truly. May Egypt find wisdom before it is too late.",
                    moral_impact=1
                )
            },
            
            "resistance_dialogue": {
                "start": DialogueNode(
                    "Hebrew Slave",
                    "Moses! We've been organizing in secret. Many are ready to follow you out of Egypt!",
                    [
                        ("Tell me of your preparations", "learn_preparations"),
                        ("We must be patient and wait for God's timing", "patience_counsel"),
                        ("Are you certain you can trust everyone?", "trust_concerns")
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
                ),
                "trust_concerns": DialogueNode(
                    "Hebrew Slave",
                    "We've been careful. Only the most faithful know of our plans. But you're right to be cautious.",
                    moral_impact=1
                )
            },
            
            "checkpoint_dialogue": {
                "start": DialogueNode(
                    "Palace Guard",
                    "This is a restricted area. State your business or turn back immediately!",
                    [
                        ("I have urgent business with Pharaoh", "pharaoh_business"),
                        ("I'm lost, can you direct me?", "lost_excuse"),
                        ("Stand aside, I serve the Most High God", "divine_authority")
                    ]
                ),
                "pharaoh_business": DialogueNode(
                    "Palace Guard",
                    "Pharaoh sees no one without appointment. You'll need proper documentation.",
                    moral_impact=0
                ),
                "lost_excuse": DialogueNode(
                    "Palace Guard",
                    "The palace is vast. Head back the way you came and ask a servant for directions.",
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
                        ("How do you know who I am?", "question_identity"),
                        ("I don't know what you're talking about", "deny_identity")
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
                ),
                "deny_identity": DialogueNode(
                    "Egyptian Citizen",
                    "Of course, of course. But if you were him... remember what I said about tomorrow.",
                    moral_impact=0
                )
            },
            
            "wisdom_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "Moses, seeker of truth, you near the end of your palace journey. What wisdom do you seek?",
                    [
                        ("How can I convince Pharaoh to free my people?", "pharaoh_counsel"),
                        ("What trials await me ahead?", "future_trials"),
                        ("Bless my mission, wise one", "seek_blessing")
                    ]
                ),
                "pharaoh_counsel": DialogueNode(
                    "Egyptian Priest",
                    "Pharaoh's heart is stone, but even stone can be broken by persistent water... or divine power.",
                    moral_impact=1
                ),
                "future_trials": DialogueNode(
                    "Egyptian Priest",
                    "Great trials await - plagues, pursuit, wilderness wandering. But also great victories and divine provision.",
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
                    moral_impact=1
                ),
                "past_behind": DialogueNode(
                    "Royal Servant",
                    "Perhaps that's wise, master. The palace has changed since you left. There's much fear and anger.",
                    moral_impact=0
                ),
                "ask_daughter": DialogueNode(
                    "Royal Servant",
                    "She grieves for you still, master. She saved you from the Nile as a baby, and loved you as her own son.",
                    [("Tell her I'm grateful for her kindness", "grateful_message")],
                    moral_impact=1
                ),
                "obey_god": DialogueNode(
                    "Royal Servant",
                    "The Hebrew God must be mighty to call you back here. May He protect you, young master.",
                    moral_impact=1
                ),
                "grateful_message": DialogueNode(
                    "Royal Servant",
                    "I will tell her, if I can. She will be glad to know you remember her love.",
                    moral_impact=1
                )
            },
            "taskmaster_dialogue": {
                "start": DialogueNode(
                    "Egyptian Taskmaster",
                    "Well, well... if it isn't the Hebrew prince who thinks he's above Egyptian law! Come back to face justice?",
                    [
                        ("I came to see the suffering you cause", "witness_suffering"),
                        ("Justice? You know nothing of justice", "challenge_justice"),
                        ("I'm here on God's business", "gods_business")
                    ]
                ),
                "witness_suffering": DialogueNode(
                    "Egyptian Taskmaster",
                    "Suffering? These Hebrew dogs are lucky to serve mighty Egypt! They should be grateful for the work!",
                    [("No man should be treated as property", "human_dignity")],
                    moral_impact=1
                ),
                "challenge_justice": DialogueNode(
                    "Egyptian Taskmaster",
                    "Justice is what Pharaoh decrees! You murdered an Egyptian - that demands blood for blood!",
                    [("He was beating an innocent man", "defend_action")],
                    moral_impact=1
                ),
                "gods_business": DialogueNode(
                    "Egyptian Taskmaster",
                    "Your Hebrew God has no power here! This is Egypt, land of the true gods!",
                    [("You will learn otherwise very soon", "prophetic_threat")],
                    moral_impact=2
                ),
                "human_dignity": DialogueNode(
                    "Egyptian Taskmaster",
                    "Property? They ARE property! Pharaoh owns them, body and soul!",
                    moral_impact=1
                ),
                "defend_action": DialogueNode(
                    "Egyptian Taskmaster",
                    "Innocent? He was Hebrew scum! You'll pay for that Egyptian's blood!",
                    moral_impact=1
                ),
                "prophetic_threat": DialogueNode(
                    "Egyptian Taskmaster",
                    "Threats from a fugitive? Guards! Seize this Hebrew rebel!",
                    moral_impact=1
                )
            },
            "priest_dialogue": {
                "start": DialogueNode(
                    "Egyptian Priest",
                    "You dare enter the sacred halls of Pharaoh's palace? I sense the stench of Hebrew rebellion about you!",
                    [
                        ("The Lord God is above all the gods of Egypt", "challenge_gods"),
                        ("I seek only safe passage", "peaceful_response"),
                        ("Your gods are powerless before the Almighty", "bold_challenge")
                    ]
                ),
                "challenge_gods": DialogueNode(
                    "Egyptian Priest",
                    "Blasphemy! Ra, Horus, and Isis are the true powers! Your Hebrew God is nothing before the might of Egypt's deities!",
                    [("You will see His power soon enough", "prophetic_warning")],
                    moral_impact=1
                ),
                "peaceful_response": DialogueNode(
                    "Egyptian Priest",
                    "Passage? Through the sacred chambers? Pay homage to our gods first, Hebrew, or face their wrath!",
                    [("I bow only to the one true God", "monotheism")],
                    moral_impact=0
                ),
                "bold_challenge": DialogueNode(
                    "Egyptian Priest",
                    "How dare you! I will call upon the power of Set to strike you down where you stand!",
                    [("Let your gods try - mine is the God of all creation", "ultimate_challenge")],
                    moral_impact=2
                ),
                "prophetic_warning": DialogueNode(
                    "Egyptian Priest",
                    "Empty threats from a fugitive! Pharaoh's gods have protected Egypt for a thousand years!",
                    moral_impact=1
                ),
                "monotheism": DialogueNode(
                    "Egyptian Priest",
                    "Stubborn fool! Your God will not save you from Pharaoh's justice!",
                    moral_impact=1
                ),
                "ultimate_challenge": DialogueNode(
                    "Egyptian Priest",
                    "We shall see, Hebrew! When the plagues come upon Egypt, remember this moment!",
                    moral_impact=2
                )
            },
            "divine_encounter": {
                "start": DialogueNode(
                    "Voice of God",
                    "Moses, I AM WHO I AM. I have heard the cry of My people. Lead them to the promised land.",
                    [("Yes, Lord, I will obey", "obedience")],
                    moral_impact=2
                ),
                "obedience": DialogueNode(
                    "Voice of God",
                    "I will be with you. Take up your staff and part the waters.",
                    moral_impact=2
                )
            },
            "bedouin_dialogue": {
                "start": DialogueNode(
                    "Bedouin Trader",
                    "Peace be upon you, traveler. You look weary from the desert journey. Are you fleeing Egypt?",
                    [
                        ("I am Moses, leading my people to freedom", "reveal_mission"),
                        ("I seek safe passage through the desert", "request_passage"),
                        ("Do you have water to spare?", "request_water")
                    ]
                ),
                "reveal_mission": DialogueNode(
                    "Bedouin Trader",
                    "Moses! We have heard tales of the Hebrew who defied Pharaoh. The desert winds carry many stories.",
                    [("Will you help us reach the Red Sea?", "ask_help")],
                    moral_impact=1
                ),
                "request_passage": DialogueNode(
                    "Bedouin Trader",
                    "The desert is treacherous, but I know the safe paths. Beware of Egyptian patrols still hunting fugitives.",
                    moral_impact=0
                ),
                "request_water": DialogueNode(
                    "Bedouin Trader",
                    "Water is precious in the desert, but I will share what I have. May Allah bless your journey.",
                    moral_impact=1
                ),
                "ask_help": DialogueNode(
                    "Bedouin Trader",
                    "The Red Sea is three days' journey east. Follow the stars of the Great Bear. May your God protect you.",
                    moral_impact=1
                )
            },
            "merchant_dialogue": {
                "start": DialogueNode(
                    "Egyptian Merchant",
                    "Fine goods from across the empire! But you... you have the look of trouble about you, stranger.",
                    [
                        ("I seek supplies for a long journey", "buy_supplies"),
                        ("What news from the palace?", "ask_news"),
                        ("I am no trouble to honest merchants", "reassure")
                    ]
                ),
                "buy_supplies": DialogueNode(
                    "Egyptian Merchant",
                    "Supplies? For what journey? The roads are dangerous with all this talk of Hebrew rebellion.",
                    [("The journey all men must make - toward truth", "philosophical")],
                    moral_impact=0
                ),
                "ask_news": DialogueNode(
                    "Egyptian Merchant",
                    "Strange happenings! They say the Hebrew Moses has returned. Pharaoh's rage burns like the desert sun!",
                    moral_impact=0
                ),
                "reassure": DialogueNode(
                    "Egyptian Merchant",
                    "Perhaps... but these are troubled times. Best to keep moving, friend.",
                    moral_impact=0
                ),
                "philosophical": DialogueNode(
                    "Egyptian Merchant",
                    "Truth? A luxury few can afford. But I wish you well on your... journey.",
                    moral_impact=1
                )
            },
            "final_encounter": {
                "start": DialogueNode(
                    "Elder of Jerusalem",
                    "Welcome, Moses! You have led our people to the promised land as God commanded!",
                    moral_impact=2
                )
            }
        }
    
    def update(self, dt):
            self.active = True
            self.current_dialogue = dialogue_id
            self.current_node = self.dialogue_data[dialogue_id]["start"]
            self.full_text = self.current_node.text
            self.displayed_text = ""
            self.text_timer = 0
            self.waiting_for_input = False
            self.is_typing = True  # Start typing
            
            # Lower background music volume for dialogue
            if self.sound_manager:
                self.sound_manager.lower_music_volume()
                # Start typing sound loop
                self.sound_manager.play_typing_sound_loop()
            
            print(f"🗣️  Started dialogue: {dialogue_id}")
    
    def update(self, dt):
        """Update dialogue system with smart typing sound"""
        if not self.active or not self.current_node:
            return
        
        if not self.waiting_for_input and len(self.displayed_text) < len(self.full_text):
            # Still typing text
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
                # Keep typing sound playing while text is being revealed
                if not self.is_typing and self.sound_manager:
                    self.sound_manager.play_typing_sound_loop()
                    self.is_typing = True
    
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
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.end_dialogue()
            else:
                # Skip text animation
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.displayed_text = self.full_text
                    self.waiting_for_input = True
    
    def choose_option(self, choice_index):
        """Choose a dialogue option"""
        if self.current_node and self.current_node.choices:
            choice_text, next_node_id = self.current_node.choices[choice_index]
            
            # Apply moral impact
            if hasattr(self, 'moral_system'):
                self.moral_system.make_choice(f"{self.current_dialogue}_{next_node_id}", 
                                            self.current_node.moral_impact)
            
            if next_node_id in self.dialogue_data[self.current_dialogue]:
                self.current_node = self.dialogue_data[self.current_dialogue][next_node_id]
                self.full_text = self.current_node.text
                self.displayed_text = ""
                self.text_timer = 0
                self.waiting_for_input = False
            else:
                self.end_dialogue()
    
    def end_dialogue(self):
        """End the current dialogue"""
        self.active = False
        self.current_dialogue = None
        self.current_node = None
        self.displayed_text = ""
        self.full_text = ""
        self.waiting_for_input = False
    
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
                # Ensure typing sound is playing while text is being revealed
                if not self.is_typing and self.sound_manager:
                    self.sound_manager.play_typing_sound_loop()
                    self.is_typing = True
    
    def render(self, screen, sprites=None):
        """Render enhanced dialogue UI with tile backgrounds"""
        if not self.active or not self.current_node:
            return
        
        font_manager = get_font_manager()
        
        # Enhanced dialogue panel with tile background
        panel_height = 220
        panel_rect = pygame.Rect(40, SCREEN_HEIGHT - panel_height - 40, SCREEN_WIDTH - 80, panel_height)
        
        # Draw tile background if available
        if sprites and 'tiles' in sprites and 'palace_wall' in sprites['tiles']:
            tile_sprite = sprites['tiles']['palace_wall']
            tile_width, tile_height = tile_sprite.get_size()
            
            # Tile the background
            for x in range(panel_rect.left, panel_rect.right, tile_width):
                for y in range(panel_rect.top, panel_rect.bottom, tile_height):
                    screen.blit(tile_sprite, (x, y))
        else:
            # Fallback to solid background
            pygame.draw.rect(screen, (40, 30, 20), panel_rect)
        
        # Enhanced border with golden color
        pygame.draw.rect(screen, (218, 165, 32), panel_rect, 4)  # Golden border
        pygame.draw.rect(screen, (139, 69, 19), panel_rect, 2)   # Brown inner border
        
        # Speaker name with enhanced styling
        if self.current_node.speaker:
            speaker_rect = pygame.Rect(panel_rect.left + 20, panel_rect.top + 15, 200, 30)
            pygame.draw.rect(screen, (218, 165, 32), speaker_rect)  # Golden background
            pygame.draw.rect(screen, (139, 69, 19), speaker_rect, 2)  # Brown border
            
            speaker_text = font_manager.render_text(self.current_node.speaker, 'medium', WHITE)
            speaker_pos = (speaker_rect.left + 10, speaker_rect.top + 5)
            screen.blit(speaker_text, speaker_pos)
        
        # Main dialogue text with better formatting
        text_lines = self.wrap_text(self.displayed_text, font_manager.get_font('small'), panel_rect.width - 40)
        y_offset = 60
        for line in text_lines:
            if y_offset + 25 <= panel_rect.bottom - 60:  # Leave space for choices
                line_surface = font_manager.render_text(line, 'small', WHITE)
                screen.blit(line_surface, (panel_rect.left + 20, panel_rect.top + y_offset))
                y_offset += 25
        
        # Enhanced choice display
        if self.waiting_for_input and self.current_node.choices:
            choice_start_y = panel_rect.top + 160
            
            for i, (choice_text, _) in enumerate(self.current_node.choices):
                choice_rect = pygame.Rect(panel_rect.left + 30, choice_start_y + i * 25, panel_rect.width - 60, 20)
                
                # Choice background with tile pattern
                if sprites and 'tiles' in sprites and 'stone_platform' in sprites['tiles']:
                    tile_sprite = sprites['tiles']['stone_platform']
                    # Scale tile to fit choice rect
                    scaled_tile = pygame.transform.scale(tile_sprite, (choice_rect.width, choice_rect.height))
                    screen.blit(scaled_tile, choice_rect.topleft)
                else:
                    pygame.draw.rect(screen, (60, 40, 30), choice_rect)
                
                pygame.draw.rect(screen, (218, 165, 32), choice_rect, 2)  # Golden border
                
                # Choice text
                choice_surface = font_manager.render_text(f"{i+1}. {choice_text}", 'tiny', WHITE)
                screen.blit(choice_surface, (choice_rect.left + 5, choice_rect.top + 2))
        
        # Continue prompt
        elif self.waiting_for_input:
            prompt_text = font_manager.render_text("Press SPACE to continue...", 'tiny', GOLD)
            prompt_pos = (panel_rect.right - 200, panel_rect.bottom - 25)
            screen.blit(prompt_text, prompt_pos)
        else:
            # Text animation indicator
            if len(self.displayed_text) < len(self.full_text):
                indicator_text = font_manager.render_text("...", 'small', GOLD)
                screen.blit(indicator_text, (panel_rect.right - 60, panel_rect.bottom - 35))
    
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
        self.moral_score = 0  # -100 to 100 scale
        self.choices_made = []
        self.righteous_choices = 0
        self.neutral_choices = 0
        self.wayward_choices = 0
    
    def make_choice(self, choice_id, moral_impact):
        """Record a moral choice"""
        self.choices_made.append((choice_id, moral_impact))
        self.moral_score += moral_impact * 10
        self.moral_score = max(-100, min(100, self.moral_score))
        
        # Track choice types
        if moral_impact > 0:
            self.righteous_choices += 1
        elif moral_impact == 0:
            self.neutral_choices += 1
        else:
            self.wayward_choices += 1
    
    def get_moral_standing(self):
        """Get current moral standing"""
        if self.moral_score >= 70:
            return "Righteous"
        elif self.moral_score >= 30:
            return "Good"
        elif self.moral_score >= -30:
            return "Neutral"
        elif self.moral_score >= -70:
            return "Wayward"
        else:
            return "Corrupt"
    
    def get_moral_color(self):
        """Get color representing moral standing"""
        standing = self.get_moral_standing()
        colors = {
            "Righteous": GOLD,
            "Good": GREEN,
            "Neutral": WHITE,
            "Wayward": GRAY,
            "Corrupt": RED
        }
        return colors.get(standing, WHITE)

class VisualFeedback:
    def __init__(self):
        self.feedback_messages = []
        self.effects = []
    
    def show_item_collected(self, item_type, position):
        """Show visual feedback for item collection"""
        message = f"+{item_type.replace('_', ' ').title()}"
        self.feedback_messages.append({
            'text': message,
            'position': position,
            'timer': 2.0,
            'color': GREEN,
            'velocity_y': -50
        })
    
    def show_location_text(self, location_name):
        """Show location transition text"""
        self.feedback_messages.append({
            'text': location_name,
            'position': (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            'timer': 3.0,
            'color': GOLD,
            'velocity_y': 0,
            'large': True
        })
    
    def show_interaction_prompt(self, x, y):
        """Show interaction prompt"""
        self.feedback_messages.append({
            'text': "Press E to interact",
            'position': (x, y),
            'timer': 0.1,  # Very short timer, refreshed each frame
            'color': WHITE,
            'velocity_y': 0,
            'small': True
        })
    
    def clear_interaction_prompt(self):
        """Clear interaction prompts"""
        self.feedback_messages = [msg for msg in self.feedback_messages 
                                if msg.get('text') != "Press E to interact"]
    
    def create_dust_effect(self, x, y):
        """Create dust cloud effect"""
        for _ in range(5):
            self.effects.append({
                'type': 'dust',
                'x': x + random.randint(-10, 10),
                'y': y,
                'velocity_x': random.randint(-20, 20),
                'velocity_y': random.randint(-30, -10),
                'timer': 1.0,
                'size': random.randint(3, 8)
            })
    
    def create_sparkle_effect(self, position):
        """Create sparkle effect"""
        x, y = position
        for _ in range(8):
            self.effects.append({
                'type': 'sparkle',
                'x': x + random.randint(-15, 15),
                'y': y + random.randint(-15, 15),
                'velocity_x': random.randint(-30, 30),
                'velocity_y': random.randint(-30, 30),
                'timer': 1.5,
                'size': random.randint(2, 5)
            })
    
    def create_damage_effect(self, position):
        """Create damage effect"""
        x, y = position
        self.feedback_messages.append({
            'text': "Ouch!",
            'position': (x, y - 20),
            'timer': 1.0,
            'color': RED,
            'velocity_y': -30
        })
    
    def update(self, dt):
        """Update feedback messages and effects"""
        # Update messages
        for msg in self.feedback_messages[:]:
            msg['timer'] -= dt
            if 'velocity_y' in msg:
                new_y = msg['position'][1] + msg['velocity_y'] * dt
                msg['position'] = (msg['position'][0], new_y)
            
            if msg['timer'] <= 0:
                self.feedback_messages.remove(msg)
        
        # Update effects
        for effect in self.effects[:]:
            effect['timer'] -= dt
            effect['x'] += effect['velocity_x'] * dt
            effect['y'] += effect['velocity_y'] * dt
            
            if effect['timer'] <= 0:
                self.effects.remove(effect)
    
    def render(self, screen):
        """Render visual feedback"""
        font_manager = get_font_manager()
        
        # Render text messages
        for msg in self.feedback_messages:
            alpha = int(255 * min(1.0, msg['timer'] / 2.0))
            
            if msg.get('large'):
                size = 'large'
            elif msg.get('small'):
                size = 'tiny'
            else:
                size = 'small'
            
            text_surface = font_manager.render_text(msg['text'], size, msg['color'])
            text_surface.set_alpha(alpha)
            
            # Center text
            text_rect = text_surface.get_rect(center=msg['position'])
            screen.blit(text_surface, text_rect)
        
        # Render effects
        for effect in self.effects:
            alpha = int(255 * min(1.0, effect['timer'] / 1.5))
            
            if effect['type'] == 'dust':
                color = (*BROWN, alpha) if alpha < 255 else BROWN
                pygame.draw.circle(screen, color[:3], 
                                 (int(effect['x']), int(effect['y'])), 
                                 effect['size'])
            
            elif effect['type'] == 'sparkle':
                color = (*GOLD, alpha) if alpha < 255 else GOLD
                pygame.draw.circle(screen, color[:3], 
                                 (int(effect['x']), int(effect['y'])), 
                                 effect['size'])
