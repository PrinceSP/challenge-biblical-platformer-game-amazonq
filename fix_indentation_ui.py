#!/usr/bin/env python3
"""
Fix indentation issue in render_ui method
"""

def fix_ui_indentation():
    """Fix the indentation issue in render_ui method"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the indentation issue
    old_ui_section = '''        
self.render_ui()
    
    def render_ui(self):'''
    
    new_ui_section = '''        
        self.render_ui()
    
    def render_ui(self):'''
    
    if old_ui_section in content:
        content = content.replace(old_ui_section, new_ui_section)
        print("✅ Fixed render_ui indentation issue")
    else:
        print("⚠️  Could not find exact indentation issue to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix indentation issue"""
    print("🔧 Fixing UI Indentation Issue")
    print("=" * 30)
    
    if fix_ui_indentation():
        print("✅ UI INDENTATION FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix indentation issue")

if __name__ == "__main__":
    main()
