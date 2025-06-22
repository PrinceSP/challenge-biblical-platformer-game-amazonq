#!/usr/bin/env python3
"""
Fix the elif structure and indentation issues
"""

def fix_elif_structure():
    """Fix the elif structure that's causing syntax errors"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the inventory section
    old_inventory_section = '''            if event.key == pygame.K_i:
                self.inventory.active = True
                self.state = GameState.INVENTORY
                elif event.key == pygame.K_ESCAPE:
                self.paused = True
                self.state = GameState.PAUSED
                # Play pause sound effect
                self.sound_manager.play_pause_sound()
                elif event.key == pygame.K_m:
                self.sound_manager.toggle_music()
                elif event.key == pygame.K_s:'''
    
    new_inventory_section = '''            elif event.key == pygame.K_i:
                self.inventory.active = True
                self.state = GameState.INVENTORY
            elif event.key == pygame.K_ESCAPE:
                self.paused = True
                self.state = GameState.PAUSED
                # Play pause sound effect
                self.sound_manager.play_pause_sound()
            elif event.key == pygame.K_m:
                self.sound_manager.toggle_music()
            elif event.key == pygame.K_s:'''
    
    if old_inventory_section in content:
        content = content.replace(old_inventory_section, new_inventory_section)
        print("✅ Fixed inventory section elif structure")
    
    # Fix any other similar patterns
    # Look for patterns where elif is indented incorrectly after an if block
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Fix elif statements that should be at the same level as their corresponding if
        if 'elif event.key ==' in line:
            # Check if this elif is properly aligned with its corresponding if
            if line.startswith('                elif'):
                # This is likely incorrectly indented - should be at 12 spaces for main event handling
                fixed_line = '            elif' + line[16:]  # Remove extra indentation
                fixed_lines.append(fixed_line)
                print(f"✅ Fixed elif indentation on line {i+1}")
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def validate_syntax():
    """Validate that the syntax is now correct"""
    
    try:
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("✅ Syntax validation passed - no errors!")
        return True
    except (IndentationError, SyntaxError) as e:
        print(f"❌ Error still exists: {e}")
        print(f"   Line {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        return False

def main():
    """Fix elif structure and validate syntax"""
    print("🔧 Fixing Elif Structure and Indentation")
    print("=" * 40)
    
    print("1. Fixing elif structure...")
    fix_elif_structure()
    
    print("2. Validating syntax...")
    if validate_syntax():
        print("\n" + "=" * 40)
        print("🎉 ALL SYNTAX ERRORS FIXED!")
        print("\nThe game should now run without any syntax or indentation errors.")
        print("Test with: python3 main.py")
    else:
        print("\n" + "=" * 40)
        print("⚠️  Some syntax issues may remain.")
        print("Will attempt additional fixes...")

if __name__ == "__main__":
    main()
