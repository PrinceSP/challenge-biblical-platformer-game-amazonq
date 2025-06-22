#!/usr/bin/env python3
"""
Fix the staff inventory bug - KeyError when using staff
"""

def fix_staff_inventory_bug():
    """Fix the staff inventory usage bug"""
    
    with open('game_systems.py', 'r') as f:
        content = f.read()
    
    # Find the use_item method and fix the logic
    old_use_item = '''    def use_item(self, item_type, player=None):
        """Use an item from inventory with game effects"""
        if item_type in self.items and self.items[item_type] > 0:
            # Apply item effects and check if item should be consumed
            item_consumed = True
            if player:
                item_consumed = self.apply_item_effect(item_type, player)
            
            # Only consume item if it should be consumed (scroll is unlimited)
            if item_consumed:
                self.items[item_type] -= 1
                if self.items[item_type] == 0:
                    del self.items[item_type]
                print(f"✅ Used {item_type}! (Consumed)")
            else:
                print(f"✅ Used {item_type}! (Unlimited use)")
            
            return True
        else:
            print(f"❌ No {item_type} in inventory!")
            return False'''
    
    new_use_item = '''    def use_item(self, item_type, player=None):
        """Use an item from inventory with game effects"""
        if item_type in self.items and self.items[item_type] > 0:
            # Apply item effects and check if item should be consumed
            item_consumed = True
            if player:
                item_consumed = self.apply_item_effect(item_type, player)
            
            # Special handling for staff - it removes itself in apply_item_effect
            if item_type == "staff" and item_consumed:
                # Staff already handled its own removal
                print(f"✅ Used {item_type}! (Consumed)")
                return True
            
            # Only consume item if it should be consumed (scroll is unlimited)
            if item_consumed and item_type in self.items:
                self.items[item_type] -= 1
                if self.items[item_type] == 0:
                    del self.items[item_type]
                print(f"✅ Used {item_type}! (Consumed)")
            else:
                print(f"✅ Used {item_type}! (Unlimited use)")
            
            return True
        else:
            print(f"❌ No {item_type} in inventory!")
            return False'''
    
    if old_use_item in content:
        content = content.replace(old_use_item, new_use_item)
        print("✅ Fixed staff inventory bug")
        
        with open('game_systems.py', 'w') as f:
            f.write(content)
        return True
    
    print("⚠️  Could not find use_item method to fix")
    return False

def main():
    """Fix the staff inventory bug"""
    print("🔧 Fixing Staff Inventory Bug")
    print("=" * 30)
    
    if fix_staff_inventory_bug():
        print("\n✅ Staff inventory bug fixed!")
        print("Now you can use the staff from inventory without crashes")
        print("\nTest again with: python3 main.py")
    else:
        print("\n❌ Failed to fix staff inventory bug")

if __name__ == "__main__":
    main()
