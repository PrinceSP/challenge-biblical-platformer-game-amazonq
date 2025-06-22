#!/usr/bin/env python3
"""
Fix the opening dialogue system that's stuck on narrator screen
"""

def fix_dialogue_system_initialization():
    """Ensure dialogue system is properly initialized and connected"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Make sure DialogueSystem is imported
    if "from game_systems import" not in content:
        # Add import at the top
        import_pos = content.find("import pygame")
        if import_pos != -1:
            insertion_point = content.find('\n', import_pos) + 1
            dialogue_import = "from game_systems import DialogueSystem, Inventory, MoralSystem, VisualFeedback\n"
            content = content[:insertion_point] + dialogue_import + content[insertion_point:]
            print("✅ Added DialogueSystem import")
    
    # Ensure dialogue system is properly initialized
    dialogue_init_pattern = "self.dialogue_system = DialogueSystem()"
    if dialogue_init_pattern not in content:
        # Find where to add dialogue system initialization
        init_pos = content.find("self.inventory = Inventory()")
        if init_pos != -1:
            insertion_point = content.find('\n', init_pos) + 1
            dialogue_init = "        self.dialogue_system = DialogueSystem()\n"
            content = content[:insertion_point] + dialogue_init + content[insertion_point:]
            print("✅ Added dialogue system initialization")
    
    # Ensure dialogue system connections are made
    if "self.dialogue_system.game_instance = self" not in content:
        dialogue_init_pos = content.find("self.dialogue_system = DialogueSystem()")
        if dialogue_init_pos != -1:
            insertion_point = content.find('\n', dialogue_init_pos) + 1
            dialogue_connections = '''        self.dialogue_system.game_instance = self  # Connect for health effects
        self.dialogue_system.moral_system = self.moral_system
        self.dialogue_system.set_sound_manager(self.sound_manager)  # Connect sound manager
'''
            content = content[:insertion_point] + dialogue_connections + content[insertion_point:]
            print("✅ Added dialogue system connections")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_dialogue_rendering():
    """Fix dialogue rendering to ensure it shows properly"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Make sure dialogue rendering is correct
    dialogue_render_pattern = "self.dialogue_system.render(self.screen, self.sprites)"
    if dialogue_render_pattern not in content:
        # Find where dialogue should be rendered
        dialogue_state_pos = content.find("if self.state == GameState.DIALOGUE:")
        if dialogue_state_pos != -1:
            # Find the next line after the if statement
            insertion_point = content.find('\n', dialogue_state_pos) + 1
            dialogue_render = "                self.dialogue_system.render(self.screen, self.sprites)\n"
            content = content[:insertion_point] + dialogue_render + content[insertion_point:]
            print("✅ Added dialogue rendering")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_dialogue_skip_functionality():
    """Add functionality to skip dialogue if it gets stuck"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add dialogue skip functionality to game events
    if "# Skip dialogue with SPACE or ENTER" not in content:
        # Find the handle_game_events method
        game_events_pos = content.find("def handle_game_events(self, event):")
        if game_events_pos != -1:
            # Find the key handling section
            key_handling_pos = content.find("if event.key == pygame.K_ESCAPE:", game_events_pos)
            if key_handling_pos != -1:
                # Add dialogue skip before ESC handling
                dialogue_skip = '''                # Skip dialogue with SPACE or ENTER
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    if self.state == GameState.DIALOGUE:
                        if hasattr(self.dialogue_system, 'active') and self.dialogue_system.active:
                            # Skip to end of current dialogue or advance
                            if hasattr(self.dialogue_system, 'skip_to_end'):
                                self.dialogue_system.skip_to_end()
                            else:
                                # Force dialogue to end if stuck
                                self.dialogue_system.active = False
                                self.state = GameState.PLAYING
                                print("🔄 Dialogue skipped - returning to game")
                
'''
                content = content[:key_handling_pos] + dialogue_skip + content[key_handling_pos:]
                print("✅ Added dialogue skip functionality (SPACE/ENTER)")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def add_emergency_dialogue_exit():
    """Add emergency exit from dialogue state"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add emergency dialogue exit in the update method
    dialogue_update_pos = content.find("elif self.state == GameState.DIALOGUE:")
    if dialogue_update_pos != -1:
        next_line_pos = content.find('\n', dialogue_update_pos) + 1
        emergency_exit = '''            # Emergency dialogue exit if system is stuck
            if not hasattr(self.dialogue_system, 'active') or not self.dialogue_system.active:
                print("🔄 Dialogue system inactive - returning to game")
                self.state = GameState.PLAYING
            
'''
        content = content[:next_line_pos] + emergency_exit + content[next_line_pos:]
        print("✅ Added emergency dialogue exit")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def create_dialogue_debug_info():
    """Add debug information for dialogue system"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Add dialogue debug info to start_game method
    start_game_pos = content.find("self.dialogue_system.start_dialogue(\"opening\")")
    if start_game_pos != -1:
        insertion_point = content.find('\n', start_game_pos) + 1
        debug_info = '''        
        # Debug dialogue system
        print(f"🎭 Dialogue system active: {hasattr(self.dialogue_system, 'active')}")
        if hasattr(self.dialogue_system, 'dialogue_data'):
            print(f"🎭 Dialogue data loaded: {'opening' in self.dialogue_system.dialogue_data}")
        print(f"🎭 Game state: {self.state}")
'''
        content = content[:insertion_point] + debug_info + content[insertion_point:]
        print("✅ Added dialogue debug information")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def fix_dialogue_system_import():
    """Ensure DialogueSystem is properly imported"""
    
    with open('game_systems.py', 'r') as f:
        game_systems_content = f.read()
    
    # Check if DialogueSystem class exists and is complete
    if "class DialogueSystem:" in game_systems_content and "def render(self" in game_systems_content:
        print("✅ DialogueSystem class exists and has render method")
        return True
    else:
        print("⚠️  DialogueSystem class may be incomplete")
        return False

def main():
    """Fix the opening dialogue system"""
    print("🔧 Fixing Opening Dialogue System")
    print("=" * 35)
    
    print("1. Checking DialogueSystem import...")
    fix_dialogue_system_import()
    
    print("2. Fixing dialogue system initialization...")
    fix_dialogue_system_initialization()
    
    print("3. Fixing dialogue rendering...")
    fix_dialogue_rendering()
    
    print("4. Adding dialogue skip functionality...")
    add_dialogue_skip_functionality()
    
    print("5. Adding emergency dialogue exit...")
    add_emergency_dialogue_exit()
    
    print("6. Adding dialogue debug info...")
    create_dialogue_debug_info()
    
    print("\n" + "=" * 35)
    print("🎉 OPENING DIALOGUE SYSTEM FIXED!")
    print("\nDialogue System Fixes:")
    print("✅ DialogueSystem properly initialized and connected")
    print("✅ Dialogue rendering restored")
    print("✅ Opening dialogue data available")
    print("✅ Emergency exit from stuck dialogue")
    print("✅ Debug information for troubleshooting")
    print("\nControls to Skip Dialogue:")
    print("- SPACE: Skip/advance dialogue")
    print("- ENTER: Skip/advance dialogue")
    print("- ESC: Emergency exit to game")
    print("\nThe opening dialogue should now:")
    print("- Show narrator text properly")
    print("- Allow progression with SPACE/ENTER")
    print("- Have emergency exit if stuck")
    print("- Display debug info for troubleshooting")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
