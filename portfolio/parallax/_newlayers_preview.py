"""用新三图生成 4 张静态预览：远景/中景/贴脸/极限贴脸，方便用户对比效果"""
from PIL import Image
import os

OUT_DIR = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/parallax"

bg     = Image.open(os.path.join(OUT_DIR, "layer-bg.png")).convert("RGBA")
angel  = Image.open(os.path.join(OUT_DIR, "layer-angel.png")).convert("RGBA")
pillar = Image.open(os.path.join(OUT_DIR, "layer-pillar.png")).convert("RGBA")

print(f"bg     = {bg.size}")
print(f"angel  = {angel.size}")
print(f"pillar = {pillar.size}")

SW, SH = 1920, 1080

# 仿 parallax-scroll.html 的真实缩放/位移参数
def render(p, label):
    # p in [0, 1]
    canvas = Image.new("RGBA", (SW, SH), (8, 6, 4, 255))

    # === bg layer ===
    bg_from, bg_to = 1.00, 1.10
    bg_s = bg_from + (bg_to - bg_from) * p
    bg_new = bg.resize((int(bg.width * bg_s), int(bg.height * bg_s)), Image.LANCZOS)
    bg_x = (SW - bg_new.width) // 2
    bg_y = (SH - bg_new.height) // 2
    canvas.paste(bg_new, (bg_x, bg_y), bg_new)

    # === angel layer ===
    # start=0.00, end=1.00, ease=smoothstep
    ease = lambda t: t * t * (3 - 2 * t)  # smoothstep
    t_ang = ease(p)
    ang_from, ang_to = 1.00, 3.00
    ang_s = ang_from + (ang_to - ang_from) * t_ang
    a_new = angel.resize((int(angel.width * ang_s), int(angel.height * ang_s)), Image.LANCZOS)
    # translateY(-p*20) + origin 50% 38%
    oy_screen = SH * 0.38
    paste_x = int(SW * 0.50 - a_new.width * 0.50)
    paste_y = int(oy_screen - a_new.height * 0.38) + int(-p * 20)
    canvas.paste(a_new, (paste_x, paste_y), a_new)

    # === pillar layer ===
    # start=0.00, end=0.80, ease=easeInOut（立方）
    if p > 0.80:
        t_pil = 1.0
        pil_op = max(0, 1 - (p - 0.80) * 10)  # 0.80→0.90 淡出到 0
    else:
        ease_inout = lambda t: t * t * (3 - 2 * t)  # 也按 S 曲线简化
        t_pil = ease_inout(p / 0.80)
        pil_op = 1.0
    pil_from, pil_to = 1.00, 2.20
    pil_s = pil_from + (pil_to - pil_from) * t_pil
    p_new = pillar.resize((int(pillar.width * pil_s), int(pillar.height * pil_s)), Image.LANCZOS)
    pil_x = (SW - p_new.width) // 2
    pil_y = (SH - p_new.height) // 2
    if pil_op < 0.999:
        # 调整 alpha
        from PIL import Image as I
        data = p_new.getdata()
        new_data = [(r, g, b, int(a * pil_op)) for (r, g, b, a) in data]
        p_new.putdata(new_data)
    canvas.paste(p_new, (pil_x, pil_y), p_new)

    canvas.convert("RGB").save(os.path.join(OUT_DIR, f"newlayers-p{int(p*100):03d}.jpg"), quality=88)
    print(f"saved newlayers-p{int(p*100):03d}.jpg  ({label})")

for p, label in [
    (0.00, "远景 · 全新开局"),
    (0.30, "30% · 神像/石柱刚启动"),
    (0.70, "70% · 推进中"),
    (1.00, "100% · 贴脸"),
]:
    render(p, label)

print("done")
