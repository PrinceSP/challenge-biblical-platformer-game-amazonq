#!/usr/bin/env python3
"""
Fix the if-elif structure that's causing syntax errors
"""

def fix_if_elif_structure():
    """Fix the if-elif structure"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the specific issue where elif appears without a corresponding if
    old_structure = '''            # Global key events
            if event.type == pygame.KEYDOWN:
                elif event.key == pygame.K_F1:'''
    
    new_structure = '''            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:'''
    
    if old_structure in content:
        content = content.replace(old_structure, new_structure)
        print("✅ Fixed if-elif structure - changed elif to if for first condition")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def validate_and_test():
    """Validate syntax and test compilation"""
    
    try:
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("✅ Syntax validation successful!")
        return True
    except (IndentationError, SyntaxError) as e:
        print(f"❌ Error on line {e.lineno}: {e}")
        if e.text:
            print(f"   Problem line: {e.text.strip()}")
        return False

def main():
    """Fix if-elif structure"""
    print("🔧 Fixing If-Elif Structure")
    print("=" * 25)
    
    print("1. Fixing if-elif structure...")
    fix_if_elif_structure()
    
    print("2. Validating syntax...")
    if validate_and_test():
        print("\n" + "=" * 25)
        print("🎉 SYNTAX FIXED SUCCESSFULLY!")
        print("\nMoses Adventure is now ready to run!")
        print("All indentation errors have been resolved.")
        print("\nTest with: python3 main.py")
    else:
        print("\n" + "=" * 25)
        print("⚠️  Still working on remaining issues...")

if __name__ == "__main__":
    main()
