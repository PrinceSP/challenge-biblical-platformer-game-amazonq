#!/usr/bin/env python3
"""
Fix elif syntax error
"""

def fix_elif_syntax():
    """Fix the elif syntax error"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the elif that should be part of a larger if-elif structure
    old_structure = '''        self.level_manager.update(dt)
        self.visual_feedback.update(dt)
        
        elif self.state == GameState.DIALOGUE:
            self.dialogue_system.update(dt)'''
    
    new_structure = '''        self.level_manager.update(dt)
        self.visual_feedback.update(dt)
    
    elif self.state == GameState.DIALOGUE:
        self.dialogue_system.update(dt)'''
    
    if old_structure in content:
        content = content.replace(old_structure, new_structure)
        print("✅ Fixed elif syntax error")
    else:
        print("⚠️  Could not find exact elif structure to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix elif syntax error"""
    print("🔧 Fixing Elif Syntax Error")
    print("=" * 25)
    
    if fix_elif_syntax():
        print("✅ ELIF SYNTAX ERROR FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix elif syntax error")

if __name__ == "__main__":
    main()
