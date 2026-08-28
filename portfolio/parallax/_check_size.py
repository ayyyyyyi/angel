from PIL import Image
from pathlib import Path

bg_new = Path(r'C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-28T02-50-45-392Z-2d642642.jpg')
bg_old = Path(r'C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax/layer-bg.png')
pillar = Path(r'C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax/layer-pillar.png')
angel  = Path(r'C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax/layer-angel.png')

print('=== 各图尺寸和模式 ===')
print(f'新背景 jpg: {Image.open(bg_new).size}  mode={Image.open(bg_new).mode}')
print(f'旧背景 png: {Image.open(bg_old).size}  mode={Image.open(bg_old).mode}')
print(f'石柱 png:   {Image.open(pillar).size}  mode={Image.open(pillar).mode}')
print(f'神像 png:   {Image.open(angel).size}  mode={Image.open(angel).mode}')
