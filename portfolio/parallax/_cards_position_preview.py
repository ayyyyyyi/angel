"""模拟卡片浮现后的页面：验证卡片新位置（baseY=-260）是否避让底部进度条/任务栏"""
from PIL import Image, ImageDraw, ImageFont
import os

SW, SH = 1920, 1080
BG = (8, 6, 4)               # 接近实际页面 background
canvas = Image.new('RGB', (SW, SH), BG)
draw = ImageDraw.Draw(canvas)

def get_font(size, bold=False):
    paths = [
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

# === 顶部导航 ===
nav_font = get_font(13, bold=False)
draw.text((40, 28), "AYI · 阿意", fill="white", font=nav_font)
draw.text((SW - 200, 28), "← 静态版   合成图", fill="white", font=nav_font)

# === 底部提示语（hint）—— 位于 screen bottom 24px
hint_font = get_font(11, bold=False)
hint = "滚轮当油门 · 按住鼠标上下拖也行  |  按 1 2 3 开关图层 · 0 全开"
hb = draw.textbbox((0, 0), hint, font=hint_font)[2]
draw.text(((SW - hb) // 2, SH - 24 - 11), hint, fill=(212, 176, 106), font=hint_font)

# === 进度条（bottom: 78px） ===
track_w = 420
track_x = (SW - track_w) // 2
track_y = SH - 78 - 4
draw.rectangle((track_x, track_y, track_x + track_w, track_y + 4), fill=(80, 80, 80))
draw.rectangle((track_x, track_y, track_x + int(track_w * 0.99), track_y + 4), fill=(212, 176, 106))
# 进度条上方文字
label_font = get_font(12, bold=False)
label = "贴脸 · 转场"
lb = draw.textbbox((0, 0), label, font=label_font)[2]
draw.text(((SW - lb) // 2, SH - 92 - 12), label, fill=(212, 176, 106), font=label_font)

# === 模拟任务栏（Windows 11 风格的底栏遮挡示意）===
# 透明灰色，让用户看到底栏大概在哪个位置
taskbar_h = 60
draw.rectangle((0, SH - taskbar_h, SW, SH), fill=(20, 20, 20))
# 加几个图标占位
for i in range(8):
    cx = 60 + i * 50
    cy = SH - taskbar_h // 2
    draw.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=(50, 50, 50))

# ====== 卡片横排 ======
CARD_W, CARD_H = 220, 290
GAP = 260
N = 5
center_x = SW // 2

# 关键：baseY = -260
# cards-stage 锚点在 (50%, bottom:0)，卡片中心 = (translateY) baseY = -260
# → 卡片中心 y = SH - 0 + (-260) = 820
baseY = -260
center_y = SH + baseY   # 屏幕底部锚点 + 向上偏移 260

card_beige = [
    (231, 212, 179),
    (218, 196, 163),
    (207, 184, 143),
]
text_dark = (43, 31, 18)
text_dark_soft = (78, 56, 38)
text_num = (58, 42, 26)

cards = [
    ("01", "项目案例", "游戏发行与数据增长全流程：达人筛选、创意内容到投放复盘。"),
    ("02", "内容创作", "视频 / 图文 / 文案多形态，紧跟平台热点借势。"),
    ("03", "实习经历", "FPS / 二次元 / 模拟经营多品类游戏的 KOL 运营实战。"),
    ("04", "数据复盘", "投放数据汇总与异常归因：盯着单位效率看，不盯总量。"),
    ("05", "达人招募", "KOL/KOC 多垂类筛选与对接，统筹渠道供应商资源。"),
]

for i, (num, title, desc) in enumerate(cards):
    idx = i - (N - 1) / 2
    cx = center_x + idx * GAP
    cy = center_y

    rot = idx * 2.5
    card = Image.new('RGBA', (CARD_W, CARD_H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    for y in range(CARD_H):
        t = y / CARD_H
        if t < 0.65:
            r = int(card_beige[0][0] + (card_beige[1][0] - card_beige[0][0]) * (t / 0.65))
            g = int(card_beige[0][1] + (card_beige[1][1] - card_beige[0][1]) * (t / 0.65))
            b = int(card_beige[0][2] + (card_beige[1][2] - card_beige[0][2]) * (t / 0.65))
        else:
            u = (t - 0.65) / 0.35
            r = int(card_beige[1][0] + (card_beige[2][0] - card_beige[1][0]) * u)
            g = int(card_beige[1][1] + (card_beige[2][1] - card_beige[1][1]) * u)
            b = int(card_beige[1][2] + (card_beige[2][2] - card_beige[1][2]) * u)
        cd.line([(0, y), (CARD_W, y)], fill=(r, g, b))

    mask = Image.new('L', (CARD_W, CARD_H), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, CARD_W, CARD_H), radius=16, fill=255)

    # 编号小圆
    cx_n, cy_n = CARD_W - 33 - 16, 16 + 17
    cd.ellipse((cx_n - 17, cy_n - 17, cx_n + 17, cy_n + 17), fill=(255, 255, 255, 25), outline=(58, 42, 26, 110), width=1)
    font_num = get_font(13, bold=False)
    nbb = cd.textbbox((0, 0), num, font=font_num)
    nb_w, nb_h = nbb[2] - nbb[0], nbb[3] - nbb[1]
    cd.text((cx_n - nb_w/2, cy_n - nb_h/2 - 1), num, fill=text_num, font=font_num)

    font_title = get_font(26, bold=True)
    cd.text((24, 80), title, fill=text_dark, font=font_title)
    font_desc = get_font(12, bold=False)
    cd.text((24, 145), desc, fill=text_dark_soft, font=font_desc)

    # 中间卡 ▶
    if i == 2:
        pw, ph = 56, 56
        px, py = (CARD_W - pw) // 2, (CARD_H - ph) // 2 + 30
        cd.ellipse((px, py, px + pw, py + ph), fill=(255, 255, 255, 235))
        cd.polygon([(px + 22, py + 16), (px + 22, py + 40), (px + 40, py + 28)], fill=text_dark)

    rotated = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    rmask = mask.rotate(rot, resample=Image.BICUBIC, expand=True)
    rx = int(cx - rotated.width / 2)
    ry = int(cy - rotated.height / 2)
    canvas.paste(rotated, (rx, ry), rmask)

# 卡片底端位置文字提示
tip_font = get_font(11, bold=False)
tip = f"卡片中心 = 屏幕底上方 {abs(baseY)}px  |  卡片底端距屏底 {abs(baseY) - 145}px  |  进度条在屏底上方 78px"
tb = draw.textbbox((0, 0), tip, font=tip_font)[2]
draw.text(((SW - tb) // 2, 640), tip, fill=(180, 180, 180), font=tip_font)

canvas.save('cards-position-preview.png')
print(f"saved cards-position-preview.png  size={canvas.size}")
print(f"卡片中心 y = {center_y},  卡片底 y = {center_y + 145},  卡片顶 y = {center_y - 145}")
