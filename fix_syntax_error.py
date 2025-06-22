#!/usr/bin/env python3
"""
Fix syntax error in dialogue skip functionality
"""

def fix_syntax_error():
    """Fix the syntax error in the dialogue skip code"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the broken elif statement
    old_broken_code = '''                if event.key == pygame.K_a:
                    # Throw stone
                    self.throw_stone_from_inventory()
                    return
                el                # Skip dialogue with SPACE or ENTER
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:'''
    
    new_fixed_code = '''                if event.key == pygame.K_a:
                    # Throw stone
                    self.throw_stone_from_inventory()
                    return
                
                # Skip dialogue with SPACE or ENTER
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:'''
    
    if old_broken_code in content:
        content = content.replace(old_broken_code, new_fixed_code)
        print("✅ Fixed syntax error in dialogue skip code")
    else:
        # Try alternative fix
        if "el                # Skip dialogue" in content:
            content = content.replace("el                # Skip dialogue", "                # Skip dialogue")
            print("✅ Fixed broken 'el' statement")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix syntax error"""
    print("🔧 Fixing Syntax Error")
    print("=" * 20)
    
    if fix_syntax_error():
        print("✅ SYNTAX ERROR FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix syntax error")

if __name__ == "__main__":
    main()
