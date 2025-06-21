#!/usr/bin/env python3
"""
Sprite Generator for Moses Adventure Game
Creates placeholder sprites for all game assets
"""

import pygame
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Initialize Pygame for color constants
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
BLUE = (70, 130, 180)
DARK_BLUE = (25, 25, 112)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
RED = (220, 20, 60)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
BEIGE = (245, 245, 220)
SAND = (194, 178, 128)

def create_directory_structure():
    """Create all necessary directories"""
    directories = [
        "assets/sprites/player",
        "assets/sprites/npcs",
        "assets/sprites/enemies",
        "assets/items",
        "assets/backgrounds",
        "assets/ui",
        "assets/music",
        "assets/sounds",
        "assets/tiles"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("Directory structure created!")

def create_player_sprites():
    """Create Moses player sprites"""
    print("Creating player sprites...")
    
    # Moses idle sprite
    moses_idle = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(moses_idle)
    
    # Head (beige skin tone)
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Beard (gray/white)
    draw.ellipse([8, 10, 24, 20], fill=LIGHT_GRAY, outline=BLACK)
    
    # Body (brown robe)
    draw.rectangle([8, 14, 24, 35], fill=BROWN, outline=BLACK)
    
    # Arms
    draw.rectangle([4, 18, 8, 30], fill=BROWN, outline=BLACK)  # Left arm
    draw.rectangle([24, 18, 28, 30], fill=BROWN, outline=BLACK)  # Right arm
    
    # Staff (in right hand)
    draw.rectangle([26, 12, 28, 32], fill=DARK_BROWN, outline=BLACK)
    
    # Legs
    draw.rectangle([10, 35, 14, 46], fill=BROWN, outline=BLACK)  # Left leg
    draw.rectangle([18, 35, 22, 46], fill=BROWN, outline=BLACK)  # Right leg
    
    # Feet
    draw.ellipse([8, 44, 16, 48], fill=BLACK)  # Left foot
    draw.ellipse([16, 44, 24, 48], fill=BLACK)  # Right foot
    
    moses_idle.save("assets/sprites/player/moses_idle.png")
    
    # Moses walking sprites (simple animation frames)
    for i in range(4):
        moses_walk = moses_idle.copy()
        # Add slight variations for walking animation
        moses_walk.save(f"assets/sprites/player/moses_walk_{i}.png")
    
    # Moses jumping sprite
    moses_jump = moses_idle.copy()
    moses_jump.save("assets/sprites/player/moses_jump.png")

def create_npc_sprites():
    """Create NPC sprites"""
    print("Creating NPC sprites...")
    
    # Palace Guard
    guard = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(guard)
    
    # Head
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Helmet
    draw.ellipse([8, 0, 24, 12], fill=GRAY, outline=BLACK)
    
    # Body (armor)
    draw.rectangle([8, 14, 24, 35], fill=GRAY, outline=BLACK)
    
    # Arms
    draw.rectangle([4, 18, 8, 30], fill=GRAY, outline=BLACK)
    draw.rectangle([24, 18, 28, 30], fill=GRAY, outline=BLACK)
    
    # Spear
    draw.rectangle([26, 8, 28, 28], fill=BROWN, outline=BLACK)
    draw.polygon([(26, 8), (28, 8), (27, 4)], fill=GRAY, outline=BLACK)
    
    # Legs
    draw.rectangle([10, 35, 14, 46], fill=GRAY, outline=BLACK)
    draw.rectangle([18, 35, 22, 46], fill=GRAY, outline=BLACK)
    
    # Feet
    draw.ellipse([8, 44, 16, 48], fill=BLACK)
    draw.ellipse([16, 44, 24, 48], fill=BLACK)
    
    guard.save("assets/sprites/npcs/palace_guard.png")
    
    # Egyptian Citizen
    citizen = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(citizen)
    
    # Head
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Hair
    draw.ellipse([8, 0, 24, 10], fill=BLACK, outline=BLACK)
    
    # Body (simple tunic)
    draw.rectangle([8, 14, 24, 35], fill=WHITE, outline=BLACK)
    
    # Arms
    draw.rectangle([4, 18, 8, 30], fill=BEIGE, outline=BLACK)
    draw.rectangle([24, 18, 28, 30], fill=BEIGE, outline=BLACK)
    
    # Legs
    draw.rectangle([10, 35, 14, 46], fill=WHITE, outline=BLACK)
    draw.rectangle([18, 35, 22, 46], fill=WHITE, outline=BLACK)
    
    # Feet
    draw.ellipse([8, 44, 16, 48], fill=BROWN)
    draw.ellipse([16, 44, 24, 48], fill=BROWN)
    
    citizen.save("assets/sprites/npcs/egyptian_citizen.png")
    
    # Hebrew Slave
    slave = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(slave)
    
    # Head
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Hair
    draw.ellipse([8, 0, 24, 10], fill=DARK_BROWN, outline=BLACK)
    
    # Body (torn/simple clothing)
    draw.rectangle([8, 14, 24, 35], fill=BROWN, outline=BLACK)
    
    # Arms
    draw.rectangle([4, 18, 8, 30], fill=BEIGE, outline=BLACK)
    draw.rectangle([24, 18, 28, 30], fill=BEIGE, outline=BLACK)
    
    # Legs
    draw.rectangle([10, 35, 14, 46], fill=BROWN, outline=BLACK)
    draw.rectangle([18, 35, 22, 46], fill=BROWN, outline=BLACK)
    
    # Feet (bare)
    draw.ellipse([8, 44, 16, 48], fill=BEIGE)
    draw.ellipse([16, 44, 24, 48], fill=BEIGE)
    
    slave.save("assets/sprites/npcs/hebrew_slave.png")
    
    # Priest
    priest = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(priest)
    
    # Head
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Beard
    draw.ellipse([8, 10, 24, 18], fill=WHITE, outline=BLACK)
    
    # Body (white robes)
    draw.rectangle([6, 14, 26, 35], fill=WHITE, outline=BLACK)
    
    # Arms
    draw.rectangle([2, 18, 6, 30], fill=WHITE, outline=BLACK)
    draw.rectangle([26, 18, 30, 30], fill=WHITE, outline=BLACK)
    
    # Legs
    draw.rectangle([8, 35, 12, 46], fill=WHITE, outline=BLACK)
    draw.rectangle([20, 35, 24, 46], fill=WHITE, outline=BLACK)
    
    # Feet
    draw.ellipse([6, 44, 14, 48], fill=BROWN)
    draw.ellipse([18, 44, 26, 48], fill=BROWN)
    
    priest.save("assets/sprites/npcs/priest.png")

def create_item_sprites():
    """Create item sprites"""
    print("Creating item sprites...")
    
    # Stone
    stone = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stone)
    draw.ellipse([2, 2, 22, 22], fill=GRAY, outline=BLACK)
    draw.ellipse([4, 4, 12, 12], fill=LIGHT_GRAY)  # Highlight
    stone.save("assets/items/stone.png")
    
    # Meat
    meat = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(meat)
    draw.ellipse([2, 6, 22, 18], fill=BROWN, outline=BLACK)
    draw.ellipse([4, 8, 20, 16], fill=DARK_BROWN)
    meat.save("assets/items/meat.png")
    
    # Water
    water = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(water)
    # Water jug
    draw.ellipse([6, 4, 18, 16], fill=BROWN, outline=BLACK)
    draw.rectangle([8, 16, 16, 20], fill=BROWN, outline=BLACK)
    draw.ellipse([10, 6, 14, 10], fill=BLUE)  # Water
    water.save("assets/items/water.png")
    
    # Armor of God
    armor = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(armor)
    # Shield shape
    draw.polygon([(12, 2), (4, 8), (4, 18), (12, 22), (20, 18), (20, 8)], fill=GOLD, outline=BLACK)
    draw.polygon([(12, 4), (6, 9), (6, 17), (12, 20), (18, 17), (18, 9)], fill=YELLOW)
    armor.save("assets/items/armor_of_god.png")
    
    # Staff of Moses
    staff = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(staff)
    draw.rectangle([11, 2, 13, 22], fill=BROWN, outline=BLACK)
    draw.ellipse([9, 2, 15, 8], fill=GOLD, outline=BLACK)  # Golden top
    staff.save("assets/items/staff.png")
    
    # Bread
    bread = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(bread)
    draw.ellipse([2, 8, 22, 16], fill=BEIGE, outline=BLACK)
    draw.ellipse([4, 10, 20, 14], fill=(210, 180, 140))
    bread.save("assets/items/bread.png")
    
    # Scroll
    scroll = Image.new('RGBA', (24, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scroll)
    draw.rectangle([4, 6, 20, 18], fill=BEIGE, outline=BLACK)
    draw.rectangle([2, 6, 4, 18], fill=BROWN, outline=BLACK)  # Rod
    draw.rectangle([20, 6, 22, 18], fill=BROWN, outline=BLACK)  # Rod
    scroll.save("assets/items/scroll.png")

def create_background_tiles():
    """Create background and tile sprites"""
    print("Creating background tiles...")
    
    # Palace wall tile
    palace_wall = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(palace_wall)
    draw.rectangle([0, 0, 32, 32], fill=(200, 180, 140), outline=BLACK)
    # Stone pattern
    draw.rectangle([0, 0, 16, 16], fill=(220, 200, 160), outline=BLACK)
    draw.rectangle([16, 16, 32, 32], fill=(220, 200, 160), outline=BLACK)
    palace_wall.save("assets/tiles/palace_wall.png")
    
    # Ground tile
    ground = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(ground)
    draw.rectangle([0, 0, 32, 32], fill=BROWN, outline=DARK_BROWN)
    # Add some texture
    for i in range(0, 32, 4):
        for j in range(0, 32, 4):
            if (i + j) % 8 == 0:
                draw.rectangle([i, j, i+2, j+2], fill=DARK_BROWN)
    ground.save("assets/tiles/ground.png")
    
    # Desert sand tile
    sand = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sand)
    draw.rectangle([0, 0, 32, 32], fill=SAND, outline=(174, 158, 108))
    # Sand texture
    for i in range(0, 32, 3):
        for j in range(0, 32, 3):
            if (i * j) % 7 == 0:
                draw.ellipse([i, j, i+1, j+1], fill=(184, 168, 118))
    sand.save("assets/tiles/sand.png")
    
    # Water tile
    water_tile = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(water_tile)
    draw.rectangle([0, 0, 32, 32], fill=BLUE, outline=DARK_BLUE)
    # Water waves
    for i in range(0, 32, 8):
        draw.arc([i-4, 8, i+12, 24], 0, 180, fill=LIGHT_GRAY)
    water_tile.save("assets/tiles/water.png")
    
    # Stone platform
    stone_platform = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(stone_platform)
    draw.rectangle([0, 0, 32, 32], fill=GRAY, outline=BLACK)
    draw.rectangle([2, 2, 30, 30], fill=LIGHT_GRAY, outline=BLACK)
    stone_platform.save("assets/tiles/stone_platform.png")

def create_ui_elements():
    """Create UI elements"""
    print("Creating UI elements...")
    
    # Health bar background
    health_bg = Image.new('RGBA', (100, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(health_bg)
    draw.rectangle([0, 0, 100, 20], fill=BLACK, outline=WHITE, width=2)
    health_bg.save("assets/ui/health_bar_bg.png")
    
    # Health bar fill
    health_fill = Image.new('RGBA', (96, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(health_fill)
    draw.rectangle([0, 0, 96, 16], fill=RED)
    health_fill.save("assets/ui/health_bar_fill.png")
    
    # Dialogue box
    dialogue_box = Image.new('RGBA', (400, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dialogue_box)
    draw.rectangle([0, 0, 400, 100], fill=BLACK, outline=WHITE, width=3)
    draw.rectangle([3, 3, 397, 97], fill=(40, 40, 40))
    dialogue_box.save("assets/ui/dialogue_box.png")
    
    # Inventory slot
    inv_slot = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(inv_slot)
    draw.rectangle([0, 0, 40, 40], fill=(60, 60, 60), outline=WHITE, width=2)
    inv_slot.save("assets/ui/inventory_slot.png")
    
    # Button
    button = Image.new('RGBA', (120, 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(button)
    draw.rectangle([0, 0, 120, 40], fill=BROWN, outline=WHITE, width=2)
    draw.rectangle([2, 2, 118, 38], fill=(160, 90, 40))
    button.save("assets/ui/button.png")

def create_enemy_sprites():
    """Create enemy sprites"""
    print("Creating enemy sprites...")
    
    # Egyptian Soldier
    soldier = Image.new('RGBA', (32, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(soldier)
    
    # Head
    draw.ellipse([10, 2, 22, 14], fill=BEIGE, outline=BLACK)
    
    # Helmet
    draw.ellipse([8, 0, 24, 12], fill=GOLD, outline=BLACK)
    
    # Body (armor)
    draw.rectangle([8, 14, 24, 35], fill=GOLD, outline=BLACK)
    
    # Arms
    draw.rectangle([4, 18, 8, 30], fill=GOLD, outline=BLACK)
    draw.rectangle([24, 18, 28, 30], fill=GOLD, outline=BLACK)
    
    # Sword
    draw.rectangle([26, 12, 28, 26], fill=GRAY, outline=BLACK)
    draw.rectangle([25, 10, 29, 14], fill=BROWN, outline=BLACK)  # Hilt
    
    # Legs
    draw.rectangle([10, 35, 14, 46], fill=GOLD, outline=BLACK)
    draw.rectangle([18, 35, 22, 46], fill=GOLD, outline=BLACK)
    
    # Feet
    draw.ellipse([8, 44, 16, 48], fill=BLACK)
    draw.ellipse([16, 44, 24, 48], fill=BLACK)
    
    soldier.save("assets/sprites/enemies/egyptian_soldier.png")
    
    # Wild Animal (for wilderness)
    animal = Image.new('RGBA', (32, 24), (0, 0, 0, 0))
    draw = ImageDraw.Draw(animal)
    
    # Body
    draw.ellipse([4, 8, 28, 20], fill=BROWN, outline=BLACK)
    
    # Head
    draw.ellipse([24, 4, 32, 12], fill=BROWN, outline=BLACK)
    
    # Legs
    draw.rectangle([6, 18, 8, 24], fill=BROWN, outline=BLACK)
    draw.rectangle([12, 18, 14, 24], fill=BROWN, outline=BLACK)
    draw.rectangle([18, 18, 20, 24], fill=BROWN, outline=BLACK)
    draw.rectangle([24, 18, 26, 24], fill=BROWN, outline=BLACK)
    
    # Tail
    draw.ellipse([0, 10, 6, 14], fill=BROWN, outline=BLACK)
    
    animal.save("assets/sprites/enemies/wild_animal.png")

def create_effect_sprites():
    """Create special effect sprites"""
    print("Creating effect sprites...")
    
    # Dust cloud (for jumping/landing)
    dust = Image.new('RGBA', (24, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dust)
    for i in range(3):
        x = i * 8
        draw.ellipse([x, 8, x+8, 16], fill=(200, 180, 140, 128), outline=(150, 130, 90))
    dust.save("assets/sprites/effects/dust_cloud.png")
    
    # Sparkle (for item collection)
    sparkle = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sparkle)
    draw.polygon([(8, 0), (10, 6), (16, 8), (10, 10), (8, 16), (6, 10), (0, 8), (6, 6)], fill=YELLOW, outline=GOLD)
    sparkle.save("assets/sprites/effects/sparkle.png")
    
    # Divine light (for special moments)
    light = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    draw = ImageDraw.Draw(light)
    # Radiating light effect
    for i in range(5):
        alpha = 255 - (i * 40)
        size = 8 + (i * 8)
        x = 24 - size//2
        y = 24 - size//2
        draw.ellipse([x, y, x+size, y+size], fill=(255, 255, 255, alpha))
    light.save("assets/sprites/effects/divine_light.png")

def create_location_backgrounds():
    """Create background images for different locations"""
    print("Creating location backgrounds...")
    
    # Palace background
    palace_bg = Image.new('RGB', (800, 600), (180, 160, 120))
    draw = ImageDraw.Draw(palace_bg)
    
    # Palace pillars
    for x in range(100, 700, 150):
        draw.rectangle([x, 100, x+30, 500], fill=(200, 180, 140), outline=BLACK, width=2)
        draw.ellipse([x-10, 90, x+40, 120], fill=(220, 200, 160), outline=BLACK, width=2)
    
    # Floor
    draw.rectangle([0, 500, 800, 600], fill=(160, 140, 100), outline=BLACK, width=2)
    
    palace_bg.save("assets/backgrounds/palace.png")
    
    # Desert background
    desert_bg = Image.new('RGB', (800, 600), SAND)
    draw = ImageDraw.Draw(desert_bg)
    
    # Sand dunes
    for i in range(3):
        y = 300 + i * 50
        draw.ellipse([i*200, y, i*200+300, y+100], fill=(184, 168, 118))
    
    # Sun
    draw.ellipse([650, 50, 750, 150], fill=YELLOW, outline=ORANGE, width=3)
    
    desert_bg.save("assets/backgrounds/desert.png")
    
    # Red Sea background
    sea_bg = Image.new('RGB', (800, 600), BLUE)
    draw = ImageDraw.Draw(sea_bg)
    
    # Waves
    for y in range(400, 600, 20):
        for x in range(0, 800, 40):
            draw.arc([x, y, x+40, y+20], 0, 180, fill=WHITE, width=2)
    
    # Shore
    draw.ellipse([-100, 500, 200, 700], fill=SAND)
    draw.ellipse([600, 500, 900, 700], fill=SAND)
    
    sea_bg.save("assets/backgrounds/red_sea.png")

def main():
    """Main function to create all sprites"""
    print("Starting sprite generation for Moses Adventure...")
    
    create_directory_structure()
    create_player_sprites()
    create_npc_sprites()
    create_item_sprites()
    create_background_tiles()
    create_ui_elements()
    create_enemy_sprites()
    create_effect_sprites()
    create_location_backgrounds()
    
    print("\n✅ All sprites created successfully!")
    print("\nGenerated assets:")
    print("📁 Player sprites (Moses in different poses)")
    print("📁 NPC sprites (Guards, Citizens, Priests, Slaves)")
    print("📁 Item sprites (Stone, Meat, Water, Armor of God, etc.)")
    print("📁 Background tiles (Palace walls, Ground, Sand, Water)")
    print("📁 UI elements (Health bars, Dialogue boxes, Buttons)")
    print("📁 Enemy sprites (Egyptian soldiers, Wild animals)")
    print("📁 Effect sprites (Dust clouds, Sparkles, Divine light)")
    print("📁 Location backgrounds (Palace, Desert, Red Sea)")
    print("\nYou can now run your Moses Adventure game!")
    print("To improve the sprites later, you can:")
    print("- Replace with hand-drawn artwork")
    print("- Add more animation frames")
    print("- Create more detailed textures")
    print("- Add transparency effects")

if __name__ == "__main__":
    main()
