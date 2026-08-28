"""裁掉抠图顶部的拱门横梁 + 生成新预览图。"""
from PIL import Image
import numpy as np

SRC = 'parts/angel.png'
GREEN_PREV = 'parts/_preview_angel_green.png'
CHECKER_PREV = 'parts/_preview_angel_checker.png'

arr = np.array(Image.open(SRC).convert('RGBA'))
h, w = arr.shape[:2]
print(f'原图: {w}x{h}')

# 在裁切带内做线性羽化（参考顶部 row_count：y=0 处就有 585 个不透明像素=横梁）
y_solid = 250       # 完全裁掉
y_feather_end = 450 # 羽化结束点
for y in range(h):
    if y < y_solid:
        arr[y, :, 3] = 0
    elif y < y_feather_end:
        f = (y_feather_end - y) / (y_feather_end - y_solid)  # 1.0 → 0.0
        arr[y, :, 3] = (arr[y, :, 3].astype(float) * f).astype(np.uint8)

Image.fromarray(arr).save(SRC)
print(f'已裁顶部 y<{y_solid}+羽化到 y={y_feather_end}')

# 重新生成预览
img = Image.open(SRC).convert('RGBA')
i_w, i_h = img.size
W = 1400
H = int(W * i_h / i_w)
small = img.resize((W, H), Image.LANCZOS)

# 绿色底
bg_g = Image.new('RGBA', (W, H), (0, 200, 0, 255))
bg_g.paste(small, (0, 0), small)
bg_g.convert('RGB').save(GREEN_PREV)

# 棋盘底
cell = 40
checker = Image.new('RGBA', (W, H), (255, 255, 255, 255))
for yy in range(0, H, cell):
    for xx in range(0, W, cell):
        if (xx // cell + yy // cell) % 2 == 0:
            for dy in range(cell):
                for dx in range(cell):
                    if xx + dx < W and yy + dy < H:
                        checker.putpixel((xx + dx, yy + dy), (230, 230, 230, 255))
checker.paste(small, (0, 0), small)
checker.convert('RGB').save(CHECKER_PREV)
print('预览图已重新生成')
