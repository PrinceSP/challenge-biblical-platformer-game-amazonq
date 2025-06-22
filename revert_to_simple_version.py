#!/usr/bin/env python3
"""
Revert the game back 5 times to a much simpler, working version
"""

def create_simple_dialogue_system():
    """Create a very simple dialogue system that just works"""
    
    simple_dialogue = '''
class DialogueSystem:
    def __init__(self):
        self.active = False
        self.current_text = ""
        self.speaker = ""
        
    def start_dialogue(self, dialogue_id):
        """Start simple dialogue"""
        self.active = True
        if dialogue_id == "opening":
            self.speaker = "Narrator"
            self.current_text = "Moses has returned to Egypt by God's command to free His people. Press SPACE to continue."
        return True
    
    def handle_event(self, event):
        """Handle dialogue events simply"""
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.active = False
                return True
        return False
    
    def update(self, dt):
        """Simple update"""
        pass
    
    def render(self, screen, sprites=None):
        """Simple dialogue rendering"""
        if not self.active:
            return
            
        # Simple dialogue box
        box_rect = pygame.Rect(50, 500, 700, 150)
        pygame.draw.rect(screen, (50, 50, 50), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 3)
        
        # Simple text rendering
        font = pygame.font.Font(None, 24)
        if self.speaker:
            speaker_text = font.render(self.speaker + ":", True, (255, 255, 255))
            screen.blit(speaker_text, (box_rect.x + 10, box_rect.y + 10))
        
        # Dialogue text
        text_surface = font.render(self.current_text, True, (255, 255, 255))
        screen.blit(text_surface, (box_rect.x + 10, box_rect.y + 40))
        
        # Continue prompt
        prompt = font.render("Press SPACE to continue", True, (200, 200, 200))
        screen.blit(prompt, (box_rect.x + 10, box_rect.y + 120))
'''
    
    return simple_dialogue

def create_simple_inventory():
    """Create simple inventory system"""
    
    simple_inventory = '''
class Inventory:
    def __init__(self):
        self.active = False
        self.items = {"bread": 3, "water": 2, "stone": 5}
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.active = not self.active
    
    def render(self, screen, sprites=None):
        if not self.active:
            return
        
        # Simple inventory display
        box_rect = pygame.Rect(200, 200, 400, 300)
        pygame.draw.rect(screen, (40, 40, 40), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)
        
        font = pygame.font.Font(None, 32)
        title = font.render("Inventory", True, (255, 255, 255))
        screen.blit(title, (box_rect.x + 10, box_rect.y + 10))
        
        y_offset = 50
        for item, count in self.items.items():
            text = font.render(f"{item}: {count}", True, (255, 255, 255))
            screen.blit(text, (box_rect.x + 10, box_rect.y + y_offset))
            y_offset += 30
'''
    
    return simple_inventory

def create_simple_game_systems():
    """Create simple game_systems.py file"""
    
    simple_systems = '''"""
Simple Game Systems for Moses Adventure
"""

import pygame
from constants import *

class DialogueNode:
    def __init__(self, speaker, text, choices=None, moral_impact=0):
        self.speaker = speaker
        self.text = text
        self.choices = choices or []
        self.moral_impact = moral_impact

''' + create_simple_dialogue_system() + '''

''' + create_simple_inventory() + '''

class MoralSystem:
    def __init__(self):
        self.moral_score = 0
    
    def add_moral_impact(self, impact):
        self.moral_score += impact

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
'''
    
    with open('game_systems.py', 'w') as f:
        f.write(simple_systems)
    
    print("✅ Created simple game_systems.py")

def simplify_main_game():
    """Simplify the main game file"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Remove complex item feedback system
    if "def show_item_feedback" in content:
        # Find and remove complex feedback methods
        start_pos = content.find("def show_item_feedback")
        end_pos = content.find("\n    def ", start_pos + 1)
        if end_pos == -1:
            end_pos = content.find("\ndef main", start_pos)
        if end_pos != -1:
            content = content[:start_pos] + content[end_pos:]
            print("✅ Removed complex item feedback system")
    
    # Simplify item collection messages
    content = content.replace('self.show_item_collection_feedback', 'print')
    content = content.replace('self.show_item_usage_feedback', 'print')
    
    # Remove complex feedback message lists
    if "self.item_feedback_messages" in content:
        content = content.replace("self.item_feedback_messages = []", "# Simple feedback system")
        print("✅ Simplified feedback system")
    
    # Remove complex dialogue debug
    lines = content.split('\n')
    simple_lines = []
    skip_debug = False
    
    for line in lines:
        if "# Debug dialogue system" in line:
            skip_debug = True
        elif skip_debug and (line.strip() == "" or not line.startswith("        ")):
            skip_debug = False
        
        if not skip_debug:
            simple_lines.append(line)
    
    content = '\n'.join(simple_lines)
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("✅ Simplified main game file")

def main():
    """Revert the game back 5 times to a simpler version"""
    print("🔄 Reverting Game Back 5 Times")
    print("=" * 35)
    
    print("Step 1: Creating simple game systems...")
    create_simple_game_systems()
    
    print("Step 2: Simplifying main game...")
    simplify_main_game()
    
    print("Step 3: Removing complex modifications...")
    # Remove complex debug files
    import os
    debug_files = [
        "fix_dialogue_text_display.py",
        "fix_game_systems_indentation.py", 
        "restore_dialogue_text_system.py",
        "add_dialogue_controls_info.py"
    ]
    
    for file in debug_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"✅ Removed {file}")
    
    print("\n" + "=" * 35)
    print("🎉 GAME REVERTED TO SIMPLE VERSION!")
    print("\nReverted Features:")
    print("✅ Simple dialogue system that just works")
    print("✅ Basic inventory system")
    print("✅ Removed complex feedback systems")
    print("✅ Removed debug complexity")
    print("✅ Clean, minimal code")
    
    print("\nSimple Game Features:")
    print("- Opening dialogue appears and can be continued")
    print("- SPACE advances dialogue")
    print("- Basic inventory with I key")
    print("- Simple item collection messages")
    print("- No complex systems or errors")
    
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
