# Moses Adventure - Biblical Platformer Game

A classic platformer-style adventure game featuring Moses' journey from Egypt to Jerusalem, based on biblical narratives.

## Features

### ✅ Implemented Features
- **Classic Platformer Mechanics**: Arrow key movement, jumping, gravity physics
- **Biblical Character**: Play as Moses with custom sprites and animations
- **Epic Journey**: Travel from Pharaoh's palace in Egypt to the Promised Land in Jerusalem
- **Multiple Locations**: Palace, Egypt City, Desert, Red Sea, Wilderness, Mount Sinai, Jerusalem
- **Inventory System**: Collect biblical items (stones, meat, water, armor of God, staff, bread, scrolls)
- **Realistic Collision Detection**: Physics-based platform interactions with visual effects
- **Visual Feedback System**: Particle effects, item collection animations, damage indicators
- **60 FPS Performance**: Optimized game loop with delta time calculations
- **Dialogue System**: Interactive conversations with NPCs, biblical storytelling
- **Moral Choice System**: Decisions affect your moral standing (Righteous, Good, Neutral, Wayward, Corrupt)
- **Sound Effects**: Audio feedback for actions (with visual alternatives when disabled)
- **Background Music**: Ancient/Middle Eastern style music system
- **Multiple NPCs**: Palace guards, Egyptian citizens, Hebrew slaves, priests
- **Enemies**: Egyptian soldiers, wild animals with AI behavior
- **Accessibility**: Visual feedback when audio is disabled
- **Full UI System**: Health bars, inventory interface, dialogue boxes

## Controls

- **Arrow Keys**: Move Moses left/right, jump up
- **E**: Interact with NPCs and objects
- **I**: Open/close inventory
- **ESC**: Pause game or return to menu
- **M**: Toggle background music
- **S**: Toggle sound effects
- **F1**: Show/hide FPS counter
- **F11**: Toggle fullscreen mode
- **1, 2, 3**: Choose dialogue options
- **SPACE/ENTER**: Continue dialogue, confirm actions

## Story & Locations

### 1. **Palace** (Starting Location)
- Escape from Pharaoh's palace
- Meet palace guards and Hebrew slaves
- Collect initial supplies

### 2. **Egypt City**
- Navigate through the bustling Egyptian city
- Encounter citizens and priests
- Avoid Egyptian soldiers

### 3. **Desert**
- Cross the harsh desert wilderness
- Find water and sustenance
- Meet other Hebrew refugees

### 4. **Red Sea**
- Witness the parting of the Red Sea
- Divine encounter with God's power
- Cross to freedom

### 5. **Wilderness**
- Journey through the wilderness
- Face wild animals and challenges
- Gather the people

### 6. **Mount Sinai**
- Climb the sacred mountain
- Receive divine guidance
- Prepare for the final journey

### 7. **Jerusalem** (Final Destination)
- Reach the Promised Land
- Complete Moses' mission
- Victory celebration

## Items & Inventory

- **Stone**: Smooth stones for David's sling
- **Meat**: Dried meat for sustenance
- **Water**: Fresh water from wells
- **Armor of God**: Divine protection
- **Staff**: Moses' staff of power
- **Bread**: Sustenance for the journey
- **Scroll**: Sacred scriptures and teachings

## Moral System

Your choices throughout the game affect Moses' moral standing:

- **Righteous**: Always choose faith and truth
- **Good**: Generally make positive choices
- **Neutral**: Balanced approach
- **Wayward**: Some questionable decisions
- **Corrupt**: Consistently poor choices

## Installation & Running

### Prerequisites
```bash
pip3 install pygame pillow numpy
```

### Running the Game
```bash
cd moses_adventure
python3 main.py
```

## File Structure

```
moses_adventure/
├── main.py              # Main game launcher
├── game_classes.py      # Player, NPCs, enemies, level management
├── game_systems.py      # Inventory, dialogue, sound, moral system
├── create_sprites.py    # Sprite generation utility
├── assets/
│   ├── sprites/
│   │   ├── player/      # Moses sprites
│   │   ├── npcs/        # NPC sprites
│   │   ├── enemies/     # Enemy sprites
│   │   └── effects/     # Visual effects
│   ├── items/           # Item sprites
│   ├── backgrounds/     # Location backgrounds
│   ├── tiles/           # Platform tiles
│   ├── ui/              # User interface elements
│   ├── music/           # Background music (placeholder)
│   └── sounds/          # Sound effects (placeholder)
└── README.md
```

## Technical Features

- **60 FPS Performance**: Optimized rendering and update loops
- **Delta Time Physics**: Smooth movement regardless of framerate
- **Collision Detection**: Realistic physics with proper collision resolution
- **Camera System**: Smooth following camera with bounds
- **Animation System**: Sprite-based character animations
- **Particle Effects**: Visual feedback for actions and events
- **State Management**: Clean game state transitions
- **Error Handling**: Graceful handling of missing assets
- **Accessibility**: Visual alternatives to audio cues

## Biblical Themes

The game incorporates authentic biblical themes and narratives:

- Moses' calling to deliver the Israelites
- The confrontation with Pharaoh's power
- The journey through the wilderness
- Divine encounters and guidance
- Moral choices reflecting biblical values
- The ultimate goal of reaching the Promised Land

## Future Enhancements

Potential improvements for the game:

- **Enhanced Graphics**: Hand-drawn artwork and animations
- **More Levels**: Additional biblical locations and events
- **Multiplayer**: Co-op mode for multiple biblical characters
- **Mini-Games**: Specific biblical challenges (parting the sea, etc.)
- **Voice Acting**: Narrated biblical stories
- **Music**: Original Middle Eastern/ancient music compositions
- **Achievements**: Biblical milestone tracking
- **Save System**: Progress saving and loading

## Credits

Created for the "Build Games Challenge: Build Classics with Amazon Q Developer CLI"

- **Game Engine**: Pygame
- **Graphics**: Procedurally generated sprites
- **Story**: Based on biblical narratives
- **Development**: Amazon Q Developer CLI assisted

## License

This game is created for educational and entertainment purposes, incorporating public domain biblical narratives.

---

**"And Moses said unto the people, Fear ye not, stand still, and see the salvation of the Lord."** - Exodus 14:13
