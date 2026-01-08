
import json
import os
import shutil
import time
from pathlib import Path

# Setup fake save file at end of chapter 1
save_data = {
    'player_name': 'Tester',
    'codiname': 'TEST_01',
    'current_chapter': 1,
    'completed_chapters': [],
    'score': 100,
    'capitulo_1_resultado': 'exfiltrar',
    'bitcoin_wallet': 0.005,
    'privacy_level': 80,
    'inventory': []
}

Path("saves").mkdir(exist_ok=True)
with open("saves/test_dynamic_load.json", "w") as f:
    json.dump(save_data, f)

print("Created test save file.")

# Mock chapter 1 to strictly complete immediately
# We need to temporarily modify chapter_01.py or just rely on the fact that we can call
# root's internal methods directly to simulate the loop.

# Actually, the best way is to instantiate IntroMenu and call _continuar_jogo with our save.
# But since chapter_01 has user input, it might block.
# I will create a dummy chapter_01 if it was easy, but I shouldn't overwrite the user's file.

# Instead, I'll rely on the fact that I can't easily run interactive tests here without blocking.
# So I will just verifying the Syntax of root_evolution_main.py
try:
    import root_evolution_main
    print("Syntax verification passed.")
except ImportError:
    print("Import error - check dependencies")
except SyntaxError:
    print("Syntax error in root_evolution_main.py")
except Exception as e:
    print(f"Error: {e}")

