#!/usr/bin/env python3
"""
Fix all indentation issues comprehensively
"""

def fix_all_indentation():
    """Fix all indentation issues in both files"""
    
    # Fix game_systems.py
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    fixed_lines = []
    in_class = False
    class_indent = 0
    
    for i, line in enumerate(lines):
        if line.strip().startswith('class ') and ':' in line:
            in_class = True
            class_indent = len(line) - len(line.lstrip())
            fixed_lines.append(line)
        elif line.strip().startswith('def ') and in_class:
            # Method should be indented 4 spaces from class
            method_line = ' ' * (class_indent + 4) + line.lstrip()
            fixed_lines.append(method_line)
        elif line.strip().startswith('"""') and in_class:
            # Docstring should be indented 8 spaces from class
            docstring_line = ' ' * (class_indent + 8) + line.lstrip()
            fixed_lines.append(docstring_line)
        else:
            fixed_lines.append(line)
    
    with open('game_systems.py', 'w') as f:
        f.write('\n'.join(fixed_lines))
    
    print("✅ Fixed game_systems.py indentation")
    
    # Fix main.py
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Remove duplicate dialogue update lines
    content = content.replace('            self.dialogue_system.update(dt)\n\n            self.dialogue_system.update(dt)', 
                             '            self.dialogue_system.update(dt)')
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed main.py indentation and duplicates")
    
    return True

def validate_syntax():
    """Validate syntax of both files"""
    
    try:
        with open('game_systems.py', 'r') as f:
            compile(f.read(), 'game_systems.py', 'exec')
        print("✅ game_systems.py syntax valid")
    except Exception as e:
        print(f"❌ game_systems.py error: {e}")
        return False
    
    try:
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("✅ main.py syntax valid")
    except Exception as e:
        print(f"❌ main.py error: {e}")
        return False
    
    return True

def main():
    """Fix all indentation issues"""
    print("🔧 Fixing All Indentation Issues")
    print("=" * 35)
    
    fix_all_indentation()
    
    if validate_syntax():
        print("\n" + "=" * 35)
        print("🎉 ALL INDENTATION FIXED!")
        print("Ready to test: python3 main.py")
    else:
        print("\n" + "=" * 35)
        print("⚠️  Some issues may remain")

if __name__ == "__main__":
    main()
