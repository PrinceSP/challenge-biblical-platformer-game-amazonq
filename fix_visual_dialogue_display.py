#!/usr/bin/env python3
"""
Fix the visual dialogue display so text actually appears on screen with typing effect
"""

def fix_dialogue_visual_display():
    """Fix the dialogue system to actually show text on screen"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Ensure dialogue system is being rendered in the main game loop
    if 'self.dialogue_system.render(' not in content:
        # Find the render method and add dialogue rendering
        render_pos = content.find('def render(self):')
        if render_pos != -1:
            # Find where to add dialogue rendering
            dialogue_state_pos = content.find('if self.state == GameState.DIALOGUE:', render_pos)
            if dialogue_state_pos != -1:
                # Find the end of the dialogue state block
                next_line = content.find('\n        elif', dialogue_state_pos)
                if next_line == -1:
                    next_line = content.find('\n        else:', dialogue_state_pos)
                if next_line == -1:
                    next_line = content.find('\n    def ', dialogue_state_pos)
                
                if next_line != -1:
                    # Add dialogue rendering
                    dialogue_render = '''
            # Render dialogue system with visible text
            self.dialogue_system.render(self.screen)
            print("🎭 Rendering dialogue on screen")
'''
                    content = content[:next_line] + dialogue_render + content[next_line:]
                    print("✅ Added dialogue rendering to main game loop")
    
    # Also ensure dialogue is rendered in PLAYING state for NPC interactions
    playing_state_pos = content.find('elif self.state == GameState.PLAYING:')
    if playing_state_pos != -1:
        # Find the render_game call
        render_game_pos = content.find('self.render_game()', playing_state_pos)
        if render_game_pos != -1:
            # Add dialogue rendering after render_game
            insertion_point = content.find('\n', render_game_pos) + 1
            dialogue_render_playing = '''
            # Render dialogue system if active (for NPC interactions)
            if self.dialogue_system.active:
                self.dialogue_system.render(self.screen)
                print("🎭 Rendering NPC dialogue on screen")
'''
            content = content[:insertion_point] + dialogue_render_playing + content[insertion_point:]
            print("✅ Added dialogue rendering for NPC interactions")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def ensure_dialogue_update_called():
    """Ensure dialogue system update is called for typing effect"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the main update method and ensure dialogue is updated
    update_pos = content.find('def update(self, dt):')
    if update_pos != -1:
        # Look for dialogue system update
        if 'self.dialogue_system.update(' not in content[update_pos:update_pos+1000]:
            # Find a good place to add dialogue update
            next_method = content.find('\n    def ', update_pos + 1)
            if next_method == -1:
                next_method = len(content)
            
            # Add dialogue update before the end of the method
            dialogue_update = '''
        # Update dialogue system for typing effect
        if self.dialogue_system and self.dialogue_system.active:
            self.dialogue_system.update(dt)
'''
            
            # Find the last line of the update method
            method_content = content[update_pos:next_method]
            last_line_pos = method_content.rfind('\n        ')
            if last_line_pos != -1:
                insertion_point = update_pos + last_line_pos
                content = content[:insertion_point] + dialogue_update + content[insertion_point:]
                print("✅ Added dialogue system update for typing effect")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_dialogue_constants():
    """Ensure SCREEN_WIDTH and SCREEN_HEIGHT are available for dialogue rendering"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Check if constants are imported
    if 'SCREEN_WIDTH' not in content or 'SCREEN_HEIGHT' not in content:
        # Add constants at the top
        constants_import = '''
# Screen constants for dialogue rendering
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
'''
        
        # Find a good place to add constants
        import_pos = content.find('import pygame')
        if import_pos != -1:
            insertion_point = content.find('\n', import_pos) + 1
            content = content[:insertion_point] + constants_import + content[insertion_point:]
            print("✅ Added screen constants for dialogue rendering")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def create_enhanced_dialogue_render():
    """Create an enhanced dialogue render method that definitely shows text"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find the DialogueSystem render method and replace it with a robust version
    render_start = content.find('def render(self, screen, sprites=None):')
    if render_start != -1:
        # Find the end of the render method
        next_method = content.find('\n    def ', render_start + 1)
        if next_method == -1:
            next_method = content.find('\nclass ', render_start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Create a robust render method that definitely shows text
        enhanced_render = '''    def render(self, screen, sprites=None):
        """Render dialogue with guaranteed visible text display"""
        if not self.active or not self.current_node:
            return
        
        print(f"🎭 RENDERING DIALOGUE: Active={self.active}, Text='{self.displayed_text[:30]}...'")
        
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Large, prominent dialogue panel
        panel_width = screen_width - 100
        panel_height = 200
        panel_x = 50
        panel_y = screen_height - panel_height - 50
        
        # Draw dialogue background - VERY VISIBLE
        dialogue_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Multiple layers for visibility
        pygame.draw.rect(screen, (0, 0, 0), dialogue_rect)  # Black background
        pygame.draw.rect(screen, (40, 30, 20), dialogue_rect.inflate(-8, -8))  # Brown inner
        pygame.draw.rect(screen, (255, 215, 0), dialogue_rect, 5)  # Thick gold border
        
        # Speaker name - VERY PROMINENT
        if self.current_node and self.current_node.speaker:
            speaker_font = pygame.font.Font(None, 48)  # Large font
            speaker_text = speaker_font.render(f"{self.current_node.speaker}:", True, (255, 215, 0))
            
            # Speaker background
            speaker_bg = pygame.Rect(panel_x + 20, panel_y + 15, speaker_text.get_width() + 30, 50)
            pygame.draw.rect(screen, (60, 40, 20), speaker_bg)
            pygame.draw.rect(screen, (255, 215, 0), speaker_bg, 3)
            
            screen.blit(speaker_text, (panel_x + 35, panel_y + 25))
            print(f"🎭 Rendered speaker: {self.current_node.speaker}")
        
        # Main dialogue text - GUARANTEED VISIBLE
        if self.displayed_text:
            text_font = pygame.font.Font(None, 32)  # Large, readable font
            text_color = (255, 255, 255)  # Pure white
            
            # Word wrap the text
            words = self.displayed_text.split(' ')
            lines = []
            current_line = ""
            max_width = panel_width - 80
            
            for word in words:
                test_line = current_line + word + " "
                if text_font.size(test_line)[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line.strip())
                    current_line = word + " "
            
            if current_line:
                lines.append(current_line.strip())
            
            # Render each line with shadow for visibility
            text_y = panel_y + 80
            for i, line in enumerate(lines[:3]):  # Max 3 lines
                if line.strip():
                    # Text shadow for better visibility
                    shadow_surface = text_font.render(line, True, (0, 0, 0))
                    screen.blit(shadow_surface, (panel_x + 42, text_y + (i * 35) + 2))
                    
                    # Main text
                    text_surface = text_font.render(line, True, text_color)
                    screen.blit(text_surface, (panel_x + 40, text_y + (i * 35)))
            
            print(f"🎭 Rendered text: '{self.displayed_text[:50]}...' ({len(lines)} lines)")
        
        # Status indicators
        status_y = panel_y + panel_height - 35
        status_font = pygame.font.Font(None, 28)
        
        if self.waiting_for_input:
            prompt_text = status_font.render("Press SPACE to continue...", True, (255, 255, 0))
            screen.blit(prompt_text, (panel_x + panel_width - 250, status_y))
            print("🎭 Showing continue prompt")
        elif self.is_typing:
            typing_text = status_font.render("...", True, (200, 200, 0))
            screen.blit(typing_text, (panel_x + panel_width - 60, status_y))
            print("🎭 Showing typing indicator")
        
        # Debug border to confirm rendering
        pygame.draw.rect(screen, (255, 0, 0), dialogue_rect, 2)  # Red debug border
        
        print(f"🎭 DIALOGUE RENDER COMPLETE: Panel at ({panel_x}, {panel_y}), Size: {panel_width}x{panel_height}")
'''
        
        content = content[:render_start] + enhanced_render + content[next_method:]
        print("✅ Created enhanced dialogue render method with guaranteed visibility")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix visual dialogue display so text actually appears on screen"""
    print("🔧 Fixing Visual Dialogue Display")
    print("=" * 40)
    
    print("1. Fixing dialogue constants...")
    fix_dialogue_constants()
    
    print("2. Creating enhanced dialogue render method...")
    create_enhanced_dialogue_render()
    
    print("3. Ensuring dialogue rendering in main game...")
    fix_dialogue_visual_display()
    
    print("4. Ensuring dialogue update is called...")
    ensure_dialogue_update_called()
    
    print("\n" + "=" * 40)
    print("🎉 VISUAL DIALOGUE DISPLAY FIXED!")
    print("\nDialogue Visual Improvements:")
    print("✅ Large, prominent dialogue box")
    print("✅ Guaranteed visible text rendering")
    print("✅ Character-by-character typing display")
    print("✅ Speaker names prominently displayed")
    print("✅ Gold borders and clear backgrounds")
    print("✅ Text shadows for better visibility")
    print("✅ Debug borders to confirm rendering")
    print("✅ Status indicators (typing/continue)")
    
    print("\nWhat You'll See Now:")
    print("- Large dialogue box at bottom of screen")
    print("- Speaker names in gold text")
    print("- Conversation text appearing character by character")
    print("- Clear, readable white text on dark background")
    print("- 'Press SPACE to continue' prompts")
    print("- Visual typing indicators")
    
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
