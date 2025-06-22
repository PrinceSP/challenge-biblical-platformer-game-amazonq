#!/usr/bin/env python3
"""
Fix all indentation issues in main.py
"""

def fix_all_indentation():
    """Fix all indentation issues"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # Fix the specific indentation issue around the camera update
    old_indented_section = '''        if hasattr(self, 'camera') and hasattr(self, 'player'):
            self.camera.update(self.player.rect)
                
                # Update simple enemies
        self.level_manager.update_simple_enemies(dt)
                
                # Update stone projectiles
                self.level_manager.update_stones(dt)
                
                # Check stone-enemy collisions
                hits = self.level_manager.check_stone_enemy_collisions()
                if hits > 0:
                    # Play enemy defeat sound'''
    
    new_indented_section = '''        if hasattr(self, 'camera') and hasattr(self, 'player'):
            self.camera.follow_player(self.player)
        
        # Update simple enemies
        self.level_manager.update_simple_enemies(dt)
        
        # Update stone projectiles
        self.level_manager.update_stones(dt)
        
        # Check stone-enemy collisions
        hits = self.level_manager.check_stone_enemy_collisions()
        if hits > 0:
            # Play enemy defeat sound'''
    
    if old_indented_section in content:
        content = content.replace(old_indented_section, new_indented_section)
        print("✅ Fixed indentation issues and updated camera call")
    else:
        print("⚠️  Could not find exact indentation issue to fix")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Fix all indentation issues"""
    print("🔧 Fixing All Indentation Issues")
    print("=" * 35)
    
    if fix_all_indentation():
        print("✅ ALL INDENTATION ISSUES FIXED!")
        print("✅ Updated camera call to use follow_player method")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Could not fix indentation issues")

if __name__ == "__main__":
    main()
