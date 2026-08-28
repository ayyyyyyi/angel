from PIL import Image, ImageDraw, ImageFont
import os, math

SW, SH = 1920, 1080

bg_color = (24, 12, 8)
canvas = Image.new('RGB', (SW, SH), bg_color)
draw = ImageDraw.Draw(canvas)

for y in range(SH):
    t = y / SH
    r = int(40 - 20 * t)
    g = int(15 - 5 * t)
    b = int(8 + 4 * t)
    draw.line([(0, y), (SW, y)], fill=(r, g, b))

def get_font(size, bold=False):
    paths = [
        r"C:\Windows\Fonts\georgiab.ttf" if bold else r"C:\Windows\Fonts\georgia.ttf",
        r"C:\Windows\Fonts\timesbd.ttf" if bold else r"C:\Windows\Fonts\times.ttf",
        r"C:\Windows\Fonts\msyhbd.ttc" if bold else r"C:\Windows\Fonts\msyh.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

CARD_W, CARD_H = 220, 290
GAP = 260
N = 5
center_x = SW // 2
center_y = SH // 2 - 30

card_beige = [(231, 212, 179), (218, 196, 163), (207, 184, 143)]
text_dark = (43, 31, 18)
text_dark_soft = (78, 56, 38)
text_num = (58, 42, 26)

cards = [
    ("01", "Bespoke\nQuests", "Journeys shaped around\nyour vision and soul"),
    ("02", "Vivid\nDrifts", "Surreal passages\nthrough breathtaking terrain"),
    ("03", "Mystic\nCrests", "Timeless ridgelines wrapped\nin cloud and myth"),
    ("04", "Deep\nCurrents", "Glowing depths alive\nwith uncharted wonder"),
    ("05", "Gilded\nDusk", "Amber horizons that\nstretch past all reason"),
]

for i, (num, title, desc) in enumerate(cards):
    idx = i - (N - 1) / 2
    cx = center_x + idx * GAP
    cy = center_y + 50
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

    cx_n = CARD_W - 16 - 17
    cy_n = 16 + 17
    cd.ellipse((cx_n - 17, cy_n - 17, cx_n + 17, cy_n + 17), fill=(255, 255, 255, 25), outline=(58, 42, 26), width=1)
    font_num = get_font(13, bold=False)
    nb_box = cd.textbbox((0, 0), num, font=font_num)
    nb, nh = nb_box[2] - nb_box[0], nb_box[3] - nb_box[1]
    cd.text((cx_n - nb / 2, cy_n - nh / 2 - 1), num, fill=text_num, font=font_num)

    font_title = get_font(26, bold=True)
    lines = title.split("\n")
    ty = 80
    for line in lines:
        cd.text((24, ty), line, fill=text_dark, font=font_title)
        ty += 30

    font_desc = get_font(13, bold=False)
    dy = ty + 14
    for line in desc.split("\n"):
        cd.text((24, dy), line, fill=text_dark_soft, font=font_desc)
        dy += 18

    if i == 2:
        pw, ph = 56, 56
        px, py = (CARD_W - pw) // 2, (CARD_H - ph) // 2 + 30
        cd.ellipse((px, py, px + pw, py + ph), fill=(255, 255, 255), outline=(58, 42, 26), width=1)
        ts = [
            (px + 22, py + 16),
            (px + 22, py + 40),
            (px + 40, py + 28),
        ]
        cd.polygon(ts, fill=text_dark)

    rotated = card.rotate(rot, resample=Image.BICUBIC, expand=True)
    rmask = mask.rotate(rot, resample=Image.BICUBIC, expand=True)
    rx = int(cx - rotated.width / 2)
    ry = int(cy - rotated.height / 2)
    canvas.paste(rotated, (rx, ry), rmask)

# Top nav
font_nav = get_font(13, bold=False)
nav_left = ["WORLDS", "ATELIER", "IMMERSIONS"]
nav_right = ["CRAFT", "CODEX", "CONNECT"]
x_pos = 40
for item in nav_left:
    draw.text((x_pos, 28), item, fill="white", font=font_nav)
    x_pos += 90

sx, sy = SW // 2, 38
star_pts = []
for k in range(8):
    angle = math.pi * 2 * k / 8 - math.pi / 2
    r = 5 if k % 2 == 0 else 2
    star_pts.append((sx + r * math.cos(angle), sy + r * math.sin(angle)))
draw.polygon(star_pts, fill="white")

nav_right_text = "    ".join(nav_right)
nb = draw.textbbox((0, 0), nav_right_text, font=font_nav)[2]
draw.text((SW - 40 - nb, 28), nav_right_text, fill="white", font=font_nav)

# Title
font_h1 = get_font(56, bold=True)
title_text = "FORGE BEYOND THE REAL"
tb = draw.textbbox((0, 0), title_text, font=font_h1)[2]
draw.text(((SW - tb) // 2, 100), title_text, fill="white", font=font_h1)

# Subtitle
font_sub = get_font(15, bold=False)
sub_text = "Singular voyages to astonishing destinations, shaped for those who seek\nbeauty beyond the ordinary and the known."
sub_lines = sub_text.split("\n")
sy = 180
for line in sub_lines:
    sl = draw.textbbox((0, 0), line, font=font_sub)[2]
    draw.text(((SW - sl) // 2, sy), line, fill=(220, 220, 220), font=font_sub)
    sy += 24

# Bottom hint
font_hint = get_font(11, bold=False)
hint = "01 - 02 - 03 - 04 - 05   |   PROJECT - CONTENT - INTERN - DATA - KOL"
hb = draw.textbbox((0, 0), hint, font=font_hint)[2]
draw.text(((SW - hb) // 2, SH - 60), hint, fill=(212, 176, 106), font=font_hint)

canvas.save("cards-style-preview.jpg", quality=92)
print(f"saved cards-style-preview.jpg  size={canvas.size}")
