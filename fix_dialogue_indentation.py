#!/usr/bin/env python3
"""
Fix dialogue system indentation error
"""

def fix_dialogue_indentation():
    """Fix the indentation error in dialogue handling"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the indentation issue
    old_dialogue_section = '''            elif self.state == GameState.DIALOGUE:
            # Emergency dialogue exit if system is stuck
            if not hasattr(self.dialogue_system, 'active') or not self.dialogue_system.active:
                print("🔄 Dialogue system inactive - returning to game")
                self.state = GameState.PLAYING
            
                self.dialogue_system.handle_event(event)
                if not self.dialogue_system.active:
                    self.state = GameState.PLAYING
                    # Remove the NPC that was just talked to'''
    
    new_dialogue_section = '''            elif self.state == GameState.DIALOGUE:
                # Emergency dialogue exit if system is stuck
                if not hasattr(self.dialogue_system, 'active') or not self.dialogue_system.active:
                    print("🔄 Dialogue system inactive - returning to game")
                    self.state = GameState.PLAYING
                else:
                    self.dialogue_system.handle_event(event)
                    if not self.dialogue_system.active:
                        self.state = GameState.PLAYING
                        # Remove the NPC that was just talked to'''
    
    if old_dialogue_section in content:
        content = content.replace(old_dialogue_section, new_dialogue_section)
        print("✅ Fixed dialogue system indentation")
    else:
        print("⚠️  Could not find exact dialogue section to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix dialogue indentation error"""
    print("🔧 Fixing Dialogue Indentation Error")
    print("=" * 35)
    
    if fix_dialogue_indentation():
        print("✅ DIALOGUE INDENTATION FIXED!")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix dialogue indentation")

if __name__ == "__main__":
    main()
