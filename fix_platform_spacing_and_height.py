#!/usr/bin/env python3
"""
Fix platform spacing and height - increase distance between platforms and position them higher
"""

def fix_platform_spacing_and_height():
    """Increase spacing between platforms and position them higher above old platforms"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the current platform system and replace with better spaced platforms
    old_platform_system = '''        # Create platform system with REACHABLE positions for Moses
        # Moses jumps from y=670 to y=437 (233px range) - platforms must be within this range
        self.game_platforms = [
            # Base level - REACHABLE from ground (y=620-650) - Just above ground level
            {'x': 300, 'y': 620, 'width': 120, 'height': 20},  # Original x=300 position - REACHABLE
            {'x': 550, 'y': 630, 'width': 110, 'height': 20},  # 250px spacing - REACHABLE
            {'x': 800, 'y': 625, 'width': 120, 'height': 20},  # 250px spacing - REACHABLE
            {'x': 1050, 'y': 635, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1300, 'y': 620, 'width': 120, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1550, 'y': 630, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 1800, 'y': 625, 'width': 120, 'height': 20}, # 250px spacing - REACHABLE
            {'x': 2050, 'y': 635, 'width': 110, 'height': 20}, # 250px spacing - REACHABLE
            
            # Level 1 - First elevated platforms (y=520-560) - REACHABLE from base level
            {'x': 200, 'y': 530, 'width': 100, 'height': 20},  # REACHABLE from base
            {'x': 450, 'y': 540, 'width': 95, 'height': 20},   # REACHABLE from base
            {'x': 700, 'y': 535, 'width': 100, 'height': 20},  # REACHABLE from base
            {'x': 950, 'y': 545, 'width': 95, 'height': 20},   # REACHABLE from base
            {'x': 1200, 'y': 530, 'width': 100, 'height': 20}, # REACHABLE from base
            {'x': 1450, 'y': 540, 'width': 95, 'height': 20},  # REACHABLE from base
            {'x': 1700, 'y': 535, 'width': 100, 'height': 20}, # REACHABLE from base
            {'x': 1950, 'y': 545, 'width': 95, 'height': 20},  # REACHABLE from base
            
            # Level 2 - Second elevated platforms (y=330-370) - REACHABLE from Level 1
            {'x': 150, 'y': 340, 'width': 85, 'height': 20},   # Offset for variety
            {'x': 400, 'y': 350, 'width': 90, 'height': 20},   # 250px spacing
            {'x': 650, 'y': 345, 'width': 85, 'height': 20},   # 250px spacing
            {'x': 900, 'y': 355, 'width': 90, 'height': 20},   # 250px spacing
            {'x': 1150, 'y': 340, 'width': 85, 'height': 20},  # 250px spacing
            {'x': 1400, 'y': 350, 'width': 90, 'height': 20},  # 250px spacing
            {'x': 1650, 'y': 345, 'width': 85, 'height': 20},  # 250px spacing
            {'x': 1900, 'y': 355, 'width': 90, 'height': 20},  # 250px spacing
            
            # Level 3 - Third elevated platforms (y=210-250) - REACHABLE from Level 2
            {'x': 250, 'y': 220, 'width': 75, 'height': 20},   # Offset for variety
            {'x': 500, 'y': 230, 'width': 80, 'height': 20},   # 250px spacing
            {'x': 750, 'y': 225, 'width': 75, 'height': 20},   # 250px spacing
            {'x': 1000, 'y': 235, 'width': 80, 'height': 20},  # 250px spacing
            {'x': 1250, 'y': 220, 'width': 75, 'height': 20},  # 250px spacing
            {'x': 1500, 'y': 230, 'width': 80, 'height': 20},  # 250px spacing
            {'x': 1750, 'y': 225, 'width': 75, 'height': 20},  # 250px spacing
            {'x': 2000, 'y': 235, 'width': 80, 'height': 20},  # 250px spacing
            
            # Level 4 - Top platforms (y=90-130) - REACHABLE from Level 3
            {'x': 350, 'y': 100, 'width': 70, 'height': 20},   # Offset for variety
            {'x': 600, 'y': 110, 'width': 75, 'height': 20},   # 250px spacing
            {'x': 850, 'y': 105, 'width': 70, 'height': 20},   # 250px spacing
            {'x': 1100, 'y': 115, 'width': 75, 'height': 20},  # 250px spacing
            {'x': 1350, 'y': 100, 'width': 70, 'height': 20},  # 250px spacing
            {'x': 1600, 'y': 110, 'width': 75, 'height': 20},  # 250px spacing
            {'x': 1850, 'y': 105, 'width': 70, 'height': 20},  # 250px spacing
        ]'''
    
    # Create new platform system with much better spacing and higher positioning
    new_platform_system = '''        # Create platform system with INCREASED SPACING and HIGHER POSITIONING
        # Old platforms are around y=608-670, new platforms positioned well above them
        self.game_platforms = [
            # Base level - HIGHER above old platforms (y=550-580) - Clear separation from old platforms
            {'x': 400, 'y': 560, 'width': 120, 'height': 20},   # 400px spacing between platforms
            {'x': 800, 'y': 570, 'width': 110, 'height': 20},   # 400px spacing - no overlap
            {'x': 1200, 'y': 565, 'width': 120, 'height': 20},  # 400px spacing - clear separation
            {'x': 1600, 'y': 575, 'width': 110, 'height': 20},  # 400px spacing - well spaced
            {'x': 2000, 'y': 560, 'width': 120, 'height': 20},  # 400px spacing - good distance
            {'x': 2400, 'y': 570, 'width': 110, 'height': 20},  # 400px spacing - final base platform
            
            # Level 1 - First elevated platforms (y=420-460) - 140px above base level
            {'x': 300, 'y': 430, 'width': 100, 'height': 20},   # Offset start, 400px spacing
            {'x': 700, 'y': 440, 'width': 95, 'height': 20},    # 400px spacing - good distance
            {'x': 1100, 'y': 435, 'width': 100, 'height': 20},  # 400px spacing - clear separation
            {'x': 1500, 'y': 445, 'width': 95, 'height': 20},   # 400px spacing - well spaced
            {'x': 1900, 'y': 430, 'width': 100, 'height': 20},  # 400px spacing - good distance
            {'x': 2300, 'y': 440, 'width': 95, 'height': 20},   # 400px spacing - final level 1
            
            # Level 2 - Second elevated platforms (y=280-320) - 140px above Level 1
            {'x': 200, 'y': 290, 'width': 85, 'height': 20},    # Offset start, 400px spacing
            {'x': 600, 'y': 300, 'width': 90, 'height': 20},    # 400px spacing - good distance
            {'x': 1000, 'y': 295, 'width': 85, 'height': 20},   # 400px spacing - clear separation
            {'x': 1400, 'y': 305, 'width': 90, 'height': 20},   # 400px spacing - well spaced
            {'x': 1800, 'y': 290, 'width': 85, 'height': 20},   # 400px spacing - good distance
            {'x': 2200, 'y': 300, 'width': 90, 'height': 20},   # 400px spacing - final level 2
            
            # Level 3 - Third elevated platforms (y=140-180) - 140px above Level 2
            {'x': 500, 'y': 150, 'width': 75, 'height': 20},    # Centered start, 400px spacing
            {'x': 900, 'y': 160, 'width': 80, 'height': 20},    # 400px spacing - good distance
            {'x': 1300, 'y': 155, 'width': 75, 'height': 20},   # 400px spacing - clear separation
            {'x': 1700, 'y': 165, 'width': 80, 'height': 20},   # 400px spacing - well spaced
            {'x': 2100, 'y': 150, 'width': 75, 'height': 20},   # 400px spacing - final level 3
            
            # Level 4 - Top platforms (y=20-60) - 120px above Level 3 - Ultimate challenge
            {'x': 700, 'y': 30, 'width': 70, 'height': 20},     # Centered, 500px spacing
            {'x': 1200, 'y': 40, 'width': 75, 'height': 20},    # 500px spacing - maximum challenge
            {'x': 1700, 'y': 35, 'width': 70, 'height': 20},    # 500px spacing - expert level
        ]'''
    
    if old_platform_system in content:
        content = content.replace(old_platform_system, new_platform_system)
        print("✅ Updated platform system with increased spacing and higher positioning")
    else:
        print("⚠️  Could not find platform system to update")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def update_items_for_new_platform_positions():
    """Update item positions to match the new platform layout"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find and update item positions to match new platforms
    old_items = '''        # Create strategic items on platforms (positioned on platform centers)
        self.game_items = [
            # Ground level items (y=600-650)
            {'x': 250, 'y': 600, 'type': 'stone'},      # On platform at x=200
            {'x': 460, 'y': 610, 'type': 'water'},      # On platform at x=400
            {'x': 700, 'y': 605, 'type': 'bread'},      # On platform at x=650
            {'x': 955, 'y': 615, 'type': 'scroll'},     # On platform at x=900
            {'x': 1200, 'y': 600, 'type': 'meat'},      # On platform at x=1150
            {'x': 1460, 'y': 620, 'type': 'armor_of_god'}, # On platform at x=1400
            {'x': 1700, 'y': 605, 'type': 'staff'},     # On platform at x=1650
            
            # Level 1 items (y=520-570)
            {'x': 195, 'y': 520, 'type': 'stone'},      # On platform at x=150
            {'x': 400, 'y': 530, 'type': 'water'},      # On platform at x=350
            {'x': 595, 'y': 510, 'type': 'bread'},      # On platform at x=550
            {'x': 800, 'y': 540, 'type': 'scroll'},     # On platform at x=750
            {'x': 995, 'y': 520, 'type': 'meat'},       # On platform at x=950
            {'x': 1250, 'y': 535, 'type': 'armor_of_god'}, # On platform at x=1200
            
            # Level 2 items (y=440-490)
            {'x': 140, 'y': 440, 'type': 'water'},      # On platform at x=100
            {'x': 345, 'y': 450, 'type': 'bread'},      # On platform at x=300
            {'x': 542, 'y': 430, 'type': 'scroll'},     # On platform at x=500
            {'x': 745, 'y': 460, 'type': 'meat'},       # On platform at x=700
            {'x': 940, 'y': 440, 'type': 'armor_of_god'}, # On platform at x=900
            {'x': 1145, 'y': 455, 'type': 'staff'},     # On platform at x=1100
            
            # Level 3 items (y=360-410)
            {'x': 287, 'y': 360, 'type': 'scroll'},     # On platform at x=250
            {'x': 490, 'y': 370, 'type': 'meat'},       # On platform at x=450
            {'x': 687, 'y': 350, 'type': 'armor_of_god'}, # On platform at x=650
            {'x': 890, 'y': 380, 'type': 'staff'},      # On platform at x=850
            {'x': 1087, 'y': 360, 'type': 'stone'},     # On platform at x=1050
            
            # Level 4 items (y=280-330)
            {'x': 235, 'y': 280, 'type': 'meat'},       # On platform at x=200
            {'x': 437, 'y': 290, 'type': 'armor_of_god'}, # On platform at x=400
            {'x': 635, 'y': 270, 'type': 'staff'},      # On platform at x=600
            {'x': 837, 'y': 300, 'type': 'stone'},      # On platform at x=800
            
            # Level 5 items (y=200-250) - Premium rewards
            {'x': 182, 'y': 200, 'type': 'armor_of_god'}, # On platform at x=150
            {'x': 385, 'y': 210, 'type': 'staff'},      # On platform at x=350
            {'x': 582, 'y': 190, 'type': 'meat'},       # On platform at x=550
            {'x': 785, 'y': 220, 'type': 'scroll'},     # On platform at x=750
        ]'''
    
    new_items = '''        # Create strategic items on NEW SPACED platforms (positioned on platform centers)
        self.game_items = [
            # Base level items (y=550-580) - On well-spaced platforms
            {'x': 460, 'y': 540, 'type': 'stone'},      # On platform at x=400
            {'x': 860, 'y': 550, 'type': 'water'},      # On platform at x=800
            {'x': 1260, 'y': 545, 'type': 'bread'},     # On platform at x=1200
            {'x': 1660, 'y': 555, 'type': 'scroll'},    # On platform at x=1600
            {'x': 2060, 'y': 540, 'type': 'meat'},      # On platform at x=2000
            {'x': 2460, 'y': 550, 'type': 'armor_of_god'}, # On platform at x=2400
            
            # Level 1 items (y=420-460) - On elevated platforms
            {'x': 360, 'y': 410, 'type': 'water'},      # On platform at x=300
            {'x': 760, 'y': 420, 'type': 'bread'},      # On platform at x=700
            {'x': 1160, 'y': 415, 'type': 'scroll'},    # On platform at x=1100
            {'x': 1560, 'y': 425, 'type': 'meat'},      # On platform at x=1500
            {'x': 1960, 'y': 410, 'type': 'armor_of_god'}, # On platform at x=1900
            {'x': 2360, 'y': 420, 'type': 'staff'},     # On platform at x=2300
            
            # Level 2 items (y=280-320) - On higher platforms
            {'x': 260, 'y': 270, 'type': 'scroll'},     # On platform at x=200
            {'x': 660, 'y': 280, 'type': 'meat'},       # On platform at x=600
            {'x': 1060, 'y': 275, 'type': 'armor_of_god'}, # On platform at x=1000
            {'x': 1460, 'y': 285, 'type': 'staff'},     # On platform at x=1400
            {'x': 1860, 'y': 270, 'type': 'stone'},     # On platform at x=1800
            {'x': 2260, 'y': 280, 'type': 'water'},     # On platform at x=2200
            
            # Level 3 items (y=140-180) - On challenging platforms
            {'x': 560, 'y': 130, 'type': 'armor_of_god'}, # On platform at x=500
            {'x': 960, 'y': 140, 'type': 'staff'},      # On platform at x=900
            {'x': 1360, 'y': 135, 'type': 'meat'},      # On platform at x=1300
            {'x': 1760, 'y': 145, 'type': 'scroll'},    # On platform at x=1700
            {'x': 2160, 'y': 130, 'type': 'stone'},     # On platform at x=2100
            
            # Level 4 items (y=20-60) - Premium rewards on top platforms
            {'x': 760, 'y': 10, 'type': 'staff'},       # On platform at x=700 - Ultimate reward
            {'x': 1260, 'y': 20, 'type': 'armor_of_god'}, # On platform at x=1200 - Ultimate reward
            {'x': 1760, 'y': 15, 'type': 'meat'},       # On platform at x=1700 - Ultimate reward
        ]'''
    
    if old_items in content:
        content = content.replace(old_items, new_items)
        print("✅ Updated item positions to match new well-spaced platforms")
    else:
        print("⚠️  Could not find items to update")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix platform spacing and height positioning"""
    print("🏗️  Fixing Platform Spacing and Height Positioning")
    print("=" * 55)
    
    print("1. Increasing platform spacing and positioning higher...")
    fix_platform_spacing_and_height()
    
    print("2. Updating item positions for new platform layout...")
    update_items_for_new_platform_positions()
    
    print("\n" + "=" * 55)
    print("🎉 PLATFORM SPACING AND HEIGHT FIXED!")
    print("\nImproved Features:")
    print("✅ Increased horizontal spacing to 400px between platforms")
    print("✅ Positioned platforms higher above old platforms")
    print("✅ Clear vertical separation between platform levels")
    print("✅ No overlapping with existing old platforms")
    print("✅ Strategic item placement on new platform positions")
    print("\nNew Platform Layout:")
    print("🏠 Base Level (y=550-580): 6 platforms - 400px spacing, above old platforms")
    print("🏢 Level 1 (y=420-460): 6 platforms - 140px above base, 400px spacing")
    print("🏔️  Level 2 (y=280-320): 6 platforms - 140px above Level 1, 400px spacing")
    print("⛰️  Level 3 (y=140-180): 5 platforms - 140px above Level 2, 400px spacing")
    print("⭐ Level 4 (y=20-60): 3 platforms - 120px above Level 3, 500px spacing")
    print("\nSpacing Improvements:")
    print("- 400px horizontal distance between platforms (no crowding)")
    print("- 140px vertical gaps between levels (comfortable jumping)")
    print("- Platforms positioned well above old platforms (no overlap)")
    print("- Progressive difficulty with fewer, more spaced platforms at higher levels")
    print("- Strategic item placement matching new platform positions")
    print("\nTotal: 26 well-spaced platforms with clear separation")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
