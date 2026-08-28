"""用新背景(雪山湖面) + 之前的石柱/神像抠图层，合成看效果。
新背景升采样到 2752x1536 让前景按原位置贴。
"""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax")
SRC  = Path(r"C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-28T02-50-45-392Z-2d642642.jpg")

bg_src = SRC
pillar_src = ROOT / "layer-pillar.png"
angel_src  = ROOT / "layer-angel.png"

TARGET = (2752, 1536)  # 和旧图层对齐

print(f"读取新背景并升采样到 {TARGET} …")
bg = Image.open(bg_src).convert("RGB").resize(TARGET, Image.LANCZOS)
pillar = Image.open(pillar_src).convert("RGBA")
angel  = Image.open(angel_src).convert("RGBA")

# 同步缩放前景到目标尺寸（保持位置一致）
pillar_resized = pillar.resize(TARGET, Image.LANCZOS)
angel_resized  = angel.resize(TARGET, Image.LANCZOS)

# 顺序：背景 < 神像 < 石柱（神像在中间层，柱子在最前）
# 让石柱在神像前面 => 柱廊从画面两侧伸出来可以挡住神像
print("合成：背景 < 神像 < 石柱")
canvas = bg.copy()
canvas.paste(angel_resized,  (0, 0), angel_resized)
canvas.paste(pillar_resized, (0, 0), pillar_resized)

out = ROOT / "layers-preview.png"
canvas.save(out, optimize=True)
print(f"合成图: {out.name}  尺寸 {canvas.size}  大小 {out.stat().st_size/1024/1024:.1f} MB")
print(f"背景源文件: {bg_src.name}  ({Path(bg_src).stat().st_size/1024/1024:.1f} MB)")
