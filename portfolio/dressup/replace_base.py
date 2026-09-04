# -*- coding: utf-8 -*-
import base64

html_path = r"C:/Users/ayiqianwang/WorkBuddy/vibe coding/portfolio/dressup/dressup-demo.html"
jpg_path = r"C:/Users/ayiqianwang/.workbuddy/clipboard-images/clipboard-2026-08-31T12-42-30-965Z-c52adaae.jpg"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

with open(jpg_path, "rb") as f:
    b64 = base64.b64encode(f.read()).decode("ascii")

# 1. 整个 SVG 角色块替换成 img（base64 内嵌，避免预览 404）
svg_start = html.index('<svg class="character-svg"')
svg_end = html.index('</svg>', svg_start) + len('</svg>')
img_tag = '<img class="character-img" id="character" src="data:image/jpeg;base64,' + b64 + '" alt="角色底模">'
html = html[:svg_start] + img_tag + html[svg_end:]

# 2. CSS：.character-svg -> .character-img（object-fit 保证全身完整 + 淡奶白光晕过渡）
html = html.replace(
    '.character-svg { width: 100%; height: 100%; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.6)); }',
    '.character-img { width: 100%; height: 100%; object-fit: contain; background: radial-gradient(ellipse at 50% 42%, rgba(232,224,210,0.16) 0%, rgba(232,224,210,0.05) 50%, transparent 72%); filter: drop-shadow(0 20px 40px rgba(0,0,0,0.6)); }'
)

# 3. 闪光动画选择器同步改
html = html.replace(
    '.character-svg.flash { animation: outfit-glow 0.8s ease; }',
    '.character-img.flash { animation: outfit-glow 0.8s ease; }'
)

# 4. setOutfit 降级：去掉 SVG outfit 图层切换，保留闪光 + 卡片激活（衣服 PNG 到齐后再接真切换）
old = '''  function setOutfit(id) {
    if (id === currentOutfit) return;
    document.querySelectorAll('.outfit').forEach(o => o.classList.remove('active'));
    const next = document.getElementById('outfit-' + id);
    if (next && id !== 0) next.classList.add('active');
    currentOutfit = id;

    // 闪光反馈
    const svg = document.getElementById('character');
    svg.classList.remove('flash');
    void svg.offsetWidth; // 强制重排
    if (id !== 0) svg.classList.add('flash');

    // 卡片激活态
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    if (id !== 0) {
      const card = document.querySelector('.card[data-outfit="' + id + '"]');
      if (card) card.classList.add('active');
    }
  }'''

new = '''  function setOutfit(id) {
    if (id === currentOutfit) return;
    currentOutfit = id;

    // 闪光反馈（换装占位：5 套衣服 PNG 到齐后替换成真正的图层切换）
    const img = document.getElementById('character');
    img.classList.remove('flash');
    void img.offsetWidth; // 强制重排
    img.classList.add('flash');

    // 卡片激活态
    document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
    const card = document.querySelector('.card[data-outfit="' + id + '"]');
    if (card) card.classList.add('active');
  }'''

html = html.replace(old, new)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("OK. new html size:", len(html))
