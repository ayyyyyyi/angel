# -*- coding: utf-8 -*-
import base64

html_path = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/dressup/dressup-demo.html"
png_path = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/dressup/character-cutout.png"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(png_path, "rb") as f:
    b64_png = base64.b64encode(f.read()).decode("ascii")

# 1. 替换 jpg base64 -> png base64（MIME 一起改）
img_start_marker = '<img class="character-img" id="character" src="data:image/jpeg;base64,'
img_end_marker = '" alt="角色底模">'

start = html.index(img_start_marker)
end = html.index(img_end_marker, start) + len(img_end_marker)
new_img = '<img class="character-img" id="character" src="data:image/png;base64,' + b64_png + '" alt="角色底模">'
html = html[:start] + new_img + html[end:]

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("OK. png b64 chars:", len(b64_png))
print("new html size:", len(html))