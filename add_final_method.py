#!/usr/bin/env python3
"""
Add the final missing method to complete the simple version
"""

def add_moral_color_method():
    """Add get_moral_color method to MoralSystem"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find the get_moral_standing method and add get_moral_color after it
    standing_pos = content.find('return "Wicked"')
    if standing_pos != -1:
        insertion_point = content.find('\n', standing_pos) + 1
        
        moral_color_method = '''
    def get_moral_color(self):
        """Get color for moral standing display"""
        if self.moral_score >= 5:
            return (0, 255, 0)  # Green for good
        elif self.moral_score >= 0:
            return (255, 255, 255)  # White for neutral
        else:
            return (255, 0, 0)  # Red for bad
'''
        
        content = content[:insertion_point] + moral_color_method + content[insertion_point:]
        print("✅ Added get_moral_color method to MoralSystem")
    
    with open('game_systems.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Add the final method"""
    print("🔧 Adding Final Method")
    print("=" * 20)
    
    add_moral_color_method()
    
    print("\n" + "=" * 20)
    print("🎉 SIMPLE VERSION COMPLETE!")
    print("Ready to test: python3 main.py")

if __name__ == "__main__":
    main()
