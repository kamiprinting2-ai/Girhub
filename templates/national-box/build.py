"""National Day cube box: lid top-face artwork + 3D mockup.
Box (owner's reference ref-box.jpg): white base, red lid sides with a wave edge, design on the lid TOP only.
Calligraphy «دام عزك يا وطن» = owner's file (source-calligraphy.png) traced to vector (calligraphy.svg).
  python3 templates/national-box/build.py   (from repo root)
Print file: top face 100x100 mm + 3 mm bleed (106 mm), text kept inside a 6 mm safe margin.
"""
import os, re, json, subprocess
H = os.path.dirname(os.path.abspath(__file__))
RED, DEEP, WHITE, PEARL = '#CE1126', '#8E0E1F', '#FBF8F3', '#EDE6DA'
svg = open(os.path.join(H, 'calligraphy.svg')).read()
vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
path = re.search(r'<path[^>]*d="([^"]+)"', svg).group(1)

def top_face(size=1060, bleed=30):
    """1060 units = 106 mm (1 unit = 0.1 mm). Trim box 30..1030."""
    S = size
    # flag serration: 5 points pointing up, red below
    y0 = 760   # serration base line
    tip = 690  # tip height
    n = 5; w = S / n
    pts = [f'0,{y0}']
    for i in range(n):
        pts += [f'{i*w + w/2:.1f},{tip}', f'{(i+1)*w:.1f},{y0}']
    red = f'<polygon points="{" ".join(pts)} {S},{S} 0,{S}" fill="{RED}"/>'
    # pearl arc above the calligraphy
    import math
    pearls = ''
    for k in range(13):
        t = -0.9 + 1.8 * k / 12
        x = S/2 + 300 * math.sin(t); y = 300 - 60 * math.cos(t)
        r = 9 if k % 6 == 0 else 6
        pearls += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="url(#pearl)"/>'
    vx, vy, vw, vh = map(float, vb.split())
    cw = 840; ch = cw * vh / vw
    cal = (f'<svg x="{(S-cw)/2:.1f}" y="{345:.1f}" width="{cw}" height="{ch:.1f}" viewBox="{vb}">'
           f'<path fill="{DEEP}" fill-rule="evenodd" d="{path}"/></svg>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">
  <defs>
    <radialGradient id="pearl" cx=".35" cy=".35"><stop offset="0" stop-color="#ffffff"/><stop offset=".7" stop-color="{PEARL}"/><stop offset="1" stop-color="#cdbfa9"/></radialGradient>
    <pattern id="weave" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{WHITE}"/>
      <path d="M0 2h8M0 6h8" stroke="#000" stroke-opacity=".025" stroke-width="2"/><path d="M2 0v8M6 0v8" stroke="#000" stroke-opacity=".018" stroke-width="2"/></pattern>
  </defs>
  <rect width="{S}" height="{S}" fill="url(#weave)"/>
  {pearls}
  <circle cx="{S/2}" cy="248" r="13" fill="url(#pearl)" stroke="#d8ccb8" stroke-width="1"/>
  {cal}
  <g fill="{DEEP}" opacity=".9"><rect x="{S/2-170}" y="650" width="120" height="2.5"/><rect x="{S/2+50}" y="650" width="120" height="2.5"/></g>
  <circle cx="{S/2}" cy="651" r="9" fill="url(#pearl)"/>
  {red}
  <text x="{S/2}" y="880" text-anchor="middle" font-family="Readex Pro" font-weight="700" font-size="62" fill="#ffffff">اليوم الوطني البحريني</text>
  <text x="{S/2}" y="950" text-anchor="middle" font-family="Readex Pro" font-weight="500" font-size="40" fill="#ffffff" opacity=".9">١٦ ديسمبر</text>
</svg>'''

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;700&display=swap" rel="stylesheet">'

def side_svg():
    # lid side: red, wave edge (down at corners, scooped up in the middle)
    return f'''<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="width:100%;height:100%;display:block">
      <path d="M0 0 H100 V62 Q100 70 92 70 Q84 70 80 60 Q72 34 50 34 Q28 34 20 60 Q16 70 8 70 Q0 70 0 62Z" fill="{RED}"/>
      <path d="M0 0 H100 V62 Q100 70 92 70 Q84 70 80 60 Q72 34 50 34 Q28 34 20 60 Q16 70 8 70 Q0 70 0 62Z" fill="url(#lw)" opacity=".12"/>
      <defs><linearGradient id="lw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient></defs></svg>'''

def mockup(top):
    E = 520
    face = lambda tr, inner, extra='': f'<div class="f" style="transform:{tr};{extra}">{inner}</div>'
    base = f'<div style="width:100%;height:100%;background:linear-gradient(180deg,#f7f5f1,#e9e5de)"></div>'
    sides = ''
    for ang, shade in ((0, 0), (90, .14), (180, .2), (-90, .08)):
        sides += face(f'rotateY({ang}deg) translateZ({E/2}px)',
                      f'<div style="position:absolute;inset:0">{base}</div><div style="position:absolute;inset:0">{side_svg()}</div>'
                      f'<div style="position:absolute;inset:0;background:rgba(0,0,0,{shade})"></div>')
    topf = face(f'rotateX(90deg) translateZ({E/2}px)', f'<div style="width:100%;height:100%;overflow:hidden">{top}</div>')
    return f'''<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:radial-gradient(circle at 70% 20%,#ffffff,#ece7df 60%,#ddd6cb);display:flex;align-items:center;justify-content:center;overflow:hidden}}
.scene{{perspective:1800px;margin-top:80px}}
.cube{{width:{E}px;height:{E}px;position:relative;transform-style:preserve-3d;transform:rotateX(-28deg) rotateY(-38deg)}}
.f{{position:absolute;width:{E}px;height:{E}px;backface-visibility:hidden}}
.f svg{{width:100%;height:100%}}
.shadow{{position:absolute;width:760px;height:170px;left:160px;top:1060px;background:radial-gradient(ellipse,rgba(60,45,30,.35),transparent 70%);filter:blur(10px)}}
.wm{{position:absolute;left:60px;bottom:50px;font:600 26px 'Readex Pro';color:rgba(46,59,42,.55)}}
</style></head><body><div class="shadow"></div><div class="scene"><div class="cube">{sides}{topf}</div></div><div class="wm">Kami printing</div></body></html>'''

def main():
    top = top_face()
    open(os.path.join(H, 'top-face.svg'), 'w', encoding='utf-8').write(top)
    page = f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>*{{margin:0}}body{{width:1060px;height:1060px}}</style></head><body>{top}</body></html>'
    open(os.path.join(H, 'top-face.html'), 'w', encoding='utf-8').write(page)
    # mockup uses the trimmed face (inside bleed)
    trimmed = top.replace('viewBox="0 0 1060 1060"', 'viewBox="30 30 1000 1000"')
    open(os.path.join(H, 'mockup.html'), 'w', encoding='utf-8').write(mockup(trimmed))
    js = r'''
const {chromium}=require('playwright');const path=require('path');(async()=>{const b=await chromium.launch();const H=process.argv[1];
let p=await b.newPage({viewport:{width:1060,height:1060},deviceScaleFactor:2.36});
await p.goto('file://'+path.join(H,'top-face.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
await p.screenshot({path:path.join(H,'وجه-الغطا-106مم-600dpi.png')});
await p.pdf({path:path.join(H,'وجه-الغطا-106مم.pdf'),width:'106mm',height:'106mm',printBackground:true,pageRanges:'1',scale:0.3774});
p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await p.goto('file://'+path.join(H,'mockup.html'),{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
await p.screenshot({path:path.join(H,'موكب-العلبة.png')});await b.close()})()'''
    subprocess.run(['node', '-e', js, H], check=True)
    print('ok')

main()
