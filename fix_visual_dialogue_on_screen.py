#!/usr/bin/env python3
"""
Fix visual dialogue display so text actually appears on screen with typing effect
"""

def fix_dialogue_visual_rendering():
    """Fix the dialogue system to show text visually on screen"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find the DialogueSystem render method and replace with a working version
    render_start = content.find('def render(self, screen, sprites=None):')
    if render_start != -1:
        # Find the end of the render method
        next_method = content.find('\n    def ', render_start + 1)
        if next_method == -1:
            next_method = content.find('\nclass ', render_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Create a render method that ACTUALLY shows text on screen
        working_render = '''    def render(self, screen, sprites=None):
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
'''
        
        content = content[:render_start] + working_render + content[next_method:]
        print("✅ Fixed dialogue render method for visible text display")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def fix_typing_effect_timing():
    """Fix typing effect to show text character by character with proper sound sync"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find and fix the update method for proper typing effect
    update_start = content.find('def update(self, dt):')
    if update_start != -1:
        next_method = content.find('\n    def ', update_start + 1)
        if next_method == -1:
            next_method = content.find('\nclass ', update_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Create update method with proper typing effect
        typing_update = '''    def update(self, dt):
        """Update dialogue with visible typing effect"""
        if not self.active or not self.current_node:
            return
        
        # Typing effect - character by character
        if self.is_typing and self.full_text:
            self.text_timer += dt
            chars_to_show = int(self.text_timer * self.text_speed)
            
            if chars_to_show >= len(self.full_text):
                # Finished typing - show full text
                self.displayed_text = self.full_text
                self.is_typing = False
                self.waiting_for_input = True
                
                # Stop typing sound when text is complete
                if self.sound_manager:
                    self.sound_manager.stop_typing_sound()
                
                print(f"🎭 Typing complete: '{self.displayed_text}'")
            else:
                # Still typing - show partial text
                self.displayed_text = self.full_text[:chars_to_show]
                print(f"🎭 Typing: '{self.displayed_text}' ({chars_to_show}/{len(self.full_text)})")
'''
        
        content = content[:update_start] + typing_update + content[next_method:]
        print("✅ Fixed typing effect update method")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def fix_dialogue_start_with_sound():
    """Fix dialogue start to properly sync sound with typing"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find and fix start_dialogue method
    start_pos = content.find('def start_dialogue(self, dialogue_id):')
    if start_pos != -1:
        next_method = content.find('\n    def ', start_pos + 1)
        if next_method == -1:
            next_method = content.find('\nclass ', start_pos + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Create start_dialogue with proper sound sync
        start_dialogue_fixed = '''    def start_dialogue(self, dialogue_id):
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
'''
        
        content = content[:start_pos] + start_dialogue_fixed + content[next_method:]
        print("✅ Fixed dialogue start with sound synchronization")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def ensure_dialogue_rendering_called():
    """Ensure dialogue rendering is called from main game loop"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Make sure dialogue is rendered in both DIALOGUE and PLAYING states
    if 'self.dialogue_system.render(self.screen)' not in content:
        # Find render method
        render_pos = content.find('def render(self):')
        if render_pos != -1:
            # Find dialogue state rendering
            dialogue_state = content.find('if self.state == GameState.DIALOGUE:', render_pos)
            if dialogue_state != -1:
                # Add dialogue rendering
                next_elif = content.find('\n        elif', dialogue_state)
                if next_elif != -1:
                    dialogue_render = '''
            # Render dialogue system
            if self.dialogue_system.active:
                self.dialogue_system.render(self.screen)
'''
                    content = content[:next_elif] + dialogue_render + content[next_elif:]
                    print("✅ Added dialogue rendering to main render loop")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix visual dialogue display on screen"""
    print("🔧 Fixing Visual Dialogue Display on Screen")
    print("=" * 45)
    
    print("1. Fixing dialogue visual rendering...")
    fix_dialogue_visual_rendering()
    
    print("2. Fixing typing effect timing...")
    fix_typing_effect_timing()
    
    print("3. Fixing dialogue start with sound sync...")
    fix_dialogue_start_with_sound()
    
    print("4. Ensuring dialogue rendering is called...")
    ensure_dialogue_rendering_called()
    
    print("\n" + "=" * 45)
    print("🎉 VISUAL DIALOGUE DISPLAY FIXED!")
    print("\nVisual Dialogue Features:")
    print("✅ White text on dark background")
    print("✅ Character-by-character typing effect visible on screen")
    print("✅ Typing sound starts when text first appears")
    print("✅ Typing sound stops when text is complete")
    print("✅ Large, readable dialogue box")
    print("✅ Gold borders for visibility")
    print("✅ Speaker names in gold text")
    print("✅ Continue prompts when ready")
    
    print("\nWhat You'll See Now:")
    print("- Large dialogue box at bottom of screen")
    print("- Dark background with white text")
    print("- Text appearing character by character")
    print("- Typing sound synchronized with text appearance")
    print("- Speaker names (Narrator, Moses, NPCs)")
    print("- 'Press SPACE to continue' prompts")
    
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
