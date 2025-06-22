#!/usr/bin/env python3
"""
Fix doubled elif statements and clean up syntax
"""

def fix_doubled_elif():
    """Fix doubled elif statements and clean up the code"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix doubled elif statements
    content = content.replace('elifelif', 'elif')
    print("✅ Fixed doubled elif statements")
    
    # Remove duplicate F1 key handling
    old_f1_duplicate = '''                if event.key == pygame.K_F1:
                    self.show_fps = not self.show_fps
            elif event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")'''
    
    new_f1_single = '''                elif event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")'''
    
    if old_f1_duplicate in content:
        content = content.replace(old_f1_duplicate, new_f1_single)
        print("✅ Removed duplicate F1 key handling")
    
    # Fix any remaining indentation issues
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # Fix any remaining incorrect indentation patterns
        if line.strip().startswith('elif event.key =='):
            # Ensure proper indentation for elif statements in event handling
            if not line.startswith('            elif') and not line.startswith('                elif'):
                # Fix the indentation
                fixed_line = '            elif' + line[line.find('elif') + 4:]
                fixed_lines.append(fixed_line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def validate_final_syntax():
    """Final validation of syntax"""
    
    try:
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("✅ Final syntax validation passed!")
        return True
    except (IndentationError, SyntaxError) as e:
        print(f"❌ Error on line {e.lineno}: {e}")
        if e.text:
            print(f"   Problem line: {e.text.strip()}")
        return False

def main():
    """Fix doubled elif and validate final syntax"""
    print("🔧 Fixing Doubled Elif Statements")
    print("=" * 35)
    
    print("1. Fixing doubled elif statements...")
    fix_doubled_elif()
    
    print("2. Final syntax validation...")
    if validate_final_syntax():
        print("\n" + "=" * 35)
        print("🎉 ALL SYNTAX ERRORS FIXED!")
        print("\nThe Moses Adventure game is now ready to run!")
        print("Test with: python3 main.py")
    else:
        print("\n" + "=" * 35)
        print("⚠️  Additional manual fixes may be needed.")

if __name__ == "__main__":
    main()
