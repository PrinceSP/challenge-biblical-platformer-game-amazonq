# Moses Adventure - Game Systems Guide

## 🔧 Fixed Issues

### ✅ Issue 1: Healing Items Not Increasing Health
**Problem**: Items like meat, water, and bread were being used but health wasn't increasing.

**Root Cause**: The game uses a **two-step healing system** by design:
1. **Step 1**: Use item from inventory (prepares healing)
2. **Step 2**: Press H key to apply healing

**Solution Applied**:
- Enhanced user feedback with clear instructions
- Added blinking visual indicators
- Improved console messages with tips
- Added full health check to prevent waste

### ✅ Issue 2: Stone Throwing Not Working
**Problem**: When using stone from inventory, pressing A to attack enemies didn't work.

**Root Cause**: Stone throwing required both `stone_throw_mode` AND `player.can_attack` to be true. The attack cooldown was preventing stone throws.

**Solution Applied**:
- Removed `can_attack` requirement for inventory-based stone throwing
- Enhanced UI with debug information
- Added better visual feedback
- Improved instructions and tips

---

## 🎮 How to Use Game Systems

### 💊 Healing System

#### Step-by-Step Process:
1. **Collect Healing Items**
   - 🥩 Meat: +10 health
   - 🍞 Bread: +5 health  
   - 💧 Water: +1 health

2. **Open Inventory**
   - Press `I` key to open inventory

3. **Select Healing Item**
   - Press number keys (1-9) for item position
   - Example: Press `1` if meat is in first slot

4. **Prepare Healing**
   - Item is consumed and healing is prepared
   - You'll see: "🩹 HEALING READY! Press H to heal +X"
   - Green blinking indicator appears on screen

5. **Apply Healing**
   - Press `H` key to restore health
   - Health increases immediately
   - Healing state is cleared

#### Important Notes:
- Items are consumed when prepared (Step 4), not when applied (Step 5)
- You can only have one healing prepared at a time
- If already at full health, healing is still consumed but no effect
- Visual feedback shows current/max health

### 🪨 Stone Throwing System

#### Step-by-Step Process:
1. **Collect Stones**
   - Find stone items in the game world
   - Each stone is single-use

2. **Open Inventory**
   - Press `I` key to open inventory

3. **Select Stone**
   - Press number keys (1-9) for stone position
   - Stone is consumed immediately

4. **Stone Throw Mode Activated**
   - You'll see: "🎯 STONE READY! Press A to throw!"
   - Yellow indicator appears on screen
   - Debug info shows attack status

5. **Throw Stone**
   - Press `A` key to throw stone
   - Stone projectile is created
   - Flies in direction Moses is facing
   - Can hit and damage enemies

6. **Cancel (Optional)**
   - Press `ESC` to cancel stone throw mode
   - No stone is wasted

#### Important Notes:
- Stones have physics (arc trajectory, gravity)
- Each stone does 15 damage to enemies
- No attack cooldown for inventory stones
- Stone disappears after 3 seconds or hitting ground

---

## 🎯 Controls Summary

### Basic Movement
- **Arrow Keys**: Move Moses
- **Space**: Jump
- **E**: Interact with NPCs

### Inventory & Items
- **I**: Open/Close Inventory
- **1-9**: Use item in inventory slot
- **H**: Apply prepared healing
- **A**: Throw prepared stone

### Combat
- **A**: Throw stone (when stone is ready)
- **ESC**: Cancel stone throw mode

### System Controls
- **M**: Toggle Music
- **S**: Toggle Sound Effects
- **ESC**: Pause Game
- **F1**: Show FPS
- **F11**: Toggle Fullscreen

---

## 🧪 Testing the Fixes

### Test Healing System:
```bash
python3 test_healing_system.py
```

### Test Stone System:
```bash
python3 test_inventory_stones.py
```

### Test All Fixes:
```bash
python3 test_fixes_applied.py
```

### Play the Game:
```bash
python3 main.py
```

---

## 🐛 Troubleshooting

### Healing Not Working?
1. Check if you have healing items in inventory (Press I)
2. Make sure you pressed number key to prepare healing
3. Look for "HEALING READY" message on screen
4. Press H key to apply healing
5. Check console for detailed messages

### Stone Throwing Not Working?
1. Check if you have stones in inventory (Press I)
2. Make sure you pressed number key to prepare stone
3. Look for "STONE READY" message on screen
4. Press A key to throw stone
5. Make sure you're facing the right direction
6. Check debug info showing "Can attack: True/False"

### General Issues:
1. Make sure pygame is installed: `pip install pygame`
2. Check console output for error messages
3. Verify all game files are present
4. Try restarting the game

---

## 📋 System Status

### ✅ Working Systems:
- Two-step healing system
- Inventory-based stone throwing
- Visual feedback and UI
- Sound effects and music
- NPC interactions
- Level progression
- Combat with enemies

### 🔧 Enhanced Features:
- Better user feedback
- Clear instructions
- Visual indicators
- Debug information
- Error handling
- Full health checks

---

## 🎨 Visual Indicators

### Healing Ready:
- 🩹 Green text: "HEALING READY! Press H to heal +X"
- Blinking green background
- Console tip messages

### Stone Ready:
- 🎯 Yellow text: "STONE READY! Press A to throw"
- Debug info showing attack status
- Console tip messages

### Health Display:
- Health bar in top-left corner
- Text showing current/max health
- Visual feedback on healing

---

This guide should help you understand and use both the healing and stone throwing systems effectively!
