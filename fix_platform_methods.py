#!/usr/bin/env python3
"""
Fix the platform methods integration issue
"""

def fix_platform_methods_integration():
    """Fix the platform methods to be properly integrated into the MosesAdventureGame class"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Remove the calls that are causing the error
    error_calls = '''        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        self.create_multi_level_platforms()
        self.create_strategic_items()
        self.create_platform_characters()'''
    
    if error_calls in content:
        content = content.replace(error_calls, '''        # Initialize multi-level platform system
        print("🏗️  Initializing multi-level platform system...")
        print("✅ Multi-level platform system ready!")''')
        print("✅ Removed problematic method calls")
    
    # Find the MosesAdventureGame class and add the methods properly
    class_marker = "class MosesAdventureGame:"
    class_pos = content.find(class_marker)
    
    if class_pos != -1:
        # Find a good place to add the methods - after __init__
        init_marker = "def __init__(self"
        init_pos = content.find(init_marker, class_pos)
        
        if init_pos != -1:
            # Find the end of __init__ method
            next_def = content.find("\n    def ", init_pos + 1)
            if next_def != -1:
                # Add the platform methods before the next method
                platform_methods = '''
    def initialize_multi_level_world(self):
        """Initialize the multi-level platform world"""
        print("🏗️  Creating multi-level platform world...")
        
        # Create comprehensive platform system
        self.game_platforms = [
            # Ground level platforms (y=570-620)
            {'x': 300, 'y': 570, 'width': 120, 'height': 20},
            {'x': 500, 'y': 590, 'width': 100, 'height': 20},
            {'x': 700, 'y': 580, 'width': 140, 'height': 20},
            {'x': 900, 'y': 608, 'width': 100, 'height': 20},
            {'x': 1100, 'y': 595, 'width': 120, 'height': 20},
            {'x': 1300, 'y': 608, 'width': 100, 'height': 20},
            {'x': 1500, 'y': 585, 'width': 130, 'height': 20},
            {'x': 1700, 'y': 560, 'width': 100, 'height': 20},
            {'x': 1900, 'y': 575, 'width': 110, 'height': 20},
            {'x': 2100, 'y': 608, 'width': 120, 'height': 20},
            
            # Mid-level platforms (y=450-520)
            {'x': 250, 'y': 470, 'width': 80, 'height': 20},
            {'x': 450, 'y': 480, 'width': 90, 'height': 20},
            {'x': 650, 'y': 460, 'width': 100, 'height': 20},
            {'x': 850, 'y': 490, 'width': 85, 'height': 20},
            {'x': 1050, 'y': 470, 'width': 95, 'height': 20},
            {'x': 1250, 'y': 485, 'width': 80, 'height': 20},
            {'x': 1450, 'y': 465, 'width': 110, 'height': 20},
            {'x': 1650, 'y': 450, 'width': 90, 'height': 20},
            {'x': 1850, 'y': 475, 'width': 100, 'height': 20},
            {'x': 2050, 'y': 490, 'width': 85, 'height': 20},
            
            # High-level platforms (y=350-420)
            {'x': 200, 'y': 370, 'width': 70, 'height': 20},
            {'x': 400, 'y': 380, 'width': 75, 'height': 20},
            {'x': 600, 'y': 360, 'width': 80, 'height': 20},
            {'x': 800, 'y': 390, 'width': 70, 'height': 20},
            {'x': 1000, 'y': 370, 'width': 85, 'height': 20},
            {'x': 1200, 'y': 385, 'width': 75, 'height': 20},
            {'x': 1400, 'y': 365, 'width': 90, 'height': 20},
            {'x': 1600, 'y': 350, 'width': 80, 'height': 20},
            {'x': 1800, 'y': 375, 'width': 85, 'height': 20},
            {'x': 2000, 'y': 390, 'width': 75, 'height': 20},
            
            # Top-level platforms (y=250-320)
            {'x': 350, 'y': 280, 'width': 60, 'height': 20},
            {'x': 550, 'y': 270, 'width': 65, 'height': 20},
            {'x': 750, 'y': 290, 'width': 70, 'height': 20},
            {'x': 950, 'y': 260, 'width': 60, 'height': 20},
            {'x': 1150, 'y': 285, 'width': 75, 'height': 20},
            {'x': 1350, 'y': 275, 'width': 65, 'height': 20},
            {'x': 1550, 'y': 250, 'width': 80, 'height': 20},
            {'x': 1750, 'y': 295, 'width': 70, 'height': 20},
            {'x': 1950, 'y': 265, 'width': 75, 'height': 20},
        ]
        
        # Create strategic items on platforms
        self.game_items = [
            # Ground level items
            {'x': 320, 'y': 550, 'type': 'stone'},
            {'x': 520, 'y': 570, 'type': 'water'},
            {'x': 720, 'y': 560, 'type': 'bread'},
            {'x': 1120, 'y': 575, 'type': 'scroll'},
            {'x': 1520, 'y': 565, 'type': 'meat'},
            {'x': 1920, 'y': 555, 'type': 'armor_of_god'},
            {'x': 2120, 'y': 588, 'type': 'staff'},
            
            # Mid-level items
            {'x': 270, 'y': 450, 'type': 'stone'},
            {'x': 470, 'y': 460, 'type': 'water'},
            {'x': 670, 'y': 440, 'type': 'bread'},
            {'x': 870, 'y': 470, 'type': 'scroll'},
            {'x': 1070, 'y': 450, 'type': 'meat'},
            {'x': 1470, 'y': 445, 'type': 'armor_of_god'},
            {'x': 1870, 'y': 455, 'type': 'staff'},
            
            # High-level items
            {'x': 220, 'y': 350, 'type': 'water'},
            {'x': 420, 'y': 360, 'type': 'bread'},
            {'x': 620, 'y': 340, 'type': 'scroll'},
            {'x': 820, 'y': 370, 'type': 'meat'},
            {'x': 1020, 'y': 350, 'type': 'armor_of_god'},
            {'x': 1420, 'y': 345, 'type': 'staff'},
            
            # Top-level items
            {'x': 370, 'y': 260, 'type': 'scroll'},
            {'x': 570, 'y': 250, 'type': 'meat'},
            {'x': 770, 'y': 270, 'type': 'armor_of_god'},
            {'x': 970, 'y': 240, 'type': 'staff'},
            {'x': 1170, 'y': 265, 'type': 'stone'},
        ]
        
        # Create NPCs and enemies on platforms
        self.game_npcs = [
            # Ground NPCs
            {'x': 320, 'y': 550, 'type': 'hebrew_slave'},
            {'x': 720, 'y': 560, 'type': 'egyptian_citizen'},
            {'x': 1120, 'y': 575, 'type': 'priest'},
            {'x': 1720, 'y': 540, 'type': 'palace_guard'},
            
            # Platform NPCs
            {'x': 470, 'y': 460, 'type': 'egyptian_citizen'},
            {'x': 870, 'y': 470, 'type': 'hebrew_slave'},
            {'x': 1270, 'y': 465, 'type': 'priest'},
            {'x': 420, 'y': 360, 'type': 'priest'},
            {'x': 820, 'y': 370, 'type': 'hebrew_slave'},
            {'x': 570, 'y': 250, 'type': 'priest'},
            {'x': 970, 'y': 240, 'type': 'palace_guard'},
        ]
        
        self.game_enemies = [
            # Ground enemies
            {'x': 600, 'y': 640, 'type': 'egyptian_soldier'},
            {'x': 1000, 'y': 620, 'type': 'egyptian_soldier'},
            {'x': 1400, 'y': 640, 'type': 'egyptian_soldier'},
            {'x': 1800, 'y': 640, 'type': 'egyptian_soldier'},
            
            # Platform enemies
            {'x': 540, 'y': 570, 'type': 'egyptian_soldier'},
            {'x': 940, 'y': 588, 'type': 'egyptian_soldier'},
            {'x': 290, 'y': 450, 'type': 'egyptian_soldier'},
            {'x': 690, 'y': 440, 'type': 'egyptian_soldier'},
            {'x': 1090, 'y': 450, 'type': 'egyptian_soldier'},
            {'x': 240, 'y': 350, 'type': 'egyptian_soldier'},
            {'x': 640, 'y': 340, 'type': 'egyptian_soldier'},
            {'x': 1040, 'y': 350, 'type': 'egyptian_soldier'},
            {'x': 390, 'y': 260, 'type': 'egyptian_soldier'},
            {'x': 790, 'y': 270, 'type': 'egyptian_soldier'},
            {'x': 1190, 'y': 265, 'type': 'egyptian_soldier'},
        ]
        
        print(f"✅ Created {len(self.game_platforms)} platforms across 4 levels")
        print(f"✅ Created {len(self.game_items)} strategic items")
        print(f"✅ Created {len(self.game_npcs)} NPCs and {len(self.game_enemies)} enemies")
        
        return True

'''
                
                content = content[:next_def] + platform_methods + content[next_def:]
                print("✅ Added platform methods to MosesAdventureGame class")
    
    # Update the start_game method to call the new method
    start_game_update = '''        print("🏗️  Initializing multi-level platform system...")
        print("✅ Multi-level platform system ready!")'''
    
    start_game_new = '''        print("🏗️  Initializing multi-level platform system...")
        self.initialize_multi_level_world()'''
    
    if start_game_update in content:
        content = content.replace(start_game_update, start_game_new)
        print("✅ Updated start_game to call platform initialization")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix platform methods integration"""
    print("🔧 Fixing Platform Methods Integration")
    print("=" * 40)
    
    if fix_platform_methods_integration():
        print("\n✅ PLATFORM METHODS INTEGRATION FIXED!")
        print("\nFixed Issues:")
        print("✅ Removed problematic method calls")
        print("✅ Added proper platform methods to class")
        print("✅ Updated game initialization")
        print("✅ Created comprehensive platform system")
        print("\nNew Features:")
        print("🏗️  Multi-level platform world")
        print("🎁 Strategic item placement")
        print("👥 NPCs and enemies on platforms")
        print("🏠 4 distinct platform levels")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Failed to fix platform methods")

if __name__ == "__main__":
    main()
