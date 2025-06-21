import pygame
import math

# Test if we can create and play sounds
pygame.init()

try:
    pygame.mixer.init()
    print("Audio system initialized successfully!")
    
    # Create a simple beep
    duration = 0.5
    sample_rate = 22050
    frames = int(duration * sample_rate)
    
    # Generate a sine wave
    arr = []
    for i in range(frames):
        wave = int(16383 * math.sin(2 * math.pi * 440 * i / sample_rate))  # 440 Hz A note
        arr.append([wave, wave])
    
    # Create sound from array
    sound = pygame.sndarray.make_sound(pygame.array.array('h', arr))
    
    print("Playing test sound...")
    pygame.mixer.Sound.play(sound)
    
    # Wait for sound to finish
    pygame.time.wait(600)
    
    print("Sound test completed!")
    
except Exception as e:
    print(f"Audio test failed: {e}")

pygame.quit()