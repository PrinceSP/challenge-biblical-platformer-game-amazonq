#!/usr/bin/env python3
"""
Fix indentation error in main.py
"""

def fix_indentation():
    """Fix the indentation error"""
    
    with open('main.py', 'r') as f:
        lines = f.readlines()
    
    # Fix indentation around line 842
    for i, line in enumerate(lines):
        if 'self.level_manager.update_simple_enemies(dt)' in line:
            # Fix the indentation
            lines[i] = '        self.level_manager.update_simple_enemies(dt)\n'
            print(f"✅ Fixed indentation on line {i+1}")
            break
    
    with open('main.py', 'w') as f:
        f.writelines(lines)
    
    return True

def main():
    """Fix indentation error"""
    print("🔧 Fixing Indentation Error")
    print("=" * 25)
    
    if fix_indentation():
        print("✅ INDENTATION ERROR FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix indentation error")

if __name__ == "__main__":
    main()
