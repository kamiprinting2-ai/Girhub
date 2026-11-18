"""Kawaii dalla (Arabic coffee/tea flask) sticker set, drawn as vectors in the style of the owner's cocoa-cup reference:
cream bodies, thin soft-brown outline, coral knit scarf, blush cheeks, closed happy eyes.
Run:  python3 templates/dalla_stickers.py   -> brand/stickers/dalla/*.png (transparent, with white die-cut border),
       sheet.png, sheet-preview.jpg, mockup.jpg
"""
import os, subprocess, sys, json, random, math
BR = '#5B3B2E'; CREAM = '#FBF1DF'; PEACH = '#F4D3B6'; CORAL = '#E8917E'; BLUSH = '#F2A29A'; BROWN = '#8A5A3C'
SAGE = '#BFD9C6'; TEA = '#D58A52'; BEIGE = '#EAD2B4'; WHITE = '#FFFFFF'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'brand', 'stickers', 'dalla')
ST = f'stroke="{BR}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"'

def face(cx, cy, k=1.0, sleepy=False):
    ex = 26 * k; ey = cy - 6 * k; r = 9 * k
    eyes = ''.join(f'<path d="M{x - r},{ey} Q{x},{ey - r * 1.5} {x + r},{ey}" fill="none" {ST}/>' for x in (cx - ex, cx + ex))
    cheeks = ''.join(f'<ellipse cx="{x}" cy="{cy + 8 * k}" rx="{11 * k}" ry="{8 * k}" fill="{BLUSH}" opacity=".85"/>' for x in (cx - 40 * k, cx + 40 * k))
    mouth = f'<path d="M{cx - 8 * k},{cy + 6 * k} Q{cx},{cy + 17 * k} {cx + 8 * k},{cy + 6 * k}" fill="none" {ST}/>'
    z = f'<text x="{cx + 44 * k}" y="{cy - 30 * k}" font-family="Readex Pro" font-weight="700" font-size="{22 * k}" fill="{BR}">z<tspan dx="3" dy="-9" font-size="{16 * k}">z</tspan></text>' if sleepy else ''
    return cheeks + eyes + mouth + z

def heart(cx, cy, s, fill):
    return (f'<path transform="translate({cx},{cy}) scale({s})" d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="{fill}" {ST.replace("4", str(max(2, round(4 / s * 0.9))), 1) if False else ST}/>')

def steam_heart(cx, cy, s=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><path d="M0 40 C-60 0 -40 -40 0 -14 C40 -40 60 0 0 40 Z" fill="none" stroke="{BEIGE}" stroke-width="16" stroke-linecap="round"/></g>')

def knit(x, y, w, h, rot=0):
    lines = ''.join(f'<path d="M{x + i * 14},{y + 4} l6,{h - 8}" stroke="#C86E5C" stroke-width="3" fill="none" stroke-linecap="round"/>' for i in range(int(w / 14)))
    return f'<g transform="rotate({rot} {x + w / 2} {y + h / 2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{CORAL}" {ST}/>{lines}</g>'

def dallah():
    return f'''
    <g {ST}>
      <path d="M262 258 Q335 236 352 140 L372 131 Q372 250 290 296 Z" fill="{CREAM}"/>
      <path d="M126 248 Q56 244 62 182 Q66 150 112 160" fill="none" stroke="{BR}" stroke-width="22"/>
      <path d="M126 248 Q56 244 62 182 Q66 150 112 160" fill="none" stroke="{PEACH}" stroke-width="13"/>
      <path d="M132 338 Q92 306 108 252 Q124 214 164 198 L174 150 L226 150 L236 198 Q276 214 292 252 Q308 306 268 338 Z" fill="{CREAM}"/>
      <path d="M118 338 Q200 356 282 338 L284 356 Q200 374 116 356 Z" fill="{PEACH}"/>
      <path d="M172 150 L228 150 L224 168 L176 168 Z" fill="{PEACH}"/>
      <path d="M176 150 Q200 98 224 150 Z" fill="{PEACH}"/>
      <circle cx="200" cy="100" r="11" fill="{CORAL}"/>
    </g>
    <g {ST}>
      <path d="M168 196 Q200 214 232 196 L236 226 Q200 244 164 226 Z" fill="{CORAL}"/>
      <path d="M212 226 L246 232 L252 292 L218 288 Z" fill="{CORAL}"/>
    </g>
    {''.join(f'<path d="M{222 + i * 7},{236} l1,46" stroke="#C86E5C" stroke-width="3" stroke-linecap="round"/>' for i in range(4))}
    {face(196, 286, 0.95)}
    {steam_heart(200, 52, 0.55)}
    <circle cx="96" cy="90" r="5" fill="{BLUSH}"/><circle cx="318" cy="80" r="6" fill="{PEACH}"/>'''

def finjan():
    return f'''
    {steam_heart(200, 64, 0.6)}
    <g {ST}>
      <ellipse cx="200" cy="338" rx="120" ry="24" fill="{PEACH}"/>
      <path d="M284 220 Q352 214 346 262 Q340 304 278 298" fill="none" stroke="{BR}" stroke-width="22"/>
      <path d="M284 220 Q352 214 346 262 Q340 304 278 298" fill="none" stroke="{CREAM}" stroke-width="13"/>
      <path d="M108 190 H292 Q290 330 200 336 Q110 330 108 190 Z" fill="{CREAM}"/>
      <ellipse cx="200" cy="190" rx="92" ry="22" fill="{TEA}"/>
      <path d="M112 232 Q200 252 288 232" fill="none" stroke="{CORAL}" stroke-width="10"/>
    </g>
    {face(200, 286, 0.95)}
    <circle cx="112" cy="130" r="5" fill="{BLUSH}"/><circle cx="296" cy="128" r="5" fill="{PEACH}"/>'''

def date():
    return f'''
    <g {ST}>
      <path d="M198 78 Q196 56 214 46" fill="none"/>
      <path d="M200 84 C130 74 92 150 100 232 C108 322 160 352 214 350 C282 346 312 280 306 206 C300 130 262 80 200 84 Z" fill="{BROWN}"/>
      <path d="M200 84 Q214 70 226 82" fill="{BROWN}"/>
    </g>
    <path d="M132 150 Q150 130 176 124" fill="none" stroke="#B88562" stroke-width="9" stroke-linecap="round" opacity=".7"/>
    <path d="M140 300 q14 6 30 0 M252 292 q12 -4 24 -14 M258 160 q8 10 6 24" fill="none" stroke="#6E4630" stroke-width="3.5" stroke-linecap="round"/>
    <g {ST}><path d="M200 84 Q196 60 214 48" fill="none" stroke-width="7"/></g>
    {face(202, 232, 1.05, sleepy=True)}'''

def cardamom():
    return f'''
    <g transform="rotate(-18 200 210)" {ST}>
      <path d="M200 52 C300 96 322 240 200 366 C78 240 100 96 200 52 Z" fill="{SAGE}"/>
      <path d="M200 52 C186 150 186 260 200 366" fill="none" stroke-width="3.5" opacity=".55"/>
      <path d="M200 52 C250 130 256 270 200 366" fill="none" stroke-width="3.5" opacity=".4"/>
      <path d="M200 52 C150 130 144 270 200 366" fill="none" stroke-width="3.5" opacity=".4"/>
      <path d="M200 52 Q204 36 214 30" fill="none" stroke-width="6"/>
    </g>
    {face(196, 232, 1.0)}
    <path d="M120 100 q12 -22 36 -28" fill="none" stroke="#E4F1E8" stroke-width="9" stroke-linecap="round" opacity=".9"/>'''

def marsh():
    return f'''
    <g {ST}><rect x="100" y="118" width="200" height="200" rx="52" fill="{WHITE}"/></g>
    <path d="M124 160 q10 -16 30 -20" fill="none" stroke="{BEIGE}" stroke-width="9" stroke-linecap="round"/>
    {face(200, 232, 1.05, sleepy=True)}
    {steam_heart(200, 50, 0.38)}'''

def sparkles():
    def star(cx, cy, r, fill):
        d = f'M{cx},{cy - r} Q{cx},{cy} {cx + r},{cy} Q{cx},{cy} {cx},{cy + r} Q{cx},{cy} {cx - r},{cy} Q{cx},{cy} {cx},{cy - r} Z'
        return f'<path d="{d}" fill="{fill}" {ST}/>'
    return star(190, 200, 120, PEACH) + star(300, 100, 54, CORAL) + star(112, 318, 50, CREAM) + star(318, 312, 30, BLUSH)

def tea():
    return f'''
    {steam_heart(200, 60, 0.58)}
    <g {ST}>
      <ellipse cx="200" cy="344" rx="104" ry="20" fill="{PEACH}"/>
      <path d="M118 150 H282 Q264 228 270 262 Q276 332 200 338 Q124 332 130 262 Q136 228 118 150 Z" fill="#FFF8EC" fill-opacity=".9"/>
      <path d="M126 178 H274 Q258 232 264 266 Q268 322 200 330 Q132 322 136 266 Q142 232 126 178 Z" fill="{TEA}"/>
      <path d="M120 150 H280" fill="none"/>
    </g>
    <path d="M142 204 q8 -4 12 14" fill="none" stroke="#FFF1DC" stroke-width="7" stroke-linecap="round" opacity=".8"/>
    {face(200, 272, 0.9)}
    <g {ST}><rect x="262" y="124" width="26" height="26" rx="6" fill="{WHITE}" transform="rotate(14 275 137)"/></g>'''

def label_text(txt, bg, fg, size=96):
    return f'''
    <g {ST}><rect x="40" y="130" width="320" height="140" rx="70" fill="{bg}"/></g>
    <rect x="56" y="146" width="288" height="108" rx="54" fill="none" stroke="{fg}" stroke-width="3" stroke-dasharray="3 9" stroke-linecap="round" opacity=".8"/>
    <text x="200" y="228" text-anchor="middle" font-family="Readex Pro" font-weight="700" font-size="{size}" fill="{fg}" direction="rtl">{txt}</text>
    <g transform="translate(332 118) scale(.5)">{'<path d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="' + BLUSH + '" ' + ST + '/>'}</g>'''

def badge():
    return f'''
    <g {ST}><circle cx="200" cy="200" r="150" fill="{CORAL}"/></g>
    <circle cx="200" cy="200" r="128" fill="none" stroke="{CREAM}" stroke-width="4" stroke-dasharray="2 11" stroke-linecap="round"/>
    <text x="200" y="228" text-anchor="middle" font-family="Readex Pro" font-weight="700" font-size="92" fill="{CREAM}" direction="rtl">حيّاكم</text>
    <g transform="translate(200 98) scale(.62)"><path d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="{CREAM}" {ST}/></g>
    <path d="M150 304 q50 22 100 0" fill="none" stroke="{CREAM}" stroke-width="5" stroke-linecap="round"/>'''

def bean():
    return f'''
    <g transform="rotate(24 200 200)" {ST}>
      <path d="M200 52 C300 60 330 190 300 270 C270 350 130 350 100 270 C70 190 100 60 200 52 Z" fill="#7A4B33"/>
      <path d="M200 60 C170 130 232 170 200 240 C176 292 206 322 200 344" fill="none" stroke="#4B2E1F" stroke-width="6"/>
    </g>
    <path d="M120 130 q14 -30 46 -42" fill="none" stroke="#A47356" stroke-width="10" stroke-linecap="round" opacity=".8"/>
    {face(198, 216, 0.85)}'''

def hearts():
    return (f'<path transform="translate(190 224) scale(3.6)" d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="{BLUSH}" {ST.replace("4", "1.4", 1)}/>'
            f'<path transform="translate(292 130) scale(1.9)" d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="{CORAL}" {ST.replace("4", "2", 1)}/>'
            f'<path transform="translate(104 118) scale(1.5)" d="M0 14 C-34 -8 -22 -34 0 -16 C22 -34 34 -8 0 14 Z" fill="{PEACH}" {ST.replace("4", "2.4", 1)}/>')

def cocoa_scarf():  # a little round "mug-less" snow-day cloud wearing a scarf, to echo the reference
    return f'''
    <g {ST}>
      <path d="M96 250 C60 250 56 190 104 186 C100 130 176 112 204 150 C240 118 312 150 296 206 C346 206 340 266 292 266 H110 Z" fill="{CREAM}"/>
    </g>
    {face(200, 214, 0.95)}
    {knit(120, 258, 160, 36, -3)}
    <g {ST}><path d="M236 288 L262 290 L268 340 L240 336 Z" fill="{CORAL}"/></g>
    <path d="M114 100 q10 -14 26 -16" fill="none" stroke="{BEIGE}" stroke-width="7" stroke-linecap="round"/>'''

STICKERS = [
    ('01-دلة', dallah), ('02-فنجان', finjan), ('03-تمرة', date), ('04-هيل', cardamom), ('05-مارشميلو', marsh),
    ('06-نجوم', sparkles), ('07-استكانة', tea), ('08-قهوتي', lambda: label_text('قهوتي', CREAM, CORAL, 90)),
    ('09-حياكم', badge), ('10-حبة-بن', bean), ('11-قلوب', hearts), ('12-سحابة', cocoa_scarf),
    ('13-شاهي', lambda: label_text('شاهي', PEACH, BR, 90)),
]

def page():
    cells = ''.join(f'<div class="c" id="s{i}"><svg width="1000" height="1000" viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">{f()}</svg></div>' for i, (n, f) in enumerate(STICKERS))
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@700&display=swap" rel="stylesheet">
<style>body{{margin:0;background:transparent}}.c{{width:1000px;height:1000px;margin:0;display:block}}svg{{display:block}}</style></head>
<body>{cells}</body></html>'''

def render():
    os.makedirs(OUT, exist_ok=True)
    html = os.path.join(OUT, '_src.html'); open(html, 'w', encoding='utf-8').write(page())
    js = os.path.join(OUT, '_shot.js')
    open(js, 'w').write(f'''const {{ chromium }} = require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1000,height:1000}}}});
await p.goto('file://{html}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
for(let i=0;i<{len(STICKERS)};i++)await p.locator('#s'+i).screenshot({{path:'{OUT}/raw-'+i+'.png',omitBackground:true}});await b.close();}})();''')
    subprocess.run(['node', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()})
    os.remove(js); os.remove(html)

def diecut():
    from PIL import Image, ImageFilter, ImageChops
    names = []
    for i, (n, _) in enumerate(STICKERS):
        im = Image.open(os.path.join(OUT, f'raw-{i}.png')).convert('RGBA')
        bb = im.getbbox(); im = im.crop(bb)
        pad = 44; w, h = im.size
        canvas = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); canvas.alpha_composite(im, (pad, pad))
        a = canvas.split()[3].point(lambda v: 255 if v > 20 else 0)
        border = a.filter(ImageFilter.MaxFilter(41)).filter(ImageFilter.GaussianBlur(2)).point(lambda v: 255 if v > 128 else 0)
        white = Image.new('RGBA', canvas.size, (255, 255, 255, 0)); white.putalpha(border)
        white = Image.composite(Image.new('RGBA', canvas.size, (255, 255, 255, 255)), white, border)
        out = Image.alpha_composite(white, canvas)
        # soft inner edge: keep sticker art on top of the white border
        path = os.path.join(OUT, f'{n}.png'); out.save(path); names.append(path); os.remove(os.path.join(OUT, f'raw-{i}.png'))
    return names

def sheet(names):
    from PIL import Image, ImageDraw
    W, H = 2480, 3508  # A4 at 300 dpi
    ims = [Image.open(p) for p in names]
    target = 560
    ims = [im.resize((int(im.width * target / max(im.size)), int(im.height * target / max(im.size))), Image.LANCZOS) for im in ims]
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cols = 3; gx, gy = 130, 120; cw = (W - 2 * gx) // cols; rows = math.ceil(len(ims) / cols); ch = (H - 2 * gy) // rows
    random.seed(11)
    for i, im in enumerate(ims):
        r, c = divmod(i, cols)
        cx = gx + c * cw + cw // 2; cy = gy + r * ch + ch // 2
        sh.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
    sh.save(os.path.join(OUT, 'sheet-A4-transparent.png'), dpi=(300, 300))
    prev = Image.new('RGB', (W, H), (231, 240, 233)); prev.paste(sh, (0, 0), sh)
    prev.resize((W // 3, H // 3), Image.LANCZOS).save(os.path.join(OUT, 'sheet-preview.jpg'), quality=88)

def mockup(names, jug):
    from PIL import Image, ImageFilter
    import numpy as np
    base = Image.open(jug).convert('RGB'); S = 2
    base = base.resize((base.width * S, base.height * S), Image.LANCZOS)
    a = np.asarray(base).astype(int)
    body = (np.abs(a - 255).sum(axis=2) > 60)           # anything that is not the white photo background
    yy, xx = np.mgrid[0:body.shape[0], 0:body.shape[1]]
    body &= (xx < int(body.shape[1] * 0.585)) & (yy > int(body.shape[0] * 0.14)) & (yy < int(body.shape[0] * 0.955))  # the jug body only: no handle, lid or base edge
    ys, xs = np.where(body)
    random.seed(21)
    canvas = base.convert('RGBA'); placed = []
    picks = [n for n in names if not any(k in n for k in ('شاهي',))]
    for p in picks:
        st = Image.open(p).convert('RGBA'); size = random.randint(115, 165)
        st = st.resize((size, int(st.height * size / st.width)), Image.LANCZOS).rotate(random.randint(-28, 28), expand=True, resample=Image.BICUBIC)
        for _ in range(1500):
            i = random.randrange(len(xs)); cx, cy = xs[i], ys[i]
            x0, y0 = cx - st.width // 2, cy - st.height // 2
            if x0 < 0 or y0 < 0 or x0 + st.width > canvas.width or y0 + st.height > canvas.height: continue
            if not (body[y0:y0 + st.height:12, x0:x0 + st.width:12].mean() > 0.985): continue
            if any(abs(cx - px) < (st.width + pw) * 0.40 and abs(cy - py) < (st.height + ph) * 0.40 for px, py, pw, ph in placed): continue
            sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); sa = st.split()[3].point(lambda v: int(v * .30))
            tmp = Image.new('RGBA', st.size, (50, 40, 30, 0)); tmp.putalpha(sa); sh.alpha_composite(tmp, (x0 + 3, y0 + 5))
            canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(3)))
            canvas.alpha_composite(st, (x0, y0)); placed.append((cx, cy, st.width, st.height)); break
    canvas.convert('RGB').save(os.path.join(OUT, 'mockup.jpg'), quality=92)

if __name__ == '__main__':
    render(); names = diecut(); sheet(names)
    if len(sys.argv) > 1: mockup(names, sys.argv[1])
    print(len(names), 'stickers ->', os.path.abspath(OUT))
