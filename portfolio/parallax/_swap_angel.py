"""把新神像图（jpg，黑底）抠成透明 PNG，缩到与 layer-bg 一致"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

src = Path(r"C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-28T03-49-19-031Z-de06f185.jpg")
dst_dir = Path(r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax")

# 1) 备份旧版（万一想回滚）
old = dst_dir / "layer-angel.png"
backup = dst_dir / "layer-angel-old.png"
if old.exists() and not backup.exists():
    import shutil
    shutil.copy2(old, backup)
    print(f"[backup] {old.name} -> {backup.name}")

# 2) 读图（jpg RGB）
img = Image.open(src).convert("RGB")
print(f"[raw] {src.name} size={img.size} mode=RGB")

# 3) 升采样到 2752x1536（与背景同尺寸）
target = (2752, 1536)
up = img.resize(target, Image.LANCZOS)
print(f"[upscale] -> {target}")

arr = np.array(up)  # H, W, 3

# 4) 黑色背景抠图：RGB 三通道都 < 阈值 -> alpha=0
#    主体是暖橙白，背景是纯黑，差距非常大，阈值 25 就够了
#    但阈值的边界会有一圈灰色，我们用平滑过渡避免硬边
threshold = 25
near_black = (arr[:, :, 0] < threshold) & (arr[:, :, 1] < threshold) & (arr[:, :, 2] < threshold)

alpha = np.where(near_black, 0, 255).astype(np.uint8)

# 5) alpha 做轻微羽化（边界平滑），避免硬边
#    用 PIL 的 GaussianBlur 把 alpha 当灰度图模糊，再二值化即可
alpha_img = Image.fromarray(alpha, mode="L").filter(ImageFilter.GaussianBlur(radius=1.2))
alpha_arr = np.array(alpha_img)
# 模糊后再清理一次：>200 视为实体，<30 视为背景，中间留过渡
alpha_final = np.clip(alpha_arr, 0, 255).astype(np.uint8)

# 6) 合成 RGBA
rgba = np.dstack([arr, alpha_final])
out_img = Image.fromarray(rgba, mode="RGBA")
print(f"[alpha stats] opaque pixels {(alpha_final > 30).sum() / alpha_final.size * 100:.2f}%")

# 7) 存为 PNG 替换 layer-angel.png
out_path = dst_dir / "layer-angel.png"
out_img.save(out_path, optimize=True)
print(f"[save] {out_path}  ({out_path.stat().st_size / 1024 / 1024:.2f} MB)")
