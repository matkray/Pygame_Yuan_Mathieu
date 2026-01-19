"""
Sound manager for game sound effects (for now beeping)
"""

import pygame
import math
import array

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def generate_tone(frequency, duration, sample_rate=22050, volume=0.3):
  frames = int(duration * sample_rate)
  max_sample = 2**(16-1)-1

  samples = array.array('h') # 'h' = signed short (16-bit)

  for i in range(frames):
    wave = int(4096 * math.sin(2 * math.pi * frequency * i / sample_rate) * volume)
    wave = max(-max_sample, min(max_sample, wave))
    samples.append(wave) # Left
    samples.append(wave) # Right

  samples_bytes = samples.tobytes()
  sound = pygame.mixer.Sound(samples_bytes)
  return sound

jump_sound = None
landing_sound = None


import numpy as np
import pygame.sndarray

def generate_tone(frequency, duration, sample_rate=22050, volume=0.3):
  frames = int(duration * sample_rate)
  arr = np.zeros((frames, 2), dtype=np.int16)
  max_sample = 2**(16-1)-1

  for i in range(frames):
    wave = int(4096 * np.sin(2 * np.pi * frequency * i / sample_rate) * volume)
    wave = max(-max_sample, min(max_sample, wave))
    arr[i][0] = wave  # Left
    arr[i][1] = wave  # Right

  return pygame.sndarray.make_sound(arr)

jump_sound = generate_tone(800, 0.1, volume=0.2)
landing_sound = generate_tone(200, 0.15, volume=0.3)

def play_jump_sound():
  if enabled and jump_sound is not None:
    jump_sound.set_volume(volume)
    jump_sound.play()

def play_landing_sound():
  if enabled and landing_sound is not None:
    landing_sound.set_volume(volume)
    landing_sound.play()