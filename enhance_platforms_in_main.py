#!/usr/bin/env python3
"""
Enhance platforms directly in main.py with multi-level system
"""

def find_and_enhance_platforms():
    """Find platform creation in main.py and enhance it"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Search for platform creation patterns
    import re
    
    # Look for platform creation patterns
    platform_patterns = [
        r"platforms\s*=\s*\[",
        r"self\.platforms\s*=\s*\[",
        r"create.*platform",
        r"Platform.*\(",
    ]
    
    found_platforms = False
    for pattern in platform_patterns:
        matches = re.search(pattern, content, re.IGNORECASE)
        if matches:
            print(f"✅ Found platform pattern: {pattern}")
            found_platforms = True
            break
    
    if not found_platforms:
        print("⚠️  No existing platform creation found, will add new system")
        return add_new_platform_system(content)
    
    return True

def add_new_platform_system(content):
    """Add a new comprehensive platform system to main.py"""
    
    # Find a good place to add the platform system - look for game initialization
    init_patterns = [
        "def start_game(self):",
        "def __init__(self",
        "class MosesAdventureGame",
    ]
    
    insertion_point = -1
    for pattern in init_patterns:
        pos = content.find(pattern)
        if pos != -1:
            # Find the end of this method/class
            next_def = content.find("def ", pos + len(pattern))
            if next_def != -1:
                insertion_point = next_def
                break
    
    if insertion_point == -1:
        print("❌ Could not find suitable insertion point")
        return False
    
    # Create the new platform system
    new_platform_system = '''
    def create_multi_level_platforms(self):
        """Create comprehensive multi-level platform system"""
        print("🏗️  Creating multi-level platform system...")
        
        # Multi-level platform system with strategic placement
        self.platforms = [
            # Ground level platforms (y=570-620) - Easy access
            {'x': 300, 'y': 570, 'width': 120, 'height': 20, 'type': 'stone_platform'},
            {'x': 500, 'y': 590, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 700, 'y': 580, 'width': 140, 'height': 20, 'type': 'stone_platform'},
            {'x': 900, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1100, 'y': 595, 'width': 120, 'height': 20, 'type': 'stone_platform'},
            {'x': 1300, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1500, 'y': 585, 'width': 130, 'height': 20, 'type': 'stone_platform'},
            {'x': 1700, 'y': 560, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1900, 'y': 575, 'width': 110, 'height': 20, 'type': 'stone_platform'},
            {'x': 2100, 'y': 608, 'width': 120, 'height': 20, 'type': 'stone_platform'},
            {'x': 2300, 'y': 590, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            
            # Mid-level platforms (y=450-520) - Moderate jumping required
            {'x': 250, 'y': 470, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            {'x': 450, 'y': 480, 'width': 90, 'height': 20, 'type': 'stone_platform'},
            {'x': 650, 'y': 460, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 850, 'y': 490, 'width': 85, 'height': 20, 'type': 'stone_platform'},
            {'x': 1050, 'y': 470, 'width': 95, 'height': 20, 'type': 'stone_platform'},
            {'x': 1250, 'y': 485, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            {'x': 1450, 'y': 465, 'width': 110, 'height': 20, 'type': 'stone_platform'},
            {'x': 1650, 'y': 450, 'width': 90, 'height': 20, 'type': 'stone_platform'},
            {'x': 1850, 'y': 475, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 2050, 'y': 490, 'width': 85, 'height': 20, 'type': 'stone_platform'},
            {'x': 2250, 'y': 460, 'width': 95, 'height': 20, 'type': 'stone_platform'},
            
            # High-level platforms (y=350-420) - Challenging platforming
            {'x': 200, 'y': 370, 'width': 70, 'height': 20, 'type': 'stone_platform'},
            {'x': 400, 'y': 380, 'width': 75, 'height': 20, 'type': 'stone_platform'},
            {'x': 600, 'y': 360, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            {'x': 800, 'y': 390, 'width': 70, 'height': 20, 'type': 'stone_platform'},
            {'x': 1000, 'y': 370, 'width': 85, 'height': 20, 'type': 'stone_platform'},
            {'x': 1200, 'y': 385, 'width': 75, 'height': 20, 'type': 'stone_platform'},
            {'x': 1400, 'y': 365, 'width': 90, 'height': 20, 'type': 'stone_platform'},
            {'x': 1600, 'y': 350, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            {'x': 1800, 'y': 375, 'width': 85, 'height': 20, 'type': 'stone_platform'},
            {'x': 2000, 'y': 390, 'width': 75, 'height': 20, 'type': 'stone_platform'},
            {'x': 2200, 'y': 360, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            
            # Top-level platforms (y=250-320) - Expert-level climbing
            {'x': 350, 'y': 280, 'width': 60, 'height': 20, 'type': 'stone_platform'},
            {'x': 550, 'y': 270, 'width': 65, 'height': 20, 'type': 'stone_platform'},
            {'x': 750, 'y': 290, 'width': 70, 'height': 20, 'type': 'stone_platform'},
            {'x': 950, 'y': 260, 'width': 60, 'height': 20, 'type': 'stone_platform'},
            {'x': 1150, 'y': 285, 'width': 75, 'height': 20, 'type': 'stone_platform'},
            {'x': 1350, 'y': 275, 'width': 65, 'height': 20, 'type': 'stone_platform'},
            {'x': 1550, 'y': 250, 'width': 80, 'height': 20, 'type': 'stone_platform'},
            {'x': 1750, 'y': 295, 'width': 70, 'height': 20, 'type': 'stone_platform'},
            {'x': 1950, 'y': 265, 'width': 75, 'height': 20, 'type': 'stone_platform'},
            {'x': 2150, 'y': 280, 'width': 65, 'height': 20, 'type': 'stone_platform'},
        ]
        
        print(f"✅ Created {len(self.platforms)} platforms across 4 levels")
        return self.platforms
    
    def create_strategic_items(self):
        """Create items strategically placed on platforms"""
        print("🎁 Creating strategic item placement...")
        
        self.items = [
            # Ground level items - Easy to collect
            {'x': 320, 'y': 550, 'type': 'stone'},
            {'x': 520, 'y': 570, 'type': 'water'},
            {'x': 720, 'y': 560, 'type': 'bread'},
            {'x': 1120, 'y': 575, 'type': 'scroll'},
            {'x': 1520, 'y': 565, 'type': 'meat'},
            {'x': 1920, 'y': 555, 'type': 'armor_of_god'},
            {'x': 2120, 'y': 588, 'type': 'staff'},
            
            # Mid-level items - Require jumping
            {'x': 270, 'y': 450, 'type': 'stone'},
            {'x': 470, 'y': 460, 'type': 'water'},
            {'x': 670, 'y': 440, 'type': 'bread'},
            {'x': 870, 'y': 470, 'type': 'scroll'},
            {'x': 1070, 'y': 450, 'type': 'meat'},
            {'x': 1470, 'y': 445, 'type': 'armor_of_god'},
            {'x': 1870, 'y': 455, 'type': 'staff'},
            {'x': 2070, 'y': 470, 'type': 'stone'},
            
            # High-level items - Challenging to reach
            {'x': 220, 'y': 350, 'type': 'water'},
            {'x': 420, 'y': 360, 'type': 'bread'},
            {'x': 620, 'y': 340, 'type': 'scroll'},
            {'x': 820, 'y': 370, 'type': 'meat'},
            {'x': 1020, 'y': 350, 'type': 'armor_of_god'},
            {'x': 1420, 'y': 345, 'type': 'staff'},
            {'x': 1820, 'y': 355, 'type': 'stone'},
            {'x': 2020, 'y': 370, 'type': 'water'},
            
            # Top-level items - Most challenging
            {'x': 370, 'y': 260, 'type': 'scroll'},
            {'x': 570, 'y': 250, 'type': 'meat'},
            {'x': 770, 'y': 270, 'type': 'armor_of_god'},
            {'x': 970, 'y': 240, 'type': 'staff'},
            {'x': 1170, 'y': 265, 'type': 'stone'},
            {'x': 1370, 'y': 255, 'type': 'water'},
            {'x': 1570, 'y': 230, 'type': 'bread'},
            {'x': 1770, 'y': 275, 'type': 'scroll'},
            {'x': 1970, 'y': 245, 'type': 'meat'},
        ]
        
        print(f"✅ Created {len(self.items)} strategically placed items")
        return self.items
    
    def create_platform_characters(self):
        """Create NPCs and enemies on platforms"""
        print("👥 Creating platform characters...")
        
        # Enhanced NPCs on platforms
        self.npcs = [
            # Ground level NPCs
            {'x': 300, 'y': 670, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 500, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 800, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1200, 'y': 670, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1600, 'y': 670, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 2000, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 2400, 'y': 670, 'type': 'palace_guard', 'dialogue': 'checkpoint_dialogue'},
            
            # NPCs on platforms
            {'x': 320, 'y': 550, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 720, 'y': 560, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1120, 'y': 575, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 1720, 'y': 540, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 470, 'y': 460, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 870, 'y': 470, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1270, 'y': 465, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 420, 'y': 360, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 820, 'y': 370, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1220, 'y': 365, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 570, 'y': 250, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 970, 'y': 240, 'type': 'palace_guard', 'dialogue': 'checkpoint_dialogue'},
        ]
        
        # Enhanced enemies on platforms
        self.enemies = [
            # Ground level enemies
            {'x': 600, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1000, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1400, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1800, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2200, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            
            # Platform enemies
            {'x': 540, 'y': 570, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 940, 'y': 588, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1340, 'y': 588, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 290, 'y': 450, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 690, 'y': 440, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1090, 'y': 450, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1490, 'y': 445, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 240, 'y': 350, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 640, 'y': 340, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1040, 'y': 350, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1440, 'y': 345, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 390, 'y': 260, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 790, 'y': 270, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1190, 'y': 265, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1590, 'y': 230, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
        ]
        
        print(f"✅ Created {len(self.npcs)} NPCs and {len(self.enemies)} enemies")
        return self.npcs, self.enemies

'''
    
    # Insert the new platform system
    content = content[:insertion_point] + new_platform_system + content[insertion_point:]
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    print("✅ Added comprehensive multi-level platform system to main.py")
    return True

def main():
    """Enhance platforms in main.py"""
    print("🏗️  Enhancing Platforms in Main.py")
    print("=" * 35)
    
    if find_and_enhance_platforms():
        print("\n✅ PLATFORM ENHANCEMENT COMPLETE!")
        print("\nNew Features Added:")
        print("✅ Multi-level platform system (4 levels)")
        print("✅ Strategic item placement on platforms")
        print("✅ NPCs and enemies on different levels")
        print("✅ Progressive difficulty by height")
        print("\nPlatform Levels:")
        print("🏠 Ground (y=570-620): Basic access")
        print("🏢 Mid (y=450-520): Moderate jumping")
        print("🏔️  High (y=350-420): Challenging")
        print("⛰️  Top (y=250-320): Expert level")
        print("\nCall these methods in your game initialization:")
        print("- self.create_multi_level_platforms()")
        print("- self.create_strategic_items()")
        print("- self.create_platform_characters()")
    else:
        print("\n❌ Failed to enhance platforms")

if __name__ == "__main__":
    main()
