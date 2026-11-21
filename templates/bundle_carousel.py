"""«من أعمالنا» client-work carousel (was «باقة تكمّل هوية مشروعك») (4 slides, 1080x1350) for business owners.
Photos (real Kami work, from the owner): templates/photos/bundle/1.jpg cups, 2.jpg sticker stack,
3.jpg sticker sheet (a previous client's logo is replaced by a «شعار مشروعك» placeholder), 4.jpg toppers.
Every photo is shown whole (no crop): frames take each photo's own aspect ratio.
  python3 templates/bundle_carousel.py && PAGE=bundle-carousel.html OUTDIR=out/bundle node templates/render.js
"""
import os, subprocess, json
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, 'photos/bundle')
W, H = 1080, 1350
N = 4
CREAM, BLUSH, INK, INK2, LINE = '#EDE9E0', '#E2CDCC', '#2E3B2A', '#394634', '#8A9878'


def text_png(text, out, size=62, color='#8A7D76'):
    """Render Arabic text to a transparent PNG with Chromium (correct shaping)."""
    html = os.path.join(PH, '_t.html')
    open(html, 'w', encoding='utf-8').write(f'''<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600&display=swap" rel="stylesheet">
<style>html,body{{margin:0;background:transparent}}#t{{display:inline-block;font:600 {size}px 'Readex Pro';color:{color};padding:8px;direction:rtl;line-height:1.25;text-align:center}}</style>
<span id="t">{text}</span>''')
    js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{html}',{{waitUntil:'networkidle'}});await p.evaluate(()=>document.fonts.ready);
await (await p.$('#t')).screenshot({{path:{json.dumps(out)},omitBackground:true}});await b.close()}})()'''
    subprocess.run(['node', '-e', js], check=True)
    os.remove(html)


def clean_sheet():
    """Client work shown anonymously: blur the client's round logo and phone number on the sticker sheet."""
    im = Image.open(os.path.join(PH, '3.jpg')).convert('RGB')
    cx, cy, r = 690, 1500, 178
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(6))
    im = Image.composite(im.filter(ImageFilter.GaussianBlur(22)), im, m)
    im.save(os.path.join(PH, '3-clean.jpg'), quality=95)


def collage():
    """Cover collage: row 1 cups + toppers (both 3:4), row 2 sticker stack + sheet; every photo whole."""
    g, Wc = 18, 1600
    a = [Image.open(os.path.join(PH, f)).convert('RGB') for f in ('1.jpg', '4.jpg', '2.jpg', '3-clean.jpg')]
    def row(ims):
        rs = [i.width / i.height for i in ims]
        h = round((Wc - g * (len(ims) - 1)) / sum(rs))
        return [i.resize((round(h * r), h), Image.LANCZOS) for i, r in zip(ims, rs)], h
    r1, h1 = row(a[:2]); r2, h2 = row(a[2:])
    c = Image.new('RGB', (Wc, h1 + h2 + g), CREAM)
    def paste(ims, y):
        x = 0
        for im in ims:
            m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, *im.size), 26, fill=255)
            c.paste(im, (x, y), m); x += im.width + g
    paste(r1, 0); paste(r2, h1 + g)
    c.save(os.path.join(PH, 'collage.jpg'), quality=94)


def fit(name, box_w, box_h, border=14):
    """Frame size that shows the whole photo inside box (border included), and a resized copy at exactly that size."""
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    iw, ih = box_w - 2 * border, box_h - 2 * border
    k = min(iw / im.width, ih / im.height)
    w, h = round(im.width * k), round(im.height * k)
    out = name.rsplit('.', 1)[0] + '-fit.jpg'
    im.resize((w, h), Image.LANCZOS).save(os.path.join(PH, out), quality=95, subsampling=0)
    return out, w + 2 * border, h + 2 * border


ICON = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
<path d="M11 21.73a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73z"/>
<path d="M12 22V12"/><path d="m3.3 7 7.703 4.734a2 2 0 0 0 1.994 0L20.7 7"/><path d="m7.5 4.27 9 5.15"/></svg>'''
WA = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
<path d="M3 21l1.65-3.8a9 9 0 1 1 3.4 2.9L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/></svg>'''
STAR = '<path d="M50 0 C54 34 66 46 100 50 C66 54 54 66 50 100 C46 66 34 54 0 50 C34 46 46 34 50 0Z"/>'
AR = '٠١٢٣٤٥٦٧٨٩'
ar = lambda n: ''.join(AR[int(d)] for d in str(n))


def slide(i, l1, l2, sub, img, fw, fh, swipe=False):
    top = 500
    avail = 1350 - 150 - top - (40 if swipe else 0)
    y = top + (avail - fh) // 2
    x = (W - fw) // 2
    return f'''<section class="post" id="bundle-{i:02d}">
  <svg class="st st1" viewBox="0 0 100 100">{STAR}</svg><svg class="st st2" viewBox="0 0 100 100">{STAR}</svg>
  <header><img src="../brand/logo-en-cream.png"><div class="chip">{ICON}<span>من أعمالنا</span></div></header>
  <div class="txt"><h1>{l1}<br><span class="hl">{l2}</span></h1><div class="cap">{sub}</div></div>
  <div class="card" style="left:{x}px;top:{y}px;width:{fw}px;height:{fh}px"></div>
  <div class="frame" style="left:{x}px;top:{y}px;width:{fw}px;height:{fh}px"><img src="photos/bundle/{img}"></div>
  {'<div class="swipe">اسحبوا ←</div>' if swipe else ''}
  <footer><div class="fw">{WA}<div><small>تواصل معنا عبر الواتساب</small><b>66606959</b></div></div>
  <div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(N)}</span></div></footer>
</section>'''


CSS = f'''*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#555;display:flex;flex-direction:column;gap:40px;padding:40px;font-family:'IBM Plex Sans Arabic',sans-serif}}
.post{{width:{W}px;height:{H}px;position:relative;overflow:hidden;direction:rtl;color:{INK};
  background:linear-gradient(225deg,#B2BF9D 0%,#A7B591 50%,#9CAB86 100%)}}
.st{{position:absolute}}
.st1{{width:230px;height:230px;right:-70px;top:250px;fill:#C6C4B0;opacity:.9}}
.st2{{width:640px;height:640px;left:-250px;bottom:40px;fill:#D5DCC8;opacity:.35}}
header{{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center;direction:ltr}}
header img{{height:78px}}
.chip{{display:flex;align-items:center;gap:12px;direction:rtl;font:500 28px 'IBM Plex Sans Arabic';color:{INK}}}
.chip svg{{width:38px;height:38px}}
.txt{{position:absolute;left:64px;right:64px;top:170px;text-align:center}}
h1{{font:700 76px/1.32 'Readex Pro';color:{INK}}}
.hl{{background:{BLUSH};padding:0 22px;border-radius:18px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.cap{{margin-top:18px;font:500 33px/1.5 'IBM Plex Sans Arabic';color:{INK2}}}
.card{{position:absolute;background:{BLUSH};border-radius:38px;transform:rotate(-4deg) translate(-14px,10px)}}
.frame{{position:absolute;background:{CREAM};border-radius:38px;padding:14px;box-shadow:0 24px 50px rgba(46,59,42,.22)}}
.frame img{{display:block;width:100%;height:100%;border-radius:26px}}
.swipe{{position:absolute;left:64px;bottom:136px;font:600 28px 'Readex Pro';color:{INK};direction:rtl}}
footer{{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;align-items:center;direction:ltr;
  border-top:2px solid {LINE};padding-top:22px}}
.fw{{display:flex;align-items:center;gap:14px;color:{INK}}}
.fw svg{{width:50px;height:50px}}
.fw small{{display:block;font-size:20px;color:{INK2};direction:rtl}}
.fw b{{font:600 32px 'Readex Pro';letter-spacing:1px}}
.fr{{display:flex;align-items:center;gap:18px}}
.fr .h{{font-size:26px;color:{INK}}}
.cnt{{background:{BLUSH};font:700 24px 'Readex Pro';padding:4px 20px;border-radius:30px;direction:rtl}}
'''


def main():
    clean_sheet(); collage()
    BOX = (952, 690)
    a = fit('collage.jpg', 952, 650)
    b = fit('1.jpg', *BOX)
    c = fit('3-clean.jpg', *BOX)
    d = fit('4.jpg', *BOX)
    slides = [
        slide(1, 'من أعمالنا..', 'لأحد زباينا', 'أكواب وستيكرات وتوبرز بهوية مشروعه ✦', *a, swipe=True),
        slide(2, 'أكواب..', 'بهوية المشروع', 'تصميم وطباعة وتاقات على ثيم البراند', *b),
        slide(3, 'ستيكر شيت..', 'وستيكرات بقص مرتب', 'باسم المشروع وشعاره على كل تغليفة', *c),
        slide(4, 'فكرتكم..', 'نطبعها لكم', 'اطلبوا أي ديزاين أو فكرة لمشروعكم ✦<br>حيّاكم على الواتساب 66606959', *d),
    ]
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Bundle Carousel</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{''.join(slides)}</body></html>'''
    open(os.path.join(HERE, 'bundle-carousel.html'), 'w', encoding='utf-8').write(page)
    print('ok', a, b, c, d)

main()
