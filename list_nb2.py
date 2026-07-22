import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

cwd = r'c:\Users\PC\Desktop\Du_An\project ADY201m\ADY mới nhất'
nb2_path = os.path.join(cwd, 'Code', '02_basic_model_training.ipynb')

with open(nb2_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    first_line = ''.join(cell['source']).strip().split('\n')[0][:80]
    print(f"Cell {i} ({cell['cell_type']}): {first_line}")
