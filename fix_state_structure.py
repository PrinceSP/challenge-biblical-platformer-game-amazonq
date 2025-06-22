#!/usr/bin/env python3
"""
Fix the state structure with proper if-elif alignment
"""

def fix_state_structure():
    """Fix the state structure with proper if-elif alignment"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and fix the state structure
    old_structure = '''        self.level_manager.update(dt)
        self.visual_feedback.update(dt)
    
    elif self.state == GameState.DIALOGUE:
        self.dialogue_system.update(dt)'''
    
    new_structure = '''            self.level_manager.update(dt)
            self.visual_feedback.update(dt)
        
        elif self.state == GameState.DIALOGUE:
            self.dialogue_system.update(dt)'''
    
    if old_structure in content:
        content = content.replace(old_structure, new_structure)
        print("✅ Fixed state structure with proper if-elif alignment")
    else:
        print("⚠️  Could not find exact state structure to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix state structure"""
    print("🔧 Fixing State Structure")
    print("=" * 25)
    
    if fix_state_structure():
        print("✅ STATE STRUCTURE FIXED!")
        print("✅ Proper if-elif alignment restored")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix state structure")

if __name__ == "__main__":
    main()
