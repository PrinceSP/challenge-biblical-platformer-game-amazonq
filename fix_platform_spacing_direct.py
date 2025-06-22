#!/usr/bin/env python3
"""
Direct fix for platform spacing and height positioning
"""

def fix_platform_spacing_direct():
    """Directly replace the platform system with better spacing and height"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Find the exact platform system and replace it
    old_platform_start = "# Create platform system with REACHABLE positions for Moses"
    old_platform_end = "# Level 4 - Top platforms"
    
    start_pos = content.find(old_platform_start)
    if start_pos != -1:
        # Find the end of the platform system
        end_marker = "        ]"
        end_pos = content.find(end_marker, start_pos)
        if end_pos != -1:
            end_pos += len(end_marker)
            
            # Create new well-spaced platform system
            new_platform_system = '''        # Create platform system with INCREASED SPACING and HIGHER POSITIONING
        # Old platforms are around y=608-670, new platforms positioned well above them
        # 400px horizontal spacing, 140px vertical spacing between levels
        self.game_platforms = [
            # Base level - HIGHER above old platforms (y=550-580) - Clear separation
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
            
            # Replace the old platform system
            content = content[:start_pos] + new_platform_system + content[end_pos:]
            print("✅ Directly replaced platform system with increased spacing and higher positioning")
            
            with open('main.py', 'w') as f:
                f.write(content)
            
            return True
    
    print("❌ Could not find platform system to replace")
    return False

def main():
    """Direct fix for platform spacing and height"""
    print("🏗️  Direct Fix: Platform Spacing and Height")
    print("=" * 45)
    
    if fix_platform_spacing_direct():
        print("\n✅ PLATFORM SPACING AND HEIGHT FIXED!")
        print("\nNew Platform Layout:")
        print("🏠 Base Level (y=550-580): 6 platforms - 400px spacing")
        print("🏢 Level 1 (y=420-460): 6 platforms - 400px spacing")
        print("🏔️  Level 2 (y=280-320): 6 platforms - 400px spacing")
        print("⛰️  Level 3 (y=140-180): 5 platforms - 400px spacing")
        print("⭐ Level 4 (y=20-60): 3 platforms - 500px spacing")
        print("\nSpacing Improvements:")
        print("- 400px horizontal distance (no crowding)")
        print("- 140px vertical gaps (comfortable jumping)")
        print("- Positioned well above old platforms (no overlap)")
        print("- Progressive difficulty with fewer platforms at higher levels")
        print("\nTotal: 26 well-spaced platforms")
        print("\nTest with: python3 main.py")
    else:
        print("\n❌ Failed to fix platform spacing")

if __name__ == "__main__":
    main()
