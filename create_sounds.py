#!/usr/bin/env python3
"""
Moses Adventure - Sound Creation System
Creates WAV sound files for the biblical platformer game
Based on the Road Fighter sound creation example
"""

import wave
import math
import struct
import os

def create_wav_file(filename, frequency, duration, sample_rate=44100, amplitude=0.5):
    """Create a simple WAV file with a sine wave"""
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("assets/audio/sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("assets/audio/sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate sine wave data
        for i in range(frames):
            # Calculate sine wave value
            time_point = float(i) / sample_rate
            wave_value = amplitude * math.sin(frequency * 2 * math.pi * time_point)
            
            # Apply fade out to avoid clicks
            fade = 1.0 - (float(i) / frames)
            wave_value = wave_value * fade
            
            # Convert to 16-bit integer
            sample = int(wave_value * 32767)
            
            # Write stereo sample (left and right channels)
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

def create_biblical_music(filename, duration=20.0):
    """Create biblical-themed background music (only if file doesn't exist)"""
    # Check if user already has ancient_egypt.mp3
    user_music_path = "assets/music/ancient_egypt.mp3"
    if os.path.exists(user_music_path):
        print(f"✅ Found existing music file: {user_music_path}")
        print("🎵 Skipping music generation - using your custom file")
        return
    
    sample_rate = 44100
    frames = int(duration * sample_rate)
    
    # Ensure music directory exists
    os.makedirs("assets/audio/music", exist_ok=True)
    
    # Full path to music folder
    filepath = os.path.join("assets/audio/music", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate biblical-style music with multiple layers
        for i in range(frames):
            time_point = float(i) / sample_rate
            
            # Deep bass foundation (like ancient drums)
            bass = 0.4 * math.sin(2 * math.pi * 60 * time_point)
            
            # Mid-range harmony (like ancient harps)
            harmony1 = 0.3 * math.sin(2 * math.pi * 220 * time_point)  # A note
            harmony2 = 0.2 * math.sin(2 * math.pi * 330 * time_point)  # E note
            
            # High frequency (like ancient flutes)
            flute = 0.15 * math.sin(2 * math.pi * 440 * time_point)  # A note higher
            
            # Add some mystical reverb effect
            reverb = 0.1 * math.sin(2 * math.pi * 880 * time_point * 0.5)
            
            # Combine all layers
            combined = bass + harmony1 + harmony2 + flute + reverb
            
            # Apply gentle volume variation (breathing effect)
            volume_variation = 0.7 + 0.3 * math.sin(2 * math.pi * 0.3 * time_point)
            combined *= volume_variation
            
            # Convert to 16-bit integer
            sample = int(combined * 12000)  # Moderate amplitude
            
            # Write stereo sample
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

def create_walking_sound(filename, is_running=False):
    """Create walking or running sound effect"""
    sample_rate = 44100
    duration = 0.4 if not is_running else 0.3  # Running is faster
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("assets/audio/sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("assets/audio/sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate footstep sound
        for i in range(frames):
            time_point = float(i) / sample_rate
            progress = float(i) / frames
            
            if is_running:
                # Running sound - faster, more intense
                # Create two footsteps per cycle
                step_frequency = 8  # Steps per second
                base_freq = 80 + (20 * math.sin(step_frequency * 2 * math.pi * time_point))
                
                # Add some gravel/dirt texture
                texture = 0.3 * math.sin(1200 * 2 * math.pi * time_point)
                
                # Main footstep sound
                footstep = 0.4 * math.sin(base_freq * 2 * math.pi * time_point)
                
                # Combine
                wave_value = footstep + texture
                
                # Apply envelope for footstep rhythm
                step_envelope = abs(math.sin(step_frequency * math.pi * time_point))
                wave_value *= step_envelope * 0.6
                
            else:
                # Walking sound - slower, gentler
                # Create footsteps
                step_frequency = 4  # Steps per second
                base_freq = 60 + (15 * math.sin(step_frequency * 2 * math.pi * time_point))
                
                # Add some soft ground texture
                texture = 0.2 * math.sin(800 * 2 * math.pi * time_point)
                
                # Main footstep sound
                footstep = 0.3 * math.sin(base_freq * 2 * math.pi * time_point)
                
                # Combine
                wave_value = footstep + texture
                
                # Apply envelope for footstep rhythm
                step_envelope = abs(math.sin(step_frequency * math.pi * time_point))
                wave_value *= step_envelope * 0.4
            
            # Apply overall fade to avoid clicks
            if progress < 0.1:
                fade = progress / 0.1
            elif progress > 0.9:
                fade = (1.0 - progress) / 0.1
            else:
                fade = 1.0
            
            wave_value *= fade
            
            # Convert to 16-bit integer
            sample = int(wave_value * 32767)
            
            # Write stereo sample
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)
    """Create a jump sound effect"""
    sample_rate = 44100
    duration = 0.3
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("assets/audio/sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("assets/audio/sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate jump sound (rising frequency)
        for i in range(frames):
            time_point = float(i) / sample_rate
            progress = float(i) / frames
            
            # Rising frequency from 200Hz to 600Hz
            frequency = 200 + (400 * progress)
            
            # Create the wave
            wave_value = 0.3 * math.sin(frequency * 2 * math.pi * time_point)
            
            # Apply envelope (quick attack, slow decay)
            if progress < 0.1:
                envelope = progress / 0.1
            else:
                envelope = 1.0 - ((progress - 0.1) / 0.9)
            
            wave_value *= envelope
            
            # Convert to 16-bit integer
            sample = int(wave_value * 32767)
            
            # Write stereo sample
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

# Create sound files for Moses Adventure
def create_all_sounds():
    """Create all sound files for Moses Adventure"""
    print("🎵 Creating sound files for Moses Adventure...")
    print("📁 Files will be created in assets/audio/ folders")
def create_jump_sound(filename):
    """Create a jump sound effect"""
    sample_rate = 44100
    duration = 0.3
    frames = int(duration * sample_rate)
    
    # Ensure sounds directory exists
    os.makedirs("assets/audio/sounds", exist_ok=True)
    
    # Full path to sounds folder
    filepath = os.path.join("assets/audio/sounds", filename)
    
    # Open WAV file for writing
    with wave.open(filepath, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(2)  # Stereo
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Generate jump sound (rising frequency)
        for i in range(frames):
            time_point = float(i) / sample_rate
            progress = float(i) / frames
            
            # Rising frequency from 200Hz to 600Hz
            frequency = 200 + (400 * progress)
            
            # Create the wave
            wave_value = 0.3 * math.sin(frequency * 2 * math.pi * time_point)
            
            # Apply envelope (quick attack, slow decay)
            if progress < 0.1:
                envelope = progress / 0.1
            else:
                envelope = 1.0 - ((progress - 0.1) / 0.9)
            
            wave_value *= envelope
            
            # Convert to 16-bit integer
            sample = int(wave_value * 32767)
            
            # Write stereo sample
            packed_value = struct.pack('<hh', sample, sample)
            wav_file.writeframes(packed_value)

# Create sound files for Moses Adventure
def create_all_sounds():
    """Create all sound files for Moses Adventure"""
    print("🎵 Creating sound files for Moses Adventure...")
    print("📁 Files will be created in assets/audio/ folders")
    
    try:
        # Jump sound - rising tone
        create_jump_sound("jump.wav")
        print("✅ Created assets/audio/sounds/jump.wav")
        
        # Walking sound - gentle footsteps
        create_walking_sound("walk.wav", is_running=False)
        print("✅ Created assets/audio/sounds/walk.wav")
        
        # Running sound - faster footsteps
        create_walking_sound("run.wav", is_running=True)
        print("✅ Created assets/audio/sounds/run.wav")
        
        # Item pickup sound - pleasant chime
        create_wav_file("pickup.wav", 800, 0.4, amplitude=0.3)
        print("✅ Created assets/audio/sounds/pickup.wav")
        
        # Dialogue sound - soft notification
        create_wav_file("dialogue.wav", 500, 0.2, amplitude=0.2)
        print("✅ Created assets/audio/sounds/dialogue.wav")
        
        # Menu select sound - click
        create_wav_file("menu_select.wav", 600, 0.1, amplitude=0.15)
        print("✅ Created assets/audio/sounds/menu_select.wav")
        
        # Player hurt sound - low warning
        create_wav_file("player_hurt.wav", 150, 0.5, amplitude=0.4)
        print("✅ Created assets/audio/sounds/player_hurt.wav")
        
        # Enemy defeat sound - victory chime
        create_wav_file("enemy_defeat.wav", 700, 0.6, amplitude=0.3)
        print("✅ Created assets/audio/sounds/enemy_defeat.wav")
        
        # Walking sound - gentle footsteps
        create_walking_sound("walk.wav", is_running=False)
        print("✅ Created assets/audio/sounds/walk.wav")
        
        # Running sound - faster footsteps
        create_walking_sound("run.wav", is_running=True)
        print("✅ Created assets/audio/sounds/run.wav")
        
        # Biblical background music (only if user doesn't have their own)
        create_biblical_music("ancient_egypt.wav", duration=30.0)
        
        # Check if user has their own music file
        user_music_path = "assets/music/ancient_egypt.mp3"
        if os.path.exists(user_music_path):
            print(f"✅ Using your custom music: {user_music_path}")
        else:
            print("✅ Created assets/audio/music/ancient_egypt.wav")
        
        print("\n🎉 All sound files created successfully!")
        print("🎮 Moses Adventure now has full audio support!")
        print("🎵 Background music: ancient_egypt.wav (30 seconds, loops)")
        print("🔊 Sound effects: jump, pickup, dialogue, menu, hurt, defeat")
        print("\n📝 Note: You can replace these with your own custom audio files")
        print("📁 Just keep the same filenames and folder structure")
        
    except Exception as e:
        print(f"❌ Error creating sound files: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_all_sounds()
