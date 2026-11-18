"""Realistic Bahrain winter-camp (مخيم شتوي) sticker set for a dalla: photo cutouts + round photo badges + phrase stickers.
Photos: Pexels (free licence, ids in brand/stickers/winter-camp/حقوق-الصور.txt). Cutouts: hyperframes remove-background (free).
Run:  python3 templates/winter_camp_stickers.py <photos_dir> <dalla_photo.jpg>
      photos_dir holds p<ID>.jpg downloads (see PHOTOS below)."""
import os, subprocess, sys, math, random, shutil
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'brand', 'stickers', 'winter-camp')
ENV = {**os.environ, 'NODE_USE_ENV_PROXY': '1', 'NODE_EXTRA_CA_CERTS': '/root/.ccr/ca-bundle.crt', 'NODE_NO_WARNINGS': '1'}

# name, photo id, crop box (fractions), kind ('cut' = background removed, 'round' / 'oval' = photo badge)
PHOTOS = [
    ('دلة-ذهبية', 7102302, (0.08, 0.68, 0.78, 0.98), 'cut'),
    ('جمل-واقف', 1718258, (0.0, 0.0, 1.0, 1.0), 'cut'),
    ('مبخرة', 17860048, (0.10, 0.0, 0.95, 0.98), 'cut'),
    ('فانوس', 2233416, (0.18, 0.25, 0.52, 0.98), 'cut'),
    ('شبّة-الليل', 3099106, (0.10, 0.40, 1.0, 1.0), 'round'),
    ('كثبان-الغروب', 18166240, (0.18, 0.0, 0.78, 1.0), 'round'),
    ('ليل-الصحراء', 5058588, (0.22, 0.05, 0.78, 1.0), 'round'),
    ('قافلة', 3121285, (0.15, 0.20, 0.85, 1.0), 'round'),
    ('صب-القهوة', 30146018, (0.20, 0.0, 1.0, 0.95), 'oval'),
]
NAVY, EMBER, SAND, GOLD, CREAM, CHAR, BROWN = '#17233F', '#E0702B', '#EAD5B0', '#E8B14B', '#FBF1DF', '#2A2522', '#5A3A24'
PHRASES = [  # text, background, text colour, accent, shape
    ('كشتة الشتا', NAVY, GOLD, EMBER, 'pill'), ('ريحة الجمر والهيل', SAND, BROWN, EMBER, 'pill'),
    ('شتاء البحرين', EMBER, CREAM, NAVY, 'round'), ('قهوة وسوالف', CREAM, CHAR, EMBER, 'pill'),
    ('برد الليل<br>ودفا السوالف', NAVY, CREAM, GOLD, 'round'), ('يا هلا بالشتا', GOLD, NAVY, EMBER, 'pill'),
    ('سمر الشبّة', CHAR, EMBER, GOLD, 'pill'), ('دلّة الأحباب', SAND, BROWN, NAVY, 'round'),
]

def crop(src, box):
    im = Image.open(src).convert('RGB'); w, h = im.size
    return im.crop(tuple(int(v) for v in (box[0] * w, box[1] * h, box[2] * w, box[3] * h)))

def cutout(im, name, work):
    p = os.path.join(work, name + '.jpg'); o = os.path.join(work, name + '.png'); im.save(p, quality=95)
    subprocess.run(['hyperframes', 'remove-background', p, '-o', o], check=True, capture_output=True, env=ENV)
    return Image.open(o).convert('RGBA')

def badge(im, shape):
    w, h = im.size
    if shape == 'round':
        s = min(w, h); im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)); size = (900, 900)
    else:
        size = (1000, 700); r = size[0] / size[1]
        cw, ch = (w, int(w / r)) if w / h < r else (int(h * r), h)
        im = im.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2))
    im = im.resize(size, Image.LANCZOS).convert('RGBA')
    m = Image.new('L', size, 0); d = ImageDraw.Draw(m)
    d.ellipse((0, 0, size[0] - 1, size[1] - 1), fill=255) if shape in ('round', 'oval') else None
    im.putalpha(m.filter(ImageFilter.GaussianBlur(1.2)))
    ring = Image.new('RGBA', size, (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((10, 10, size[0] - 11, size[1] - 11), outline=(255, 255, 255, 235), width=7)
    return Image.alpha_composite(im, ring)

def phrase_page():
    cells = ''
    for i, (t, bg, fg, ac, shp) in enumerate(PHRASES):
        cls = 'pill' if shp == 'pill' else 'round'
        cells += f'<div class="s {cls}" id="p{i}" style="background:{bg};color:{fg};--ac:{ac}"><i class="o"></i><span class="t">{t}</span><b class="d">✦</b></div>'
    return f'''<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Aref+Ruqaa:wght@700&family=Readex+Pro:wght@600&display=swap" rel="stylesheet">
<style>body{{margin:0;background:transparent;display:flex;flex-direction:column;gap:30px;padding:30px}}
.s{{box-sizing:border-box;position:relative;display:flex;align-items:center;justify-content:center;text-align:center;font-family:'Aref Ruqaa','Readex Pro';font-weight:700;line-height:1.35;box-shadow:inset 0 0 0 8px rgba(255,255,255,.0)}}
.pill{{width:1000px;height:360px;border-radius:180px;font-size:150px}}
.round{{width:760px;height:760px;border-radius:50%;font-size:132px;padding:0 110px}}
.o{{position:absolute;inset:26px;border:6px dashed var(--ac);border-radius:inherit;opacity:.85}}
.d{{position:absolute;top:34px;color:var(--ac);font-size:60px;font-family:'Readex Pro'}}
.pill .d{{right:130px}} .round .d{{top:64px;font-size:48px}}
.t{{position:relative;z-index:1}}</style></head><body>{cells}</body></html>'''

def render_phrases(work):
    html = os.path.join(work, 'phr.html'); open(html, 'w', encoding='utf-8').write(phrase_page())
    js = os.path.join(work, 'phr.js')
    open(js, 'w').write(f'''const {{ chromium }} = require('playwright');
(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1100,height:1100}}}});
await p.goto('file://{html}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(600);
for(let i=0;i<{len(PHRASES)};i++)await p.locator('#p'+i).screenshot({{path:'{work}/ph'+i+'.png',omitBackground:true}});await b.close();}})();''')
    subprocess.run(['node', js], check=True, env={**ENV, 'NODE_PATH': subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()})
    return [Image.open(os.path.join(work, f'ph{i}.png')).convert('RGBA') for i in range(len(PHRASES))]

def diecut(im, pad=46, width=41):
    bb = im.getbbox(); im = im.crop(bb); w, h = im.size
    cv = Image.new('RGBA', (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); cv.alpha_composite(im, (pad, pad))
    a = cv.split()[3].point(lambda v: 255 if v > 24 else 0)
    border = a.filter(ImageFilter.MaxFilter(width)).filter(ImageFilter.GaussianBlur(2.2)).point(lambda v: 255 if v > 120 else 0)
    white = Image.new('RGBA', cv.size, (255, 255, 255, 255)); white.putalpha(border)
    return Image.alpha_composite(white, cv)

def main(photos, dalla):
    os.makedirs(OUT, exist_ok=True); work = os.path.join(OUT, '_work'); os.makedirs(work, exist_ok=True)
    stickers = []
    for name, pid, box, kind in PHOTOS:
        im = crop(os.path.join(photos, f'p{pid}.jpg'), box)
        art = cutout(im, name, work) if kind == 'cut' else badge(im, kind)
        stickers.append((name, diecut(art)))
    for i, art in enumerate(render_phrases(work)):
        stickers.append((f'عبارة-{i + 1}', diecut(art, pad=40, width=35)))
    names = []
    for n, im in stickers:
        im.save(os.path.join(OUT, f'{n}.png')); names.append((n, im))
    shutil.rmtree(work)
    # A4 transparent sheet (300 dpi), packed in rows
    W, H = 2480, 3508
    def layout(k):
        sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0)); x = y = 110; rowh = 0
        for n, im in names:
            sc = (k * 620 if 'عبارة' not in n else k * 720) / max(im.size)
            t = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
            if x + t.width > W - 110: x = 110; y += rowh + 60; rowh = 0
            sheet.alpha_composite(t, (x, y)); x += t.width + 60; rowh = max(rowh, t.height)
        return sheet, y + rowh
    k = 1.0
    while True:
        sheet, bottom = layout(k)
        if bottom <= H - 110 or k < 0.4: break
        k -= 0.04
    sheet.save(os.path.join(OUT, 'sheet-A4-transparent.png'), dpi=(300, 300))
    prev = Image.new('RGB', (W, H), (236, 232, 222)); prev.paste(sheet, (0, 0), sheet); prev.resize((W // 3, H // 3), Image.LANCZOS).save(os.path.join(OUT, 'sheet-preview.jpg'), quality=88)
    mockup(names, dalla)
    open(os.path.join(OUT, 'حقوق-الصور.txt'), 'w', encoding='utf-8').write(
        'الصور من Pexels (رخصة Pexels المجانية: استخدام وتعديل بدون ذكر المصدر). أرقام الصور:\n' + '\n'.join(f'{n}: pexels.com/photo/{pid}' for n, pid, _, _ in PHOTOS) +
        '\nملاحظة: للبيع التجاري للستيكرات راجع شروط Pexels لكل صورة (ممنوع بيع الصورة كما هي بدون تعديل).\n')
    print(len(names), 'stickers ->', os.path.abspath(OUT))

def mockup(names, dalla):
    import numpy as np
    base = Image.open(dalla).convert('RGB'); S = 2; base = base.resize((base.width * S, base.height * S), Image.LANCZOS)
    a = np.asarray(base).astype(int); body = (np.abs(a - 255).sum(axis=2) > 60)
    yy, xx = np.mgrid[0:body.shape[0], 0:body.shape[1]]
    body &= (xx < int(body.shape[1] * 0.585)) & (yy > int(body.shape[0] * 0.14)) & (yy < int(body.shape[0] * 0.955))
    ys, xs = np.where(body); random.seed(8); canvas = base.convert('RGBA'); placed = []
    order = [n for n in names if 'عبارة' not in n[0]] + [n for n in names if 'عبارة' in n[0]][:4]
    for n, st in order:
        size = random.randint(135, 175) if 'عبارة' not in n else random.randint(150, 195)
        st = st.resize((size, int(st.height * size / st.width)), Image.LANCZOS).rotate(random.randint(-22, 22), expand=True, resample=Image.BICUBIC)
        for _ in range(2500):
            i = random.randrange(len(xs)); cx, cy = xs[i], ys[i]; x0, y0 = cx - st.width // 2, cy - st.height // 2
            if x0 < 0 or y0 < 0 or x0 + st.width > canvas.width or y0 + st.height > canvas.height: continue
            if body[y0:y0 + st.height:12, x0:x0 + st.width:12].mean() < 0.985: continue
            if any(abs(cx - px) < (st.width + pw) * 0.40 and abs(cy - py) < (st.height + ph) * 0.40 for px, py, pw, ph in placed): continue
            sh = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); tmp = Image.new('RGBA', st.size, (40, 30, 20, 0)); tmp.putalpha(st.split()[3].point(lambda v: int(v * .32)))
            sh.alpha_composite(tmp, (x0 + 3, y0 + 5)); canvas = Image.alpha_composite(canvas, sh.filter(ImageFilter.GaussianBlur(3)))
            canvas.alpha_composite(st, (x0, y0)); placed.append((cx, cy, st.width, st.height)); break
    canvas.convert('RGB').save(os.path.join(OUT, 'mockup.jpg'), quality=92)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
