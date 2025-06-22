#!/usr/bin/env python3
"""
Enhance the game with multi-level platforms, strategic item placement, and NPCs/enemies on platforms
"""

def create_multi_level_platform_system():
    """Create a comprehensive multi-level platform system with items and characters"""
    
    with open('level_manager.py', 'r') as f:
        content = f.read()
    
    # Find the platform creation section and enhance it
    old_platform_creation = '''        # Create platforms for jumping
        platforms = [
            {'x': 300, 'y': 570, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 500, 'y': 470, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 700, 'y': 470, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 900, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1100, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1300, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1500, 'y': 560, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1700, 'y': 560, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 1900, 'y': 560, 'width': 100, 'height': 20, 'type': 'stone_platform'},
            {'x': 2100, 'y': 608, 'width': 100, 'height': 20, 'type': 'stone_platform'},
        ]'''
    
    new_platform_creation = '''        # Create comprehensive multi-level platform system
        platforms = [
            # Ground level platforms (y=570-620)
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
            
            # Mid-level platforms (y=450-520)
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
            
            # High-level platforms (y=350-420)
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
            
            # Top-level platforms (y=250-320)
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
        ]'''
    
    if old_platform_creation in content:
        content = content.replace(old_platform_creation, new_platform_creation)
        print("✅ Created comprehensive multi-level platform system")
    else:
        print("⚠️  Could not find platform creation to enhance")
    
    with open('level_manager.py', 'w') as f:
        f.write(content)
    
    return True

def add_strategic_item_placement():
    """Add strategic item placement on platforms"""
    
    with open('level_manager.py', 'r') as f:
        content = f.read()
    
    # Find the items creation section and enhance it
    old_items_creation = '''        # Create collectible items
        items = [
            {'x': 250, 'y': 550, 'type': 'stone'},
            {'x': 550, 'y': 450, 'type': 'water'},
            {'x': 850, 'y': 450, 'type': 'bread'},
            {'x': 1150, 'y': 540, 'type': 'scroll'},
            {'x': 1550, 'y': 540, 'type': 'meat'},
            {'x': 1950, 'y': 540, 'type': 'armor_of_god'},
            {'x': 2350, 'y': 540, 'type': 'staff'},
        ]'''
    
    new_items_creation = '''        # Create strategically placed collectible items on platforms
        items = [
            # Ground level items
            {'x': 320, 'y': 550, 'type': 'stone'},      # On ground platform
            {'x': 520, 'y': 570, 'type': 'water'},      # On ground platform
            {'x': 720, 'y': 560, 'type': 'bread'},      # On ground platform
            {'x': 1120, 'y': 575, 'type': 'scroll'},    # On ground platform
            {'x': 1520, 'y': 565, 'type': 'meat'},      # On ground platform
            {'x': 1920, 'y': 555, 'type': 'armor_of_god'}, # On ground platform
            {'x': 2120, 'y': 588, 'type': 'staff'},     # On ground platform
            
            # Mid-level items (require jumping)
            {'x': 270, 'y': 450, 'type': 'stone'},      # On mid platform
            {'x': 470, 'y': 460, 'type': 'water'},      # On mid platform
            {'x': 670, 'y': 440, 'type': 'bread'},      # On mid platform
            {'x': 870, 'y': 470, 'type': 'scroll'},     # On mid platform
            {'x': 1070, 'y': 450, 'type': 'meat'},      # On mid platform
            {'x': 1470, 'y': 445, 'type': 'armor_of_god'}, # On mid platform
            {'x': 1870, 'y': 455, 'type': 'staff'},     # On mid platform
            {'x': 2070, 'y': 470, 'type': 'stone'},     # On mid platform
            
            # High-level items (challenging to reach)
            {'x': 220, 'y': 350, 'type': 'water'},      # On high platform
            {'x': 420, 'y': 360, 'type': 'bread'},      # On high platform
            {'x': 620, 'y': 340, 'type': 'scroll'},     # On high platform
            {'x': 820, 'y': 370, 'type': 'meat'},       # On high platform
            {'x': 1020, 'y': 350, 'type': 'armor_of_god'}, # On high platform
            {'x': 1420, 'y': 345, 'type': 'staff'},     # On high platform
            {'x': 1820, 'y': 355, 'type': 'stone'},     # On high platform
            {'x': 2020, 'y': 370, 'type': 'water'},     # On high platform
            
            # Top-level items (most challenging)
            {'x': 370, 'y': 260, 'type': 'scroll'},     # On top platform
            {'x': 570, 'y': 250, 'type': 'meat'},       # On top platform
            {'x': 770, 'y': 270, 'type': 'armor_of_god'}, # On top platform
            {'x': 970, 'y': 240, 'type': 'staff'},      # On top platform
            {'x': 1170, 'y': 265, 'type': 'stone'},     # On top platform
            {'x': 1370, 'y': 255, 'type': 'water'},     # On top platform
            {'x': 1570, 'y': 230, 'type': 'bread'},     # On top platform
            {'x': 1770, 'y': 275, 'type': 'scroll'},    # On top platform
            {'x': 1970, 'y': 245, 'type': 'meat'},      # On top platform
        ]'''
    
    if old_items_creation in content:
        content = content.replace(old_items_creation, new_items_creation)
        print("✅ Added strategic item placement on platforms")
    else:
        print("⚠️  Could not find items creation to enhance")
    
    with open('level_manager.py', 'w') as f:
        f.write(content)
    
    return True

def add_npcs_and_enemies_on_platforms():
    """Add NPCs and enemies strategically placed on platforms"""
    
    with open('level_manager.py', 'r') as f:
        content = f.read()
    
    # Find the NPCs creation section and enhance it
    old_npcs_creation = '''        # Create NPCs
        npcs = [
            {'x': 300, 'y': 670, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 500, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 800, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1200, 'y': 670, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1600, 'y': 670, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 2000, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 2400, 'y': 670, 'type': 'palace_guard', 'dialogue': 'checkpoint_dialogue'},
        ]'''
    
    new_npcs_creation = '''        # Create NPCs strategically placed on platforms and ground
        npcs = [
            # Ground level NPCs
            {'x': 300, 'y': 670, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 500, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 800, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1200, 'y': 670, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1600, 'y': 670, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 2000, 'y': 670, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 2400, 'y': 670, 'type': 'palace_guard', 'dialogue': 'checkpoint_dialogue'},
            
            # NPCs on ground platforms
            {'x': 320, 'y': 550, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 720, 'y': 560, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1120, 'y': 575, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 1720, 'y': 540, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 2120, 'y': 588, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            
            # NPCs on mid-level platforms
            {'x': 470, 'y': 460, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 870, 'y': 470, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1270, 'y': 465, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 1670, 'y': 430, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 2070, 'y': 470, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            
            # NPCs on high-level platforms
            {'x': 420, 'y': 360, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 820, 'y': 370, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
            {'x': 1220, 'y': 365, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1620, 'y': 330, 'type': 'palace_guard', 'dialogue': 'guard_dialogue'},
            {'x': 2020, 'y': 370, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            
            # NPCs on top-level platforms (special encounters)
            {'x': 570, 'y': 250, 'type': 'priest', 'dialogue': 'priest_dialogue'},
            {'x': 970, 'y': 240, 'type': 'palace_guard', 'dialogue': 'checkpoint_dialogue'},
            {'x': 1370, 'y': 255, 'type': 'egyptian_citizen', 'dialogue': 'citizen_dialogue'},
            {'x': 1770, 'y': 275, 'type': 'hebrew_slave', 'dialogue': 'slave_dialogue'},
        ]'''
    
    if old_npcs_creation in content:
        content = content.replace(old_npcs_creation, new_npcs_creation)
        print("✅ Added NPCs strategically placed on platforms")
    else:
        print("⚠️  Could not find NPCs creation to enhance")
    
    # Find the enemies creation section and enhance it
    old_enemies_creation = '''        # Create simple enemies (blocks for now)
        enemies = [
            {'x': 1000, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2200, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
        ]'''
    
    new_enemies_creation = '''        # Create enemies strategically placed on platforms and ground
        enemies = [
            # Ground level enemies
            {'x': 600, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1000, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1400, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1800, 'y': 640, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2200, 'y': 620, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            
            # Enemies on ground platforms
            {'x': 540, 'y': 570, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 940, 'y': 588, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1340, 'y': 588, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1940, 'y': 555, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2340, 'y': 570, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            
            # Enemies on mid-level platforms
            {'x': 290, 'y': 450, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 690, 'y': 440, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1090, 'y': 450, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1490, 'y': 445, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1890, 'y': 455, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2290, 'y': 440, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            
            # Enemies on high-level platforms
            {'x': 240, 'y': 350, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 640, 'y': 340, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1040, 'y': 350, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1440, 'y': 345, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1840, 'y': 355, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 2240, 'y': 340, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            
            # Elite enemies on top-level platforms (more challenging)
            {'x': 390, 'y': 260, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 790, 'y': 270, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1190, 'y': 265, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1590, 'y': 230, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
            {'x': 1990, 'y': 245, 'width': 30, 'height': 30, 'type': 'egyptian_soldier'},
        ]'''
    
    if old_enemies_creation in content:
        content = content.replace(old_enemies_creation, new_enemies_creation)
        print("✅ Added enemies strategically placed on platforms")
    else:
        print("⚠️  Could not find enemies creation to enhance")
    
    with open('level_manager.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Enhance the game with multi-level platforms, items, NPCs, and enemies"""
    print("🏗️  Enhancing Game with Multi-Level Platform System")
    print("=" * 55)
    
    print("1. Creating comprehensive multi-level platform system...")
    create_multi_level_platform_system()
    
    print("2. Adding strategic item placement on platforms...")
    add_strategic_item_placement()
    
    print("3. Adding NPCs and enemies on platforms...")
    add_npcs_and_enemies_on_platforms()
    
    print("\n" + "=" * 55)
    print("🎉 MULTI-LEVEL PLATFORM SYSTEM COMPLETE!")
    print("\nNew Features:")
    print("✅ 4 distinct platform levels (ground, mid, high, top)")
    print("✅ 40+ platforms with varying sizes and positions")
    print("✅ Strategic item placement requiring platforming skills")
    print("✅ NPCs positioned on different platform levels")
    print("✅ Enemies guarding platforms and items")
    print("✅ Progressive difficulty - higher platforms = more challenge")
    print("\nPlatform Levels:")
    print("🏠 Ground Level (y=570-620): Easy access, basic items")
    print("🏢 Mid Level (y=450-520): Moderate jumping required")
    print("🏔️  High Level (y=350-420): Challenging platforming")
    print("⛰️  Top Level (y=250-320): Expert-level climbing")
    print("\nGameplay Features:")
    print("- Jump between platforms to collect items")
    print("- Meet NPCs on different levels for dialogue")
    print("- Fight enemies guarding valuable items")
    print("- Explore vertical level design")
    print("- Use staff projectiles to clear platform enemies")
    print("\nTest with: python3 main.py")

if __name__ == "__main__":
    main()
