#!/usr/bin/env python3
"""
Add render_text method to DialogueSystem
"""

def add_render_text_to_dialogue():
    """Add render_text method to DialogueSystem class"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find DialogueSystem class and add render_text method
    dialogue_pos = content.find('class DialogueSystem:')
    if dialogue_pos != -1:
        # Find a good place to add the method (after __init__)
        init_end = content.find('def load_dialogue_data(self):', dialogue_pos)
        if init_end != -1:
            render_text_method = '''
    def render_text(self, text, font_size, color):
        """Simple text rendering method"""
        font_sizes = {'tiny': 16, 'small': 24, 'medium': 32, 'large': 48}
        size = font_sizes.get(font_size, 24)
        font = pygame.font.Font(None, size)
        return font.render(text, True, color)
    
'''
            content = content[:init_end] + render_text_method + content[init_end:]
            print("✅ Added render_text method to DialogueSystem")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Add render_text method"""
    print("🔧 Adding render_text Method")
    print("=" * 25)
    
    if add_render_text_to_dialogue():
        print("✅ RENDER_TEXT METHOD ADDED!")
        print("Test with: python3 main.py")
    else:
        print("❌ Could not add render_text method")

if __name__ == "__main__":
    main()
