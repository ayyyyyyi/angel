# -*- coding: utf-8 -*-
import base64

html_path = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/dressup/dressup-demo.html"
jpg_path = r"C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-31T12-46-51-344Z-45110ac0.jpg"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(jpg_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")

# 1. body 背景：暖黑径向渐变 -> 宫廷大堂图（base64 内嵌）
old_body = """  body {
    font-family: 'Georgia', 'Playfair Display', 'Times New Roman', serif;
    background: radial-gradient(ellipse at center top, #1a1208 0%, #0a0806 70%);
    color: #e8e0d2;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
  }"""

new_body = """  body {
    font-family: 'Georgia', 'Playfair Display', 'Times New Roman', serif;
    background-image: url('data:image/jpeg;base64,""" + b64 + """');
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
    color: #e8e0d2;
    min-height: 100vh;
    overflow-x: hidden;
    position: relative;
  }"""

assert old_body in html, "body block not found"
html = html.replace(old_body, new_body)
print("body replaced OK")

# 2. body::before: 金色光晕 -> 中央 vignette（中间透出宫廷，四角暗化做舞台聚焦，前景文字可读）
old_before = """  body::before {
    content: '';
    position: fixed;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 1200px;
    height: 800px;
    background: radial-gradient(ellipse, rgba(200,160,74,0.12) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }"""

new_before = """  /* 中央透出宫廷大堂，四角暗化做舞台聚焦 + 前景文字可读 */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse at center, transparent 0%, transparent 28%, rgba(0,0,0,0.55) 78%, rgba(0,0,0,0.82) 100%);
    pointer-events: none;
    z-index: 0;
  }"""

assert old_before in html, "body::before block not found"
html = html.replace(old_before, new_before)
print("body::before replaced OK")

# 3. character-img 去掉奶白光晕（背景已亮，叠光晕会糊）
old_img = ".character-img { width: 100%; height: 100%; object-fit: contain; background: radial-gradient(ellipse at 50% 42%, rgba(232,224,210,0.16) 0%, rgba(232,224,210,0.05) 50%, transparent 72%); filter: drop-shadow(0 20px 40px rgba(0,0,0,0.6)); }"

new_img = ".character-img { width: 100%; height: 100%; object-fit: contain; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.5)); }"

assert old_img in html, "character-img CSS not found"
html = html.replace(old_img, new_img)
print("character-img CSS replaced OK")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("done. new html size:", len(html))
