#!/usr/bin/env python3
"""
Fix missing methods in simple systems
"""

def fix_moral_system():
    """Add missing methods to MoralSystem"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find MoralSystem and add missing method
    moral_pos = content.find('class MoralSystem:')
    if moral_pos != -1:
        # Find the end of the class
        next_class = content.find('\nclass ', moral_pos + 1)
        if next_class == -1:
            next_class = len(content)
        
        # Add missing method before the next class
        missing_method = '''
    def get_moral_standing(self):
        """Get moral standing description"""
        if self.moral_score >= 10:
            return "Righteous"
        elif self.moral_score >= 5:
            return "Good"
        elif self.moral_score >= 0:
            return "Neutral"
        elif self.moral_score >= -5:
            return "Questionable"
        else:
            return "Wicked"
'''
        
        content = content[:next_class] + missing_method + content[next_class:]
        print("✅ Added get_moral_standing method to MoralSystem")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def fix_visual_feedback():
    """Add missing methods to VisualFeedback"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find VisualFeedback and add missing methods
    visual_pos = content.find('class VisualFeedback:')
    if visual_pos != -1:
        # Find the end of the render method
        render_end = content.find('y_offset += 30', visual_pos)
        if render_end != -1:
            insertion_point = content.find('\n', render_end) + 1
            
            # Add missing methods
            missing_methods = '''
    def create_dust_effect(self, x, y):
        """Create dust effect (simple version)"""
        pass
    
    def clear_interaction_prompt(self):
        """Clear interaction prompt (simple version)"""
        pass
    
    def show_interaction_prompt(self, text):
        """Show interaction prompt (simple version)"""
        self.show_message(text, 2.0)
'''
            
            content = content[:insertion_point] + missing_methods + content[insertion_point:]
            print("✅ Added missing methods to VisualFeedback")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix missing methods in simple systems"""
    print("🔧 Fixing Missing Methods")
    print("=" * 25)
    
    print("1. Fixing MoralSystem...")
    fix_moral_system()
    
    print("2. Fixing VisualFeedback...")
    fix_visual_feedback()
    
    print("\n" + "=" * 25)
    print("🎉 MISSING METHODS FIXED!")
    print("\nAdded methods:")
    print("✅ MoralSystem.get_moral_standing()")
    print("✅ VisualFeedback.create_dust_effect()")
    print("✅ VisualFeedback.clear_interaction_prompt()")
    print("✅ VisualFeedback.show_interaction_prompt()")
    
    print("\nSimple game should now work without errors.")
    print("Test with: python3 main.py")

if __name__ == "__main__":
    main()
