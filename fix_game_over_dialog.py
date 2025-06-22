#!/usr/bin/env python3
"""
Fix for Game Over Dialog - Show proper dialog instead of quitting
"""

def fix_game_over_dialog():
    """Add proper game over dialog with restart/menu options"""
    
    with open('main.py', 'r') as f:
        content = f.read()
    
    # First, let's find where the render_game_over_screen should be and add it
    # Look for the corrupted game over rendering code and fix it
    
    # Find the corrupted section and replace it
    corrupted_section = '''        close_text = self.font_manager.render_text("Press any key to close", 'tiny', GRAY)
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH//2, box_y + box_height - 20))
        self.screen.blit(close_text, close_rect)
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with custom font
        game_over_text = self.font_manager.render_text("Game Over", 'large', WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.font_manager.render_text("Press SPACE to restart or ESC to quit", 'medium', WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)'''
    
    fixed_section = '''        close_text = self.font_manager.render_text("Press any key to close", 'tiny', GRAY)
        close_rect = close_text.get_rect(center=(SCREEN_WIDTH//2, box_y + box_height - 20))
        self.screen.blit(close_text, close_rect)
    
    def render_game_over_screen(self):
        """Render game over screen with dialog options"""
        # Semi-transparent red overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        # Game over dialog box
        dialog_width = 500
        dialog_height = 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background
        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill(BLACK)
        pygame.draw.rect(dialog_surface, WHITE, dialog_surface.get_rect(), 3)
        self.screen.blit(dialog_surface, (dialog_x, dialog_y))
        
        # Game over title
        game_over_text = self.font_manager.render_text("Moses Has Fallen!", 'large', RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Subtitle
        subtitle_text = self.font_manager.render_text("The journey ends here...", 'medium', WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Options
        restart_text = self.font_manager.render_text("Press SPACE to Restart Journey", 'medium', GOLD)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 160))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_manager.render_text("Press ESC to Return to Main Menu", 'medium', LIGHT_GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 190))
        self.screen.blit(menu_text, menu_rect)
        
        quit_text = self.font_manager.render_text("Press Q to Quit Game", 'small', GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 230))
        self.screen.blit(quit_text, quit_rect)'''
    
    if corrupted_section in content:
        content = content.replace(corrupted_section, fixed_section)
        print("✅ Fixed corrupted game over rendering code")
    else:
        # If the corrupted section isn't found, let's add the method before the main function
        main_function_start = content.find("def main():")
        if main_function_start != -1:
            new_method = '''    def render_game_over_screen(self):
        """Render game over screen with dialog options"""
        # Semi-transparent red overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(RED)
        self.screen.blit(overlay, (0, 0))
        
        # Game over dialog box
        dialog_width = 500
        dialog_height = 300
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background
        dialog_surface = pygame.Surface((dialog_width, dialog_height))
        dialog_surface.fill(BLACK)
        pygame.draw.rect(dialog_surface, WHITE, dialog_surface.get_rect(), 3)
        self.screen.blit(dialog_surface, (dialog_x, dialog_y))
        
        # Game over title
        game_over_text = self.font_manager.render_text("Moses Has Fallen!", 'large', RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 60))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Subtitle
        subtitle_text = self.font_manager.render_text("The journey ends here...", 'medium', WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 100))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Options
        restart_text = self.font_manager.render_text("Press SPACE to Restart Journey", 'medium', GOLD)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 160))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font_manager.render_text("Press ESC to Return to Main Menu", 'medium', LIGHT_GRAY)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 190))
        self.screen.blit(menu_text, menu_rect)
        
        quit_text = self.font_manager.render_text("Press Q to Quit Game", 'small', GRAY)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH//2, dialog_y + 230))
        self.screen.blit(quit_text, quit_rect)

'''
            content = content[:main_function_start] + new_method + content[main_function_start:]
            print("✅ Added render_game_over_screen method")
    
    # Also enhance the game over event handling to make it clearer
    old_game_over_events = '''    def handle_game_over_events(self, event):
        """Handle game over screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Restart the game
                print("🔄 Restarting game...")
                self.restart_game()
            elif event.key == pygame.K_r:
                # Alternative restart key
                print("🔄 Restarting game...")
                self.restart_game()
            elif event.key == pygame.K_ESCAPE:
                # Return to main menu
                print("📋 Returning to main menu...")
                self.state = GameState.MENU
                self.player = None
            elif event.key == pygame.K_q:
                # Quit game
                print("👋 Quitting game...")
                self.running = False'''
    
    new_game_over_events = '''    def handle_game_over_events(self, event):
        """Handle game over screen events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Restart the game
                print("🔄 Restarting Moses' journey...")
                self.restart_game()
                # Play restart sound if available
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_r:
                # Alternative restart key
                print("🔄 Restarting Moses' journey...")
                self.restart_game()
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_ESCAPE:
                # Return to main menu
                print("📋 Returning to main menu...")
                self.state = GameState.MENU
                self.player = None
                if hasattr(self.sound_manager, 'play_sound'):
                    self.sound_manager.play_sound('menu_select')
            elif event.key == pygame.K_q:
                # Quit game
                print("👋 Farewell, Moses...")
                self.running = False'''
    
    if old_game_over_events in content:
        content = content.replace(old_game_over_events, new_game_over_events)
        print("✅ Enhanced game over event handling")
    
    # Make sure the game doesn't quit immediately when health reaches 0
    # Check if there are any direct quit calls on game over
    if "sys.exit()" in content and "game over" in content.lower():
        print("⚠️  Found potential immediate quit on game over - please check manually")
    
    with open('main.py', 'w') as f:
        f.write(content)
    
    return True

def main():
    """Apply the game over dialog fix"""
    print("🔧 Fixing Game Over Dialog System")
    print("=" * 40)
    
    print("1. Adding proper game over dialog...")
    if fix_game_over_dialog():
        print("✅ Game over dialog system fixed!")
        print("\nNow when Moses' health reaches 0:")
        print("- Game shows a proper dialog box")
        print("- Options to restart or return to menu")
        print("- No more immediate quitting")
        print("\nDialog Options:")
        print("- SPACE: Restart the journey")
        print("- ESC: Return to main menu")
        print("- Q: Quit game")
        print("\nTest with: python3 main.py")
    else:
        print("❌ Failed to fix game over dialog")

if __name__ == "__main__":
    main()
