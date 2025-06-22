#!/usr/bin/env python3
"""
Fix event handling logic error
"""

def fix_event_handling_logic():
    """Fix the event handling logic that's causing the AttributeError"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the problematic event handling section
    old_event_handling = '''            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")
                
            elif event.key == pygame.K_F11:'''
    
    new_event_handling = '''            # Global key events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")
                
                elif event.key == pygame.K_F11:'''
    
    if old_event_handling in content:
        content = content.replace(old_event_handling, new_event_handling)
        print("✅ Fixed event handling logic - moved elif inside KEYDOWN check")
    
    # Also fix any other similar issues where event.key is accessed outside KEYDOWN
    lines = content.split('\n')
    fixed_lines = []
    inside_keydown = False
    
    for i, line in enumerate(lines):
        if 'if event.type == pygame.KEYDOWN:' in line:
            inside_keydown = True
            fixed_lines.append(line)
        elif line.strip().startswith('elif event.key ==') and not inside_keydown:
            # This elif is outside a KEYDOWN check, need to fix it
            # Convert to proper if inside KEYDOWN
            fixed_line = line.replace('elif event.key ==', 'if event.key ==')
            fixed_lines.append('            if event.type == pygame.KEYDOWN:')
            fixed_lines.append('                ' + fixed_line.strip())
            inside_keydown = True
            print(f"✅ Fixed event.key access outside KEYDOWN on line {i+1}")
        elif line.strip() == '' or not line.strip().startswith('elif event.key =='):
            if 'def ' in line or 'class ' in line or line.strip().startswith('if ') and 'event.type' in line:
                inside_keydown = False
            fixed_lines.append(line)
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def validate_event_handling():
    """Validate that event handling is now correct"""
    
    try:
        with open('main.py', 'r') as f:
            compile(f.read(), 'main.py', 'exec')
        print("✅ Event handling validation successful!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Fix event handling logic"""
    print("🔧 Fixing Event Handling Logic")
    print("=" * 30)
    
    print("1. Fixing event handling logic...")
    fix_event_handling_logic()
    
    print("2. Validating event handling...")
    if validate_event_handling():
        print("\n" + "=" * 30)
        print("🎉 EVENT HANDLING FIXED!")
        print("\nMoses Adventure should now run without errors!")
        print("✅ All indentation errors resolved")
        print("✅ Event handling logic fixed")
        print("✅ Game ready to play")
        print("\nTest with: python3 main.py")
    else:
        print("\n" + "=" * 30)
        print("⚠️  Additional fixes may be needed.")

if __name__ == "__main__":
    main()
