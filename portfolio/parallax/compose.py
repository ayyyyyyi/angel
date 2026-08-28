# -*- coding: utf-8 -*-
"""
把三张抠图按 z-index 叠成一张，验证「石柱（柱廊）穿越神像」的前后关系。

层级（从下到上）：
  1. 背景（没有石柱和神像的背景）
  2. 神像（中央天使）
  3. 石柱（前景柱廊）—— 应该在最上层，能遮住神像一部分

输出：
  - portfolio/parallax/layers-preview.png  合成结果（直接看效果）
  - portfolio/parallax/layers-mask.png     三张图各自的 alpha mask 缩略图（看抠图质量）
"""
from pathlib import Path
from PIL import Image
import numpy as np

ROOT = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding")
OUT = ROOT / "portfolio" / "parallax"

bg_src = OUT / "layer-bg.png"        # 完整原图（阿意指定）
pillar_src = OUT / "layer-pillar.png" # 抠出来的柱廊
angel_src = OUT / "layer-angel.png"   # 抠出来的天使

bg = Image.open(bg_src).convert("RGBA")
pillar = Image.open(pillar_src).convert("RGBA")
angel = Image.open(angel_src).convert("RGBA")

print(f"背景    : {bg.size}   mode={bg.mode}")
print(f"石柱    : {pillar.size} mode={pillar.mode}")
print(f"神像    : {angel.size} mode={angel.mode}")

# 尺寸必须一致才能对齐
assert bg.size == pillar.size == angel.size, "三张图尺寸不一致！需要 resize 对齐"
W, H = bg.size

# 合成：背景 -> 神像 -> 石柱（石柱在最上层，能挡住神像）
canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
canvas.alpha_composite(bg)        # 底层
canvas.alpha_composite(angel)     # 中层
canvas.alpha_composite(pillar)    # 顶层：石柱在最前，能遮住神像

canvas.convert("RGB").save(OUT / "layers-preview.png", optimize=True)
print(f"\n合成图已保存: {OUT / 'layers-preview.png'}")

# 顺手做一张 alpha mask 缩略图，方便看每张图抠得有多"干净"
# 黑色 = 透明，白色 = 不透明
def mask_preview(img_rgba: Image.Image, name: str, max_w: int = 800) -> None:
    a = np.array(img_rgba)
    alpha = a[:, :, 3]
    h, w = alpha.shape
    # 等比缩到 max_w 宽
    scale = max_w / w
    new_size = (max_w, int(h * scale))
    mask = Image.fromarray(alpha).convert("L").resize(new_size, Image.LANCZOS)
    mask.save(OUT / f"_mask_{name}.png")
    # 顺便打印不透明像素占比（粗看抠图干净度）
    opaque = (alpha > 30).sum() / alpha.size * 100
    print(f"  {name}: 不透明像素 {opaque:.2f}%")

print("\n各层 alpha mask 缩略图：")
mask_preview(bg, "背景")
mask_preview(pillar, "石柱")
mask_preview(angel, "神像")
print(f"\n全部输出在: {OUT}")