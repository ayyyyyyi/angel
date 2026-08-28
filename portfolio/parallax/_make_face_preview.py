from PIL import Image
from pathlib import Path

SRC = Path(r'C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax/layer-angel.png')
OUT = Path(r'C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax')

img = Image.open(SRC)
W, H = img.size  # 2752, 1536
print(f'src {W}x{H}')

vw, vh = 1920, 1080
render_w = vw
render_h = vw / (W / H)  # ~1071
y_offset = (vh - render_h) / 2  # ~4.5

ox_screen, oy_screen = vw * 0.5, vh * 0.38
ox_img = ox_screen * W / render_w
oy_img = (oy_screen - y_offset) * H / render_h
print(f'origin in img: ({ox_img:.0f}, {oy_img:.0f})')

s = 3
left_img = ox_img - ox_screen / s * W / render_w
right_img = ox_img + (vw - ox_screen) / s * W / render_w
top_img = oy_img - oy_screen / s * H / render_h
bot_img = oy_img + (vh - oy_screen) / s * H / render_h
print(f'screen 0..vw maps to img: x={left_img:.0f}..{right_img:.0f}, y={top_img:.0f}..{bot_img:.0f}')

box = (max(0, int(left_img)), max(0, int(top_img)), min(W, int(right_img)), min(H, int(bot_img)))
print(f'crop box: {box}')
cropped = img.crop(box)
result = cropped.resize((vw, vh), Image.LANCZOS)
result.save(OUT / 'face-preview.png', quality=95)
print('saved face-preview.png')
