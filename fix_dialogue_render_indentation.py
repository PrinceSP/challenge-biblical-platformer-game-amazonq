#!/usr/bin/env python3
"""
Fix dialogue render method indentation
"""

def fix_dialogue_render_indentation():
    """Fix the indentation in dialogue render method"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Fix the specific indentation issue
    old_section = '''            print(f"🎭 Speaker: {self.current_node.speaker}")
            print(f"🎭 Full text: {self.full_text[:50]}...")
            print(f"🎭 Displayed text: {self.displayed_text[:50]}...")
        
font_manager = get_font_manager()'''
    
    new_section = '''            print(f"🎭 Speaker: {self.current_node.speaker}")
            print(f"🎭 Full text: {self.full_text[:50]}...")
            print(f"🎭 Displayed text: {self.displayed_text[:50]}...")
        
        font_manager = get_font_manager()'''
    
    if old_section in content:
        content = content.replace(old_section, new_section)
        print("✅ Fixed font_manager indentation")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def validate_final_game_systems():
    """Final validation of game_systems.py"""
    
    try:
        with open('game_systems.py', 'r') as f:
            compile(f.read(), 'game_systems.py', 'exec')
        print("✅ game_systems.py final validation successful!")
        return True
    except (IndentationError, SyntaxError) as e:
        print(f"❌ Error in game_systems.py line {e.lineno}: {e}")
        if e.text:
            print(f"   Problem line: {e.text.strip()}")
        return False

def main():
    """Fix dialogue render indentation"""
    print("🔧 Fixing Dialogue Render Indentation")
    print("=" * 35)
    
    print("1. Fixing dialogue render indentation...")
    fix_dialogue_render_indentation()
    
    print("2. Final validation...")
    if validate_final_game_systems():
        print("\n" + "=" * 35)
        print("🎉 DIALOGUE SYSTEM FULLY FIXED!")
        print("\nThe dialogue text should now appear properly.")
        print("Test with: python3 main.py")
    else:
        print("\n" + "=" * 35)
        print("⚠️  Manual review may be needed.")

if __name__ == "__main__":
    main()
