#!/usr/bin/env python3
"""
Moses Adventure - Sound Manager
Handles all audio functionality for the biblical platformer game
Separated for clean code organization
"""

import pygame
import os
import math

class SoundManager:
    def __init__(self):
        """Initialize the sound manager"""
        self.sounds = {}
        self.music_enabled = True
        self.sound_enabled = True
        self.current_music = None
        self.music_volume = 0.7
        self.sound_volume = 0.8
        
        # Initialize pygame mixer with better settings
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            pygame.mixer.set_num_channels(8)  # Allow multiple sounds
            print("🎵 Audio system initialized successfully")
        except pygame.error as e:
            print(f"⚠️  Audio initialization warning: {e}")
        
        # Set initial volumes
        pygame.mixer.music.set_volume(self.music_volume)
        
        # Load all sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects from files"""
        sound_files = {
            'jump': 'assets/audio/sounds/jump.wav',
            'pickup': 'assets/audio/sounds/pickup.wav',
            'dialogue': 'assets/audio/sounds/dialogue.wav',
            'menu_select': 'assets/audio/sounds/menu_select.wav',
            'player_hurt': 'assets/audio/sounds/player_hurt.wav',
            'enemy_defeat': 'assets/audio/sounds/enemy_defeat.wav',
            'single_step': 'assets/audio/sounds/single_step.wav',  # NEW: Single step
            'long_walk': 'assets/audio/sounds/long_walk.mp3',     # NEW: Continuous walking
            'pause': 'assets/audio/sounds/pause.wav',             # NEW: Pause sound
            'typing': 'assets/audio/sounds/typing.wav'            # NEW: Dialogue typing
        }
        
        sounds_loaded = 0
        for sound_name, file_path in sound_files.items():
            try:
                if os.path.exists(file_path):
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    self.sounds[sound_name].set_volume(self.sound_volume)
                    sounds_loaded += 1
                    print(f"✅ Loaded sound: {sound_name}")
                else:
                    print(f"⚠️  Sound file not found: {file_path}")
                    self.sounds[sound_name] = None
            except pygame.error as e:
                print(f"❌ Error loading sound {sound_name}: {e}")
                self.sounds[sound_name] = None
        
        if sounds_loaded == 0:
            print("⚠️  No sound files found. Run create_sounds.py to generate them.")
        else:
            print(f"🔊 Loaded {sounds_loaded}/{len(sound_files)} sound files")
        
        # Initialize walking and typing state tracking
        self.is_walking_continuously = False
        self.walking_channel = None
        self.typing_channel = None
    
    def play_single_step(self):
        """Play single step sound for one key press"""
        self.play_sound('single_step')
        print("🦶 Single step sound")
    
    def start_continuous_walking(self):
        """Start continuous walking sound by looping single_step.wav"""
        if not self.is_walking_continuously and 'single_step' in self.sounds and self.sounds['single_step']:
            try:
                # Stop any existing walking sound
                self.stop_movement_sounds()
                
                # Start looping single_step.wav on a dedicated channel
                self.walking_channel = self.sounds['single_step'].play(-1)  # Loop single step indefinitely
                self.is_walking_continuously = True
                print("🚶 Started continuous walking (looping single_step.wav)")
            except pygame.error as e:
                print(f"❌ Error starting walking sound: {e}")
    
    def stop_movement_sounds(self):
        """Stop all movement sounds"""
        if self.walking_channel:
            self.walking_channel.stop()
            self.walking_channel = None
        
        self.is_walking_continuously = False
        print("🛑 Stopped movement sounds")
    
    def play_typing_sound_loop(self):
        """Start looping typing sound for dialogue"""
        if 'typing' in self.sounds and self.sounds['typing']:
            try:
                # Stop any existing typing sound
                self.stop_typing_sound()
                
                # Start looping typing sound
                self.typing_channel = self.sounds['typing'].play(-1)  # Loop indefinitely
                print("⌨️  Started typing sound loop")
            except pygame.error as e:
                print(f"❌ Error starting typing sound: {e}")
    
    def stop_typing_sound(self):
        """Stop typing sound"""
        if hasattr(self, 'typing_channel') and self.typing_channel:
            self.typing_channel.stop()
            self.typing_channel = None
            print("🔇 Stopped typing sound")
    
    def play_pause_sound(self):
        """Play pause sound effect"""
        self.play_sound('pause')
        print("⏸️  Pause sound")
    
    def play_typing_sound(self):
        """Play typing sound for dialogue"""
        self.play_sound('typing')
        print("⌨️  Typing sound")
    
    def lower_music_volume(self, volume_factor=0.3):
        """Lower background music volume (for dialogue)"""
        lowered_volume = self.music_volume * volume_factor
        pygame.mixer.music.set_volume(lowered_volume)
        print(f"🔉 Music volume lowered to {int(lowered_volume * 100)}%")
    
    def restore_music_volume(self):
        """Restore background music to normal volume"""
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"🔊 Music volume restored to {int(self.music_volume * 100)}%")
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if not self.sound_enabled:
            return
            
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                # Stop any previous instance of this sound
                self.sounds[sound_name].stop()
                # Play the sound
                self.sounds[sound_name].play()
            except pygame.error as e:
                print(f"❌ Error playing sound {sound_name}: {e}")
    
    def play_jump_sound(self):
        """Play jump sound effect"""
        self.play_sound('jump')
    
    def play_pickup_sound(self):
        """Play item pickup sound"""
        self.play_sound('pickup')
    
    def play_dialogue_sound(self):
        """Play dialogue notification sound"""
        self.play_sound('dialogue')
    
    def play_menu_sound(self):
        """Play menu selection sound"""
        self.play_sound('menu_select')
    
    def play_hurt_sound(self):
        """Play player hurt sound"""
        self.play_sound('player_hurt')
    
    def play_victory_sound(self):
        """Play enemy defeat sound"""
        self.play_sound('enemy_defeat')
    
    def play_background_music(self, track_name=None):
        """Play background music"""
        # Updated paths - music folder moved into audio folder
        music_files = [
            "assets/audio/music/ancient_egypt.mp3",  # New location after move
            "/Users/javascript/Desktop/my_lab/challenge-biblical-platformer-game-amazonq/assets/audio/music/ancient_egypt.mp3",  # Full path
            "assets/audio/music/ancient_egypt.wav",  # Generated fallback
            "assets/music/ancient_egypt.mp3"   # Old location (fallback)
        ]
        
        music_file = None
        for file_path in music_files:
            if os.path.exists(file_path):
                music_file = file_path
                break
        
        if music_file:
            try:
                if self.current_music != music_file:
                    pygame.mixer.music.load(music_file)
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    self.current_music = music_file
                    self.music_enabled = True
                    print(f"🎵 Playing background music: {os.path.basename(music_file)} from {os.path.dirname(music_file)}")
                elif not pygame.mixer.music.get_busy() and self.music_enabled:
                    # Music was loaded but stopped, restart it
                    pygame.mixer.music.play(-1)
                    print(f"🎵 Restarting background music: {os.path.basename(music_file)}")
            except pygame.error as e:
                print(f"❌ Error playing music: {e}")
        else:
            print("⚠️  No background music found.")
            print("📁 Searched for:")
            for file_path in music_files:
                print(f"   {file_path} {'✅ EXISTS' if os.path.exists(file_path) else '❌ NOT FOUND'}")
            print("💡 Please ensure ancient_egypt.mp3 is in assets/audio/music/ folder")
    
    def toggle_music(self):
        """Toggle background music on/off"""
        self.music_enabled = not self.music_enabled
        
        if self.music_enabled:
            try:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.unpause()
                    print("🎵 Music resumed")
                else:
                    # Start music from beginning
                    self.play_background_music()
            except pygame.error:
                print("🎵 Music enabled (will start when available)")
                self.play_background_music()
        else:
            try:
                pygame.mixer.music.pause()
                print("🔇 Music paused")
            except pygame.error:
                print("🔇 Music disabled")
    
    def toggle_sound(self):
        """Toggle sound effects on/off"""
        self.sound_enabled = not self.sound_enabled
        print(f"🔊 Sound effects {'enabled' if self.sound_enabled else 'disabled'}")
        
        # Test sound when enabling
        if self.sound_enabled:
            print("🔊 Testing sound...")
            self.play_jump_sound()
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        print(f"🎵 Music volume: {int(self.music_volume * 100)}%")
    
    def set_sound_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound_name, sound in self.sounds.items():
            if sound:
                sound.set_volume(self.sound_volume)
        print(f"🔊 Sound volume: {int(self.sound_volume * 100)}%")
    
    def stop_all_sounds(self):
        """Stop all currently playing sounds"""
        pygame.mixer.stop()
        print("🔇 All sounds stopped")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.current_music = None
        print("🔇 Music stopped")
    
    def is_music_playing(self):
        """Check if music is currently playing"""
        return pygame.mixer.music.get_busy()
    
    def get_sound_info(self):
        """Get information about loaded sounds"""
        info = {
            'music_enabled': self.music_enabled,
            'sound_enabled': self.sound_enabled,
            'music_volume': self.music_volume,
            'sound_volume': self.sound_volume,
            'current_music': self.current_music,
            'loaded_sounds': list(self.sounds.keys()),
            'working_sounds': [name for name, sound in self.sounds.items() if sound is not None]
        }
        return info
    
    def print_status(self):
        """Print current audio system status"""
        info = self.get_sound_info()
        print("\n🎵 === Audio System Status ===")
        print(f"Music: {'🎵 ON' if info['music_enabled'] else '🔇 OFF'} (Volume: {int(info['music_volume'] * 100)}%)")
        print(f"Sound: {'🔊 ON' if info['sound_enabled'] else '🔇 OFF'} (Volume: {int(info['sound_volume'] * 100)}%)")
        print(f"Current Music: {info['current_music'] or 'None'}")
        print(f"Working Sounds: {len(info['working_sounds'])}/{len(info['loaded_sounds'])}")
        if info['working_sounds']:
            print(f"Available: {', '.join(info['working_sounds'])}")
        print("=" * 30)

# Test function
def test_sound_manager():
    """Test the sound manager functionality"""
    print("🧪 Testing Sound Manager...")
    
    # Initialize pygame
    pygame.init()
    
    # Create sound manager
    sm = SoundManager()
    
    # Print status
    sm.print_status()
    
    # Test sounds
    print("\n🔊 Testing sounds...")
    sm.play_jump_sound()
    
    # Test music
    print("\n🎵 Testing music...")
    sm.play_background_music()
    
    print("\n✅ Sound Manager test complete!")

if __name__ == "__main__":
    test_sound_manager()
