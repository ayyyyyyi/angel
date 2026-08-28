"""把白底神像图（png）抠成透明 PNG，缩到与 layer-bg 一致。
白底判定：R,G,B 都 >235 且色差 max-min<10（避免误伤金色翅膀）"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import shutil

src = Path(r"C:/Users/ayiqianwang/Desktop/新建文件夹/1787888856967622.png")
dst_dir = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax")

# 1) 备份当前 layer-angel.png（暖橙展翅天使，作为 layer-angel-warm.png）
old = dst_dir / "layer-angel.png"
backup = dst_dir / "layer-angel-warm.png"
if old.exists() and not backup.exists():
    shutil.copy2(old, backup)
    print(f"[backup] {old.name} -> {backup.name}")

# 2) 读图（PNG 可能是 RGB 或 RGBA，统一先转 RGBA 保留透明）
img = Image.open(src)
print(f"[raw] {src.name} size={img.size} mode={img.mode}")
if img.mode != "RGBA":
    img = img.convert("RGBA")

# 已经是 RGBA 但底子不是白，可能之前已抠过？确认一下
# 看像素 [0,0]
pix00 = img.getpixel((0, 0))
print(f"[pix 0,0] = {pix00}")

# 3) 升采样到 2752x1536（与背景同尺寸）
target = (2752, 1536)
up = img.resize(target, Image.LANCZOS)
arr_rgba = np.array(up)
rgb = arr_rgba[:, :, :3]
H, W, _ = rgb.shape

# 4) 白底抠图判定
#   RGB 三通道都 > 235
#   且 max-min < 10（避免误伤金色翅膀——金色 B 通道低）
#   alpha = 0（透明），else alpha = 255
r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
max_ch = np.max(rgb, axis=2)
min_ch = np.min(rgb, axis=2)
chroma = max_ch - min_ch  # 色彩饱和度代理指标

white_bg = (r > 235) & (g > 235) & (b > 235) & (chroma < 10)

alpha = np.where(white_bg, 0, 255).astype(np.uint8)

# 5) 羽化 alpha 边界
alpha_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=1.5))
alpha = np.array(alpha_img).astype(np.uint8)

opaque_pct = (alpha > 30).sum() / alpha.size * 100
print(f"[alpha stats] opaque pixels {opaque_pct:.2f}%")

# 6) 重新拼 RGBA
rgba = np.dstack([rgb, alpha])
out_img = Image.fromarray(rgba, mode="RGBA")

out_path = dst_dir / "layer-angel.png"
out_img.save(out_path, optimize=True)
print(f"[save] {out_path}  ({out_path.stat().st_size / 1024 / 1024:.2f} MB)")
