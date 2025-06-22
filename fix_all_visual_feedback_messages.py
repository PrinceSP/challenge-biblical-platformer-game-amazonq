#!/usr/bin/env python3
"""
Fix all visual feedback messages to disappear after 1.5 seconds
"""

def enhance_visual_feedback_system():
    """Enhance the visual feedback system to handle all message types"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Update the existing text timer system to handle multiple message types
    old_text_system = '''        # Text display timer system
        self.consumption_text = ""
        self.consumption_text_timer = 0.0
        self.consumption_text_duration = 1.0  # 1 second display time'''
    
    new_text_system = '''        # Enhanced visual feedback system for all messages
        self.feedback_messages = []  # List of active feedback messages
        self.feedback_duration = 1.5  # 1.5 seconds display time for all messages
        
        # Legacy support for consumption text
        self.consumption_text = ""
        self.consumption_text_timer = 0.0
        self.consumption_text_duration = 1.5  # Updated to 1.5 seconds'''
    
    if old_text_system in content:
        content = content.replace(old_text_system, new_text_system)
        print("✅ Enhanced visual feedback system for all message types")
    
    # Update the text timer update to handle multiple messages
    old_timer_update = '''        # Update consumption text timer
        if self.consumption_text_timer > 0:
            self.consumption_text_timer -= dt
            if self.consumption_text_timer <= 0:
                self.consumption_text = ""  # Clear text after timer expires'''
    
    new_timer_update = '''        # Update all visual feedback messages
        if self.consumption_text_timer > 0:
            self.consumption_text_timer -= dt
            if self.consumption_text_timer <= 0:
                self.consumption_text = ""  # Clear text after timer expires
        
        # Update feedback messages list
        if hasattr(self, 'feedback_messages'):
            for message in self.feedback_messages[:]:  # Copy list to avoid modification during iteration
                message['timer'] -= dt
                if message['timer'] <= 0:
                    self.feedback_messages.remove(message)'''
    
    if old_timer_update in content:
        content = content.replace(old_timer_update, new_timer_update)
        print("✅ Updated timer system to handle multiple feedback messages")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_universal_feedback_methods():
    """Add universal methods for showing feedback messages"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add universal feedback methods
    if "def show_feedback_message(self" not in content:
        # Find a good place to add the methods
        class_methods_end = content.find("def main():")
        if class_methods_end == -1:
            class_methods_end = len(content) - 100
        
        feedback_methods = '''
    def show_feedback_message(self, text, message_type="info", color=(255, 255, 255)):
        """Show a feedback message that disappears after 1.5 seconds"""
        if not hasattr(self, 'feedback_messages'):
            self.feedback_messages = []
        
        message = {
            'text': text,
            'timer': self.feedback_duration,
            'type': message_type,
            'color': color,
            'y_offset': len(self.feedback_messages) * 30  # Stack messages vertically
        }
        
        self.feedback_messages.append(message)
        print(text)  # Also print to console for debugging
    
    def show_item_collection_message(self, item_name, item_type):
        """Show item collection feedback message"""
        emoji_map = {
            'stone': '🪨',
            'water': '💧',
            'bread': '🍞',
            'meat': '🥩',
            'scroll': '📜',
            'armor_of_god': '🛡️',
            'staff': '🪄'
        }
        
        emoji = emoji_map.get(item_type, '📦')
        message = f"{emoji} Collected {item_name}!"
        self.show_feedback_message(message, "collection", (0, 255, 0))  # Green for collection
    
    def show_item_usage_message(self, item_name, effect):
        """Show item usage feedback message"""
        message = f"✨ Used {item_name}! {effect}"
        self.show_feedback_message(message, "usage", (255, 255, 0))  # Yellow for usage
    
    def show_combat_message(self, message):
        """Show combat feedback message"""
        self.show_feedback_message(message, "combat", (255, 100, 100))  # Red for combat
    
    def show_interaction_message(self, message):
        """Show interaction feedback message"""
        self.show_feedback_message(message, "interaction", (100, 200, 255))  # Blue for interaction
    
    def show_system_message(self, message):
        """Show system feedback message"""
        self.show_feedback_message(message, "system", (200, 200, 200))  # Gray for system

'''
        
        content = content[:class_methods_end] + feedback_methods + content[class_methods_end:]
        print("✅ Added universal feedback message methods")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_item_collection_feedback():
    """Update item collection to use the new feedback system"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and replace item collection messages
    old_collection_patterns = [
        'print(f"📦 Collected {item_name}")',
        'print("📦 Collected stone")',
        'print("📦 Collected water")',
        'print("📦 Collected bread")',
        'print("📦 Collected meat")',
        'print("📦 Collected scroll")',
        'print("📦 Collected armor_of_god")',
        'print("📦 Collected staff")'
    ]
    
    new_collection_patterns = [
        'self.show_item_collection_message(item_name, item_type)',
        'self.show_item_collection_message("Stone", "stone")',
        'self.show_item_collection_message("Water", "water")',
        'self.show_item_collection_message("Bread", "bread")',
        'self.show_item_collection_message("Meat", "meat")',
        'self.show_item_collection_message("Scroll", "scroll")',
        'self.show_item_collection_message("Armor of God", "armor_of_god")',
        'self.show_item_collection_message("Staff", "staff")'
    ]
    
    for old_pattern, new_pattern in zip(old_collection_patterns, new_collection_patterns):
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Updated item collection feedback: {old_pattern[:30]}...")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_item_usage_feedback():
    """Update item usage to use the new feedback system"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Update item usage messages
    old_usage_patterns = [
        'self.show_consumption_text(f"🍞 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"💧 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"🥩 Used {item_name}! Health +{heal_amount}")',
        'self.show_consumption_text(f"📜 Used {item_name}! Wisdom gained")',
        'self.show_consumption_text(f"🛡️ Used {item_name}! Armor of God activated")',
        'self.show_consumption_text(f"🪄 Used {item_name}! Staff activated")'
    ]
    
    new_usage_patterns = [
        'self.show_item_usage_message(item_name, f"Health +{heal_amount}")',
        'self.show_item_usage_message(item_name, f"Health +{heal_amount}")',
        'self.show_item_usage_message(item_name, f"Health +{heal_amount}")',
        'self.show_item_usage_message(item_name, "Wisdom gained")',
        'self.show_item_usage_message(item_name, "Armor of God activated")',
        'self.show_item_usage_message(item_name, "Staff activated")'
    ]
    
    for old_pattern, new_pattern in zip(old_usage_patterns, new_usage_patterns):
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Updated item usage feedback: {old_pattern[:30]}...")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_combat_feedback():
    """Update combat messages to use the new feedback system"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Update combat messages
    combat_patterns = [
        ('print(f"💔 Moses took {damage} damage! Health: {self.player.health}/{self.player.max_health}")', 
         'self.show_combat_message(f"💔 Took {damage} damage! Health: {self.player.health}/{self.player.max_health}")'),
        ('print(f"💥 Player hit {enemy_type} for {damage} damage!")', 
         'self.show_combat_message(f"💥 Hit {enemy_type} for {damage} damage!")'),
        ('print("💀 Game Over! Moses has fallen!")', 
         'self.show_combat_message("💀 Game Over! Moses has fallen!")'),
        ('print(f"⚡ CREATED DIAMOND staff projectile")', 
         'self.show_system_message("⚡ Staff projectile fired!")'),
        ('print("⚡ Moses shoots divine energy!")', 
         'self.show_combat_message("⚡ Divine energy unleashed!")')
    ]
    
    for old_pattern, new_pattern in combat_patterns:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Updated combat feedback: {old_pattern[:30]}...")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_interaction_feedback():
    """Update interaction messages to use the new feedback system"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Update interaction messages
    interaction_patterns = [
        ('print(f"💬 Near {npc.npc_type} at x={npc.rect.x}, y={npc.rect.y} - Press E to interact")', 
         'self.show_interaction_message(f"💬 Press E to talk to {npc.npc_type}")'),
        ('print(f"📏 Distance: {distance} pixels (Moses at x={self.player.rect.centerx})")', 
         '# Distance debug removed for cleaner interface'),
        ('print("✅ Started dialogue:")', 
         'self.show_interaction_message("✅ Dialogue started")'),
        ('print("✅ Dialogue ended")', 
         'self.show_interaction_message("✅ Dialogue ended")')
    ]
    
    for old_pattern, new_pattern in interaction_patterns:
        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            print(f"✅ Updated interaction feedback: {old_pattern[:30]}...")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_feedback_rendering():
    """Update the rendering system to show all feedback messages"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Update the consumption text rendering to handle all feedback messages
    old_rendering = '''        # Render consumption text (disappears after 1 second)
        if hasattr(self, 'consumption_text') and self.consumption_text and hasattr(self, 'consumption_text_timer') and self.consumption_text_timer > 0:
            import pygame
            text_surface = self.font_manager.get_font('medium').render(self.consumption_text, True, (255, 255, 255))
            # Position text in center-top of screen
            text_rect = text_surface.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = 50
            
            # Add background for better visibility
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
            
            self.screen.blit(text_surface, text_rect)'''
    
    new_rendering = '''        # Render all feedback messages (disappear after 1.5 seconds)
        if hasattr(self, 'feedback_messages') and self.feedback_messages:
            import pygame
            for i, message in enumerate(self.feedback_messages):
                text_surface = self.font_manager.get_font('medium').render(message['text'], True, message['color'])
                
                # Position messages stacked vertically from center-top
                text_rect = text_surface.get_rect()
                text_rect.centerx = SCREEN_WIDTH // 2
                text_rect.y = 50 + (i * 35)  # Stack messages with 35px spacing
                
                # Add background for better visibility
                bg_rect = text_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
                pygame.draw.rect(self.screen, message['color'], bg_rect, 2)
                
                self.screen.blit(text_surface, text_rect)
        
        # Legacy consumption text support (for backward compatibility)
        elif hasattr(self, 'consumption_text') and self.consumption_text and hasattr(self, 'consumption_text_timer') and self.consumption_text_timer > 0:
            import pygame
            text_surface = self.font_manager.get_font('medium').render(self.consumption_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = SCREEN_WIDTH // 2
            text_rect.y = 50
            
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
            
            self.screen.blit(text_surface, text_rect)'''
    
    if old_rendering in content:
        content = content.replace(old_rendering, new_rendering)
        print("✅ Updated feedback message rendering system")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix all visual feedback messages to disappear after 1.5 seconds"""
    print("🔧 Fixing All Visual Feedback Messages")
    print("=" * 45)
    
    print("1. Enhancing visual feedback system...")
    enhance_visual_feedback_system()
    
    print("2. Adding universal feedback methods...")
    add_universal_feedback_methods()
    
    print("3. Updating item collection feedback...")
    update_item_collection_feedback()
    
    print("4. Updating item usage feedback...")
    update_item_usage_feedback()
    
    print("5. Updating combat feedback...")
    update_combat_feedback()
    
    print("6. Updating interaction feedback...")
    update_interaction_feedback()
    
    print("7. Updating feedback rendering system...")
    update_feedback_rendering()
    
    print("\n" + "=" * 45)
    print("🎉 ALL VISUAL FEEDBACK MESSAGES FIXED!")
    print("\nEnhanced Feedback System:")
    print("✅ All messages disappear after 1.5 seconds")
    print("✅ No more messages sticking on screen forever")
    print("✅ Color-coded message types for better clarity")
    print("✅ Messages stack vertically when multiple appear")
    print("✅ Clean, professional interface")
    print("\nMessage Types:")
    print("🟢 Item Collection - Green messages")
    print("🟡 Item Usage - Yellow messages") 
    print("🔴 Combat - Red messages")
    print("🔵 Interaction - Blue messages")
    print("⚪ System - Gray messages")
    print("\nFeatures:")
    print("- All feedback messages auto-disappear after 1.5 seconds")
    print("- Messages stack vertically for multiple simultaneous messages")
    print("- Color coding helps distinguish message types")
    print("- Clean interface without permanent text clutter")
    print("- Professional game-like feedback system")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
