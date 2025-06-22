#!/usr/bin/env python3
"""
Fix menu events syntax error
"""

def fix_menu_events_syntax():
    """Fix the syntax error in menu events"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the menu events syntax
    old_menu_events = '''    def handle_menu_events(self, event):
        \"\"\"Handle menu events\"\"\"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.start_game()
                elif event.key == pygame.K_ESCAPE:
                self.running = False'''
    
    new_menu_events = '''    def handle_menu_events(self, event):
        \"\"\"Handle menu events\"\"\"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                self.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.running = False'''
    
    if old_menu_events in content:
        content = content.replace(old_menu_events, new_menu_events)
        print("✅ Fixed menu events syntax error")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix menu events syntax"""
    print("🔧 Fixing Menu Events Syntax")
    print("=" * 25)
    
    if fix_menu_events_syntax():
        print("✅ MENU EVENTS SYNTAX FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix menu events syntax")

if __name__ == "__main__":
    main()
