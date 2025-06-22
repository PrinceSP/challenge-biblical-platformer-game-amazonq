#!/usr/bin/env python3
"""
Debug Enemy class import
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Importing game_classes...")
from game_classes import Enemy

print(f"Enemy class: {Enemy}")
print(f"Enemy.__init__ signature: {Enemy.__init__}")

import inspect
print(f"Enemy.__init__ parameters: {inspect.signature(Enemy.__init__)}")

# Try to create an enemy
try:
    enemy = Enemy(100, 100, "test", {})
    print(f"✅ Enemy created successfully: {enemy}")
except Exception as e:
    print(f"❌ Error creating enemy: {e}")
    import traceback
    traceback.print_exc()
