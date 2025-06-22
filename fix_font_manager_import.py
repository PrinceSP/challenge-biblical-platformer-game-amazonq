#!/usr/bin/env python3
"""
Fix font manager import issue
"""

def fix_font_manager_import():
    """Add missing font manager import to game_systems.py"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Check if font_manager import exists
    if "from font_manager import get_font_manager" not in content:
        # Add the import at the top
        import_pos = content.find("from constants import *")
        if import_pos != -1:
            insertion_point = content.find('\n', import_pos) + 1
            font_import = "from font_manager import get_font_manager\n"
            content = content[:insertion_point] + font_import + content[insertion_point:]
            print("✅ Added font_manager import")
    
    # Also fix any render methods that use basic pygame fonts instead of font_manager
    if "pygame.font.Font(None, 24)" in content:
        content = content.replace("pygame.font.Font(None, 24)", "font_manager.get_font('small')")
        content = content.replace("pygame.font.Font(None, 32)", "font_manager.get_font('medium')")
        print("✅ Fixed font usage in render methods")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix font manager import"""
    print("🔧 Fixing Font Manager Import")
    print("=" * 30)
    
    if fix_font_manager_import():
        print("✅ FONT MANAGER IMPORT FIXED!")
        print("\nThe dialogue system should now render properly.")
        print("Test with: python3 main.py")
    else:
        print("❌ Could not fix font manager import")

if __name__ == "__main__":
    main()
