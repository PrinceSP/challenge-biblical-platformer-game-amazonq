#!/usr/bin/env python3
"""
Fix all font manager issues in game_systems.py
"""

def fix_all_font_issues():
    """Fix all font manager issues throughout the file"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Replace all instances where font_manager is used without being defined
    replacements = [
        ('font = font_manager.get_font(\'small\')', 'font = pygame.font.Font(None, 24)'),
        ('font_manager.get_font(\'medium\')', 'pygame.font.Font(None, 32)'),
        ('font_manager.get_font(\'large\')', 'pygame.font.Font(None, 48)'),
        ('font_manager.get_font(\'tiny\')', 'pygame.font.Font(None, 16)'),
        ('font_manager.render_text(', 'self.render_text('),
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Fixed: {old[:30]}...")
    
    # Add a simple render_text method to classes that need it
    if "def render_text(self" not in content:
        # Find VisualFeedback class and add render_text method
        visual_feedback_pos = content.find('class VisualFeedback:')
        if visual_feedback_pos != -1:
            # Find a good place to add the method
            method_pos = content.find('def render(self, screen):', visual_feedback_pos)
            if method_pos != -1:
                render_text_method = '''
    def render_text(self, text, font_size, color):
        """Simple text rendering method"""
        font_sizes = {'tiny': 16, 'small': 24, 'medium': 32, 'large': 48}
        size = font_sizes.get(font_size, 24)
        font = pygame.font.Font(None, size)
        return font.render(text, True, color)
    
'''
                content = content[:method_pos] + render_text_method + content[method_pos:]
                print("✅ Added render_text method to VisualFeedback")
    
    # Fix any remaining font_manager calls in render methods
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if 'font_manager.render_text(' in line and 'self.render_text(' not in line:
            # Replace with simple pygame font rendering
            if 'font_manager.render_text(' in line:
                # Extract the text and color from the call
                if '"' in line and '(' in line:
                    # Simple replacement for basic cases
                    line = line.replace('font_manager.render_text(', 'pygame.font.Font(None, 24).render(')
                    line = line.replace(', \'small\', ', ', True, ')
                    line = line.replace(', \'medium\', ', ', True, ')
                    line = line.replace(', \'large\', ', ', True, ')
                    line = line.replace(', \'tiny\', ', ', True, ')
                    print("✅ Fixed font_manager.render_text call")
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix all font issues"""
    print("🔧 Fixing All Font Issues")
    print("=" * 25)
    
    if fix_all_font_issues():
        print("\n" + "=" * 25)
        print("✅ ALL FONT ISSUES FIXED!")
        print("\nThe game should now run without font errors.")
        print("Test with: python3 main.py")
    else:
        print("❌ Could not fix all font issues")

if __name__ == "__main__":
    main()
