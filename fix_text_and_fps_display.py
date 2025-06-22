#!/usr/bin/env python3
"""
Fix item consumption text stacking and FPS display issues
"""

def fix_item_consumption_text():
    """Fix item consumption text to disappear after 1 second"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add text timer system to __init__
    init_marker = "def __init__(self):"
    init_pos = content.find(init_marker)
    if init_pos != -1:
        # Find end of __init__ method
        next_method = content.find("\n    def ", init_pos + 1)
        if next_method != -1:
            # Add text timer system before the end of __init__
            text_timer_init = '''
        # Text display timer system
        self.consumption_text = ""
        self.consumption_text_timer = 0.0
        self.consumption_text_duration = 1.0  # 1 second display time
        
        print("✅ Item consumption text timer system initialized")'''
            
            insertion_point = content.rfind('\n', init_pos, next_method)
            content = content[:insertion_point] + text_timer_init + content[insertion_point:]
            print("✅ Added text timer system to initialization")
    
    # Add text timer update to the main update method
    if "def update(self, dt):" in content:
        # Find the update method and add text timer update
        update_pos = content.find("def update(self, dt):")
        if update_pos != -1:
            next_method = content.find("\n    def ", update_pos + 1)
            if next_method != -1:
                # Add text timer update
                text_timer_update = '''
        # Update consumption text timer
        if self.consumption_text_timer > 0:
            self.consumption_text_timer -= dt
            if self.consumption_text_timer <= 0:
                self.consumption_text = ""  # Clear text after timer expires
'''
                # Find a good insertion point in the update method
                insertion_point = content.find("self.level_manager.update(dt)", update_pos)
                if insertion_point != -1:
                    insertion_point = content.find('\n', insertion_point) + 1
                    content = content[:insertion_point] + text_timer_update + content[insertion_point:]
                    print("✅ Added text timer update to main update method")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_item_usage_text_display():
    """Fix item usage to use timed text display"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find item usage methods and update them to use timed text
    old_item_usage_patterns = [
        'print(f"🍞 Used {item_name}! Health restored by {heal_amount}")',
        'print(f"💧 Used {item_name}! Health restored by {heal_amount}")',
        'print(f"🥩 Used {item_name}! Health restored by {heal_amount}")',
        'print(f"📜 Used {item_name}! Wisdom gained")',
        'print(f"🛡️ Used {item_name}! Armor of God activated")',
        'print(f"🪄 Used {item_name}! Staff activated")'
    ]
    
    new_item_usage_patterns = [
        'self.show_consumption_text(f"🍞 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"💧 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"🥩 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"📜 Used {item_name}! Wisdom gained")',
        'self.show_consumption_text(f"🛡️ Used {item_name}! Armor of God activated")',
        'self.show_consumption_text(f"🪄 Used {item_name}! Staff activated")'
    ]
    
    for old_pattern, new_pattern in zip(old_item_usage_patterns, new_item_usage_patterns):
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Updated item usage text: {old_pattern[:20]}...")
    
    # Add the show_consumption_text method
    if "def show_consumption_text(self" not in content:
        # Find a good place to add the method
        class_methods_end = content.find("def main():")
        if class_methods_end == -1:
            class_methods_end = len(content) - 100
        
        show_consumption_text_method = '''
    def show_consumption_text(self, text):
        """Show consumption text that disappears after 1 second"""
        self.consumption_text = text
        self.consumption_text_timer = self.consumption_text_duration
        print(text)  # Also print to console for debugging

'''
        
        content = content[:class_methods_end] + show_consumption_text_method + content[class_methods_end:]
        print("✅ Added show_consumption_text method")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_fps_display():
    """Remove always-visible FPS and make it toggle with F1"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Remove the always-visible FPS counter
    old_fps_counter = '''        
        # FPS Counter and Performance Monitoring
        if hasattr(self, 'clock'):
            fps = self.clock.get_fps()
            if fps > 0:  # Avoid division by zero
                fps_text = self.font_manager.get_font('small').render(f"FPS: {fps:.1f}", True, (255, 255, 255))
                self.screen.blit(fps_text, (10, 10))
                
                # Performance warning
                if fps < 30:
                    warning_text = self.font_manager.get_font('small').render("Low FPS - Consider reducing quality", True, (255, 255, 0))
                    self.screen.blit(warning_text, (10, 35))'''
    
    new_fps_counter = '''        
        # FPS Counter - Only show when toggled with F1
        if hasattr(self, 'show_fps') and self.show_fps and hasattr(self, 'clock'):
            fps = self.clock.get_fps()
            if fps > 0:  # Avoid division by zero
                fps_text = self.font_manager.get_font('small').render(f"FPS: {fps:.1f}", True, (255, 255, 255))
                self.screen.blit(fps_text, (10, 10))
                
                # Performance warning
                if fps < 30:
                    warning_text = self.font_manager.get_font('small').render("Low FPS - Consider reducing quality", True, (255, 255, 0))
                    self.screen.blit(warning_text, (10, 35))'''
    
    if old_fps_counter in content:
        content = content.replace(old_fps_counter, new_fps_counter)
        print("✅ Updated FPS counter to toggle with F1")
    
    # Add FPS toggle variable to initialization
    if "self.show_fps = False" not in content:
        init_marker = "def __init__(self):"
        init_pos = content.find(init_marker)
        if init_pos != -1:
            next_method = content.find("\n    def ", init_pos + 1)
            if next_method != -1:
                fps_toggle_init = '''
        # FPS display toggle
        self.show_fps = False
        
        print("✅ FPS toggle system initialized (Press F1 to show/hide)")'''
                
                insertion_point = content.rfind('\n', init_pos, next_method)
                content = content[:insertion_point] + fps_toggle_init + content[insertion_point:]
                print("✅ Added FPS toggle variable to initialization")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_f1_fps_toggle():
    """Add F1 key handling for FPS toggle"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the event handling section and add F1 toggle
    if "pygame.K_F11:" in content:
        # Add F1 handling before F11
        old_f11_handler = "                elif event.key == pygame.K_F11:"
        new_f1_and_f11_handler = '''                elif event.key == pygame.K_F1:
                    # Toggle FPS display
                    self.show_fps = not self.show_fps
                    fps_status = "ON" if self.show_fps else "OFF"
                    print(f"📊 FPS display toggled {fps_status}")
                
                elif event.key == pygame.K_F11:'''
        
        if old_f11_handler in content:
            content = content.replace(old_f11_handler, new_f1_and_f11_handler)
            print("✅ Added F1 key handler for FPS toggle")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_consumption_text_rendering():
    """Add rendering for consumption text"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the render method and add consumption text rendering
    render_method_pos = content.find("def render_game(self):")
    if render_method_pos != -1:
        # Find end of render method
        next_method = content.find("\n    def ", render_method_pos + 1)
        if next_method != -1:
            # Add consumption text rendering
            consumption_text_render = '''
        # Render consumption text (disappears after 1 second)
        if hasattr(self, 'consumption_text') and self.consumption_text and self.consumption_text_timer > 0:
            text_surface = self.font_manager.get_font('medium').render(self.consumption_text, True, (255, 255, 255))
            # Position text in center-top of screen
            text_rect = text_surface.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = 50
            
            # Add background for better visibility
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
            
            self.screen.blit(text_surface, text_rect)
'''
            
            # Find a good insertion point (before FPS counter)
            insertion_point = content.find("# FPS Counter", render_method_pos)
            if insertion_point == -1:
                insertion_point = content.rfind('\n        pygame.display.flip()', render_method_pos, next_method)
            
            if insertion_point != -1:
                content = content[:insertion_point] + consumption_text_render + content[insertion_point:]
                print("✅ Added consumption text rendering")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix item consumption text stacking and FPS display issues"""
    print("🔧 Fixing Item Consumption Text and FPS Display")
    print("=" * 50)
    
    print("1. Fixing item consumption text timer system...")
    fix_item_consumption_text()
    
    print("2. Updating item usage to use timed text display...")
    fix_item_usage_text_display()
    
    print("3. Fixing FPS display to toggle with F1...")
    fix_fps_display()
    
    print("4. Adding F1 key handler for FPS toggle...")
    add_f1_fps_toggle()
    
    print("5. Adding consumption text rendering...")
    add_consumption_text_rendering()
    
    print("\n" + "=" * 50)
    print("🎉 TEXT AND FPS DISPLAY FIXES COMPLETE!")
    print("\nItem Consumption Text Fixes:")
    print("✅ Text disappears after 1 second (no more stacking)")
    print("✅ Timed display system implemented")
    print("✅ Clean text rendering with background")
    print("✅ Centered display for better visibility")
    print("\nFPS Display Fixes:")
    print("✅ FPS counter removed from always-visible")
    print("✅ FPS now toggles with F1 key")
    print("✅ Clean interface when FPS is hidden")
    print("✅ Performance warnings only when FPS is shown")
    print("\nEnhanced Features:")
    print("- Item consumption text shows for 1 second then disappears")
    print("- No more text stacking on screen")
    print("- F1 toggles FPS display ON/OFF")
    print("- Clean interface without constant FPS display")
    print("- Better text visibility with background")
    print("\nControls:")
    print("- F1: Toggle FPS display ON/OFF")
    print("- Number keys (1-9): Use items (text shows for 1 second)")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
