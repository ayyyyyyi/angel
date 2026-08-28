"""把新背景升采样到 2752x1536 并覆盖 layer-bg.png，让 HTML 直接生效。"""
from pathlib import Path
from PIL import Image

ROOT = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax")
SRC  = Path(r"C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-28T02-50-45-392Z-2d642642.jpg")

# 1. 原版小图也保存一份留档
raw_dst = ROOT / "layer-bg-newsnow.jpg"
Image.open(SRC).convert("RGB").save(raw_dst, quality=92)
print(f"原版小图留档: {raw_dst.name}  ({raw_dst.stat().st_size/1024:.0f} KB)")

# 2. 升采样到 2752x1536 覆盖 layer-bg.png
big = Image.open(SRC).convert("RGB").resize((2752, 1536), Image.LANCZOS)
bg_dst = ROOT / "layer-bg.png"
big.save(bg_dst, optimize=True)
print(f"覆盖 layer-bg.png: {bg_dst.name}  尺寸 {big.size}  ({bg_dst.stat().st_size/1024/1024:.1f} MB)")

# 3. 列出最终三图
print("\n=== 最终三层文件 ===")
for name in ["layer-bg.png", "layer-bg-newsnow.jpg", "layer-angel.png", "layer-pillar.png",
             "layer-bg-cutout.png"]:
    p = ROOT / name
    if p.exists():
        print(f"  {name:30s}  {p.stat().st_size/1024/1024:5.1f} MB")
    else:
        print(f"  {name} (不存在)")
