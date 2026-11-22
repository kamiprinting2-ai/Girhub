"""Two sample Kami favor designs shown as if photographed (mockups), inspired by instagram/examples:
 1. Gerga'oon die-cut card: faceless boy & girl holding a candy bar, «قرقاعون عادت عليكم», «من: ___».
 2. Malcha «نثور» pieces: kraft die-cut dalla with a coin window.
Pure HTML/SVG, no AI credits.  python3 templates/samples_favors.py && PAGE=samples-favors.html OUTDIR=out/samples node templates/render.js
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- 1) Gerga'oon card (viewBox 600x820) ----------
def kid(x, girl):
    # faceless child peeking from the top: head + headwear + hands
    if girl:
        back = f'''<path d="M{x-120} 380 Q{x-135} 150 {x} 140 Q{x+135} 150 {x+120} 380Z" fill="#6E8B5E"/>'''
        front = f'''<path d="M{x-86} 250 Q{x-80} 168 {x} 166 Q{x+80} 168 {x+86} 250" fill="none" stroke="#D9B45A" stroke-width="6" stroke-dasharray="2 11" stroke-linecap="round"/>
        <g fill="#D9B45A">{''.join(f'<circle cx="{x-75+i*30}" cy="372" r="5"/>' for i in range(6))}</g>'''
        face_y = 262
    else:
        back = ''
        front = f'''<path d="M{x-92} 228 Q{x} 140 {x+92} 228Z" fill="#FFFFFF" stroke="#E7E1D3" stroke-width="3"/>
        <ellipse cx="{x}" cy="226" rx="94" ry="20" fill="#FFFFFF" stroke="#E7E1D3" stroke-width="3"/>
        <g fill="none" stroke="#C9B98F" stroke-width="3">{''.join(f'<path d="M{x-56+i*28} 205 l8 -10 l8 10"/>' for i in range(5))}</g>'''
        face_y = 270
    return f'''<g>
      <path d="M{x-112} 420 Q{x-112} 330 {x} 330 Q{x+112} 330 {x+112} 420Z" fill="{'#E9D3D0' if girl else '#F4F1EA'}"/>
      {back}
      <circle cx="{x}" cy="{face_y}" r="80" fill="#F2D2B6"/>
      {front}
      <circle cx="{x-42}" cy="{face_y+22}" r="13" fill="#EFA9A5" opacity=".8"/><circle cx="{x+42}" cy="{face_y+22}" r="13" fill="#EFA9A5" opacity=".8"/>
    </g>'''

CANDY = '''<g transform="translate(70 420)">
  <path d="M0 18 L30 0 L30 120 L0 102Z" fill="#B8925A"/><path d="M460 18 L430 0 L430 120 L460 102Z" fill="#B8925A"/>
  <rect x="28" y="0" width="404" height="120" rx="12" fill="#5B3A29"/>
  <rect x="28" y="0" width="404" height="120" rx="12" fill="url(#foil)" opacity=".35"/>
  <text x="230" y="78" text-anchor="middle" font-family="Aref Ruqaa" font-weight="700" font-size="50" fill="#E8C987">حلاوة</text>
</g>'''
HANDS = ''.join(f'<ellipse cx="{x}" cy="432" rx="30" ry="22" fill="#F2D2B6" stroke="#E2BE9E" stroke-width="2"/>' for x in (120, 205, 395, 480))

def gerga_card(names='من: ـــــــــــــــ'):
    return f'''<svg viewBox="0 0 600 820" class="card">
  <defs><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity=".5"/></linearGradient>
  <filter id="cut" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#3b3226" flood-opacity=".28"/></filter></defs>
  <g filter="url(#cut)">
    <path d="M40 300 Q40 120 170 120 Q240 120 300 200 Q360 120 430 120 Q560 120 560 300 L560 760 Q560 800 520 800 L80 800 Q40 800 40 760Z" fill="#FBF7EF"/>
  </g>
  <path d="M56 305 Q56 136 170 136 Q236 136 300 222 Q364 136 430 136 Q544 136 544 305 L544 752 Q544 784 512 784 L88 784 Q56 784 56 752Z" fill="none" stroke="#9CAB86" stroke-width="3" stroke-dasharray="1 9" stroke-linecap="round"/>
  <g fill="#D9B45A"><path d="M300 70 a26 26 0 1 0 20 44 a20 20 0 1 1 -20 -44z"/>
    <path d="M90 200 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4z"/><path d="M505 205 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4 l10 -4z"/></g>
  {kid(165, False)}{kid(435, True)}
  {CANDY}{HANDS}
  <text x="300" y="652" text-anchor="middle" font-family="Aref Ruqaa" font-weight="700" font-size="64" fill="#2E3B2A">قرقاعون عادت عليكم</text>
  <text x="300" y="730" text-anchor="middle" font-family="Readex Pro" font-weight="500" font-size="34" fill="#6B7A5C">{names}</text>
</svg>'''

# ---------- 2) Dalla «نثور» piece (viewBox 400x600) ----------
DALLA = ('M150 95 L250 95 Q255 120 270 135 Q320 170 318 230 Q316 290 250 315 Q236 322 240 336 '
         'Q300 362 318 430 L330 500 L70 500 L82 430 Q100 362 160 336 Q164 322 150 315 Q84 290 82 230 '
         'Q80 170 130 135 Q145 120 150 95Z')
SPOUT = 'M104 188 Q44 168 20 92 Q14 76 28 80 Q46 140 110 162Z'
HANDLE = 'M300 160 Q372 150 374 240 Q374 330 300 360 L292 340 Q350 318 350 245 Q350 180 302 184Z'
CAP = 'M175 40 L225 40 L232 70 L168 70Z M160 68 L240 68 L252 97 L148 97Z M200 14 a10 10 0 1 1 -0.1 0Z M196 22 L204 22 L206 42 L194 42Z'

def dalla(color, coin=False, label=True):
    holes = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#00000000"/>' for cx, cy, r in ())
    lattice = ''.join(f'<path d="M{x} 74 l9 9 l-9 9 l-9 -9z" fill="url(#hole)"/>' for x in (178, 200, 222))
    win = '<circle cx="200" cy="228" r="60" fill="url(#hole)"/>'
    c = ('<circle cx="200" cy="228" r="62" fill="url(#silver)" stroke="#9a9a9a" stroke-width="2"/>'
         '<circle cx="200" cy="228" r="48" fill="none" stroke="#cfcfcf" stroke-width="2"/>'
         '<text x="200" y="241" text-anchor="middle" font-family="Readex Pro" font-weight="700" font-size="34" fill="#8d8d8d">100</text>') if coin else ''
    moon = '<path d="M204 398 a26 26 0 1 0 19 44 a21 21 0 1 1 -19 -44z" fill="url(#hole)"/>'
    lab = ('<text x="200" y="551" text-anchor="middle" font-family="Aref Ruqaa" font-weight="700" font-size="30" fill="#5a4330">ملجة سارة ومحمد</text>') if label else ''
    return f'''<svg viewBox="0 0 400 600" class="dl">
  <g filter="url(#cut)" fill="{color}">
    <path d="{DALLA}"/><path d="{SPOUT}"/><path d="{HANDLE}"/><path d="{CAP}"/>
  </g>
  <g fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-width="2"><path d="{DALLA}" transform="translate(0 0)"/></g>
  {lattice}{win}{c}{moon}
  <rect x="62" y="512" width="276" height="56" rx="10" fill="{color}" filter="url(#cut)"/>{lab}
</svg>'''

DEFS = '''<svg width="0" height="0" style="position:absolute"><defs>
<filter id="cut" x="-15%" y="-15%" width="130%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#3b3226" flood-opacity=".3"/></filter>
<radialGradient id="silver" cx=".35" cy=".35"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#c9c9c9"/><stop offset="1" stop-color="#9b9b9b"/></radialGradient>
<linearGradient id="hole"><stop offset="0" stop-color="#ECE6DB"/><stop offset="1" stop-color="#E2DACB"/></linearGradient>
</defs></svg>'''

KRAFT, KRAFT2 = '#C9A27A', '#7A5A41'

CSS = '''*{margin:0;padding:0;box-sizing:border-box}
body{background:#555;display:flex;flex-direction:column;gap:40px;padding:40px}
.post{width:1080px;height:1350px;position:relative;overflow:hidden}
.linen{background:#EFE8DC;background-image:
  radial-gradient(circle at 20% 15%,rgba(255,255,255,.7),transparent 45%),
  radial-gradient(circle at 85% 90%,rgba(0,0,0,.06),transparent 50%),
  repeating-linear-gradient(0deg,rgba(0,0,0,.018) 0 2px,transparent 2px 5px),
  repeating-linear-gradient(90deg,rgba(0,0,0,.015) 0 2px,transparent 2px 6px)}
.white{background:#F5F3EF;background-image:radial-gradient(circle at 30% 20%,#fff,transparent 55%),radial-gradient(circle at 90% 95%,rgba(0,0,0,.07),transparent 55%)}
.abs{position:absolute}
.card{width:100%;height:100%}
.dl{width:100%;height:100%}
.wm{position:absolute;left:60px;bottom:52px;font:italic 400 30px 'Pinyon Script',cursive;color:rgba(255,255,255,.9);text-shadow:0 1px 3px rgba(0,0,0,.25)}
.wm.dark{color:rgba(90,67,48,.55);text-shadow:none}
.light{position:absolute;inset:0;background:linear-gradient(115deg,rgba(255,255,255,.35),transparent 40%,transparent 70%,rgba(0,0,0,.06))}
.lantern{position:absolute;right:-30px;top:-40px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(255,214,140,.55),transparent 65%)}
'''

def post_gerga():
    return f'''<section class="post linen" id="sample-01">
  <div class="lantern"></div>
  <div class="abs" style="left:-40px;top:70px;width:430px;height:588px;transform:rotate(-9deg);opacity:.97">{gerga_card('من: ســارة')}</div>
  <div class="abs" style="left:610px;top:40px;width:430px;height:588px;transform:rotate(8deg)">{gerga_card('من: يوسـف')}</div>
  <div class="abs" style="left:210px;top:430px;width:640px;height:875px;transform:rotate(-2deg)">{gerga_card('من: نورة')}</div>
  <div class="light"></div><div class="wm">Kami printing</div>
</section>'''

def post_nathour():
    pieces = ''
    spots = [(-30, 60, -14, KRAFT2, False), (300, 10, 6, KRAFT, False), (700, 70, 16, KRAFT2, False),
             (40, 640, 10, KRAFT, False), (760, 700, -10, KRAFT, False)]
    for x, y, r, c, coin in spots:
        pieces += f'<div class="abs" style="left:{x}px;top:{y}px;width:300px;height:450px;transform:rotate({r}deg)">{dalla(c, coin, False)}</div>'
    pieces += f'<div class="abs" style="left:250px;top:380px;width:580px;height:870px;transform:rotate(-3deg)">{dalla(KRAFT, True, True)}</div>'
    return f'''<section class="post white" id="sample-02">{pieces}<div class="light"></div><div class="wm dark">Kami printing</div></section>'''

page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Favor Samples</title>
<link href="https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=Readex+Pro:wght@500;700&family=Pinyon+Script&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{DEFS}{post_gerga()}{post_nathour()}</body></html>'''
open(os.path.join(HERE, 'samples-favors.html'), 'w', encoding='utf-8').write(page)
print('ok')
