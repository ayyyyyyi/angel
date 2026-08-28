from PIL import Image
import numpy as np
from pathlib import Path

p = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax/layer-pillar.png")
im = Image.open(p).convert("RGBA")
a = np.array(im)[:, :, 3]  # alpha 通道
h, w = a.shape
print(f"石柱图尺寸: {w}x{h}")

# 每列有多少不透明像素
col_opaque = (a > 30).sum(axis=0)
# 每行有多少不透明像素
row_opaque = (a > 30).sum(axis=1)

# 找到中间"空白"列（不透明像素很少），作为左右柱廊的分界
# 打印每 50 列的不透明像素占比，粗看分布
print("\n=== 每 50 列的不透明像素数（宽=%d）===" % w)
for x in range(0, w, 50):
    seg = col_opaque[x:x+50]
    print(f"  x={x:4d}-{x+50:4d}: {seg.sum():6d}  (峰值 {seg.max()})")

# 找全局最空的连续区域（柱廊之间的缝）
# 用滑动窗口找不透明像素最少的 200 列窗口
best_start, best_sum = 0, 10**9
for x in range(0, w - 200, 10):
    s = col_opaque[x:x+200].sum()
    if s < best_sum:
        best_sum = s
        best_start = x
print(f"\n最空的 200 列窗口: x={best_start}~{best_start+200}, 不透明像素总和={best_sum}")
print(f"  建议左右分界点(中线): x={best_start+100}")
