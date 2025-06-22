#!/usr/bin/env python3
"""
Final comprehensive indentation fix
"""

def fix_all_indentation_issues():
    """Fix all indentation issues in game_systems.py"""
    
    with open('game_systems.py', 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_class = False
    class_indent = 0
    
    for i, line in enumerate(lines):
        original_line = line
        
        # Detect class definitions
        if line.strip().startswith('class ') and ':' in line:
            in_class = True
            class_indent = len(line) - len(line.lstrip())
            fixed_lines.append(line)
            continue
        
        # Fix method definitions
        if line.strip().startswith('def ') and in_class:
            # Methods should be indented 4 spaces from class
            method_line = ' ' * (class_indent + 4) + line.lstrip()
            fixed_lines.append(method_line)
            continue
        
        # Fix docstrings
        if line.strip().startswith('"""') and in_class:
            # Docstrings should be indented 8 spaces from class
            docstring_line = ' ' * (class_indent + 8) + line.lstrip()
            fixed_lines.append(docstring_line)
            continue
        
        # Keep other lines as is
        fixed_lines.append(line)
    
    with open('game_systems.py', 'w') as f:
        f.writelines(fixed_lines)
    
    print("✅ Fixed all indentation issues")
    return True

def validate_syntax():
    """Validate that the syntax is correct"""
    
    try:
        with open('game_systems.py', 'r') as f:
            compile(f.read(), 'game_systems.py', 'exec')
        print("✅ Syntax validation successful")
        return True
    except Exception as e:
        print(f"❌ Syntax error: {e}")
        return False

def main():
    """Fix all indentation issues"""
    print("🔧 Final Indentation Fix")
    print("=" * 25)
    
    fix_all_indentation_issues()
    
    if validate_syntax():
        print("\n" + "=" * 25)
        print("🎉 ALL INDENTATION FIXED!")
        print("Ready to test visual dialogue!")
    else:
        print("❌ Still has syntax issues")

if __name__ == "__main__":
    main()
