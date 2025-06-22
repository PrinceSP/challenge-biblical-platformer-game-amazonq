#!/usr/bin/env python3
"""
Fix indentation issues comprehensively
"""

def fix_indentation_issues():
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
        
        # Detect method definitions
        if line.strip().startswith('def ') and ':' in line and in_class:
            # Methods should be indented 4 spaces from class
            expected_indent = class_indent + 4
            current_indent = len(line) - len(line.lstrip())
            
            if current_indent != expected_indent:
                # Fix the indentation
                fixed_line = ' ' * expected_indent + line.lstrip()
                fixed_lines.append(fixed_line)
                print(f"✅ Fixed method indentation on line {i+1}")
            else:
                fixed_lines.append(line)
            continue
        
        # For other lines, maintain relative indentation
        fixed_lines.append(line)
    
    with open('game_systems.py', 'w') as f:
        f.writelines(fixed_lines)
    
    return True

def validate_syntax():
    """Validate that the file compiles correctly"""
    
    try:
        with open('game_systems.py', 'r') as f:
            compile(f.read(), 'game_systems.py', 'exec')
        print("✅ Syntax validation successful!")
        return True
    except (IndentationError, SyntaxError) as e:
        print(f"❌ Error on line {e.lineno}: {e}")
        if e.text:
            print(f"   Problem line: {e.text.strip()}")
        return False

def main():
    """Fix indentation issues"""
    print("🔧 Fixing Indentation Issues")
    print("=" * 30)
    
    print("1. Fixing indentation...")
    fix_indentation_issues()
    
    print("2. Validating syntax...")
    if validate_syntax():
        print("\n" + "=" * 30)
        print("✅ INDENTATION FIXED!")
        print("Test with: python3 main.py")
    else:
        print("\n" + "=" * 30)
        print("⚠️  Manual review may be needed")

if __name__ == "__main__":
    main()
