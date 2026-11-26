"""Red shades chart: 16 swatches (light to dark) with Arabic name, HEX, RGB and approx. CMYK.
  python3 brand/colors/reds/make_reds.py && node templates/render.js-style export below (see render step in this file's folder)
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SH = [
 ('زهري فاتح', '#F8C8C8'), ('مرجاني فاتح', '#F08080'), ('سلموني', '#FA8072'), ('مرجاني', '#FF6F61'),
 ('طماطي', '#FF6347'), ('أحمر ناري', '#FF2400'), ('أحمر صافي', '#FF0000'), ('قرمزي', '#DC143C'),
 ('كرزي', '#D2042D'), ('أحمر فراولي', '#C72C48'), ('طوبي', '#B22222'), ('نبيتي', '#9B1B30'),
 ('توتي', '#8E2443'), ('عنابي', '#800020'), ('ماروني', '#800000'), ('أحمر داكن', '#4A0404'),
]
def cmyk(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5))
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    return tuple(round(x * 100) for x in ((1-r-k)/(1-k), (1-g-k)/(1-k), (1-b-k)/(1-k), k))
def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
cells = ''
for i, (n, h) in enumerate(SH, 1):
    c = cmyk(h); r = rgb(h)
    cells += f'''<div class="sw"><div class="chip" style="background:{h}"><span>{i:02d}</span></div>
<b>{n}</b><code>{h}</code><small>RGB {r[0]}, {r[1]}, {r[2]}</small><small>CMYK {c[0]}, {c[1]}, {c[2]}, {c[3]}</small></div>'''
page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>درجات الأحمر</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@500;600&family=IBM+Plex+Mono:wght@500&display=block" rel="stylesheet">
<style>@page{{size:210mm 297mm;margin:0}}*{{margin:0;padding:0;box-sizing:border-box}}
body{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:210mm;height:297mm;background:#F3EFE6;padding:14mm 13mm 10mm;display:flex;flex-direction:column;color:#2E3B2A;font-family:'IBM Plex Sans Arabic'}}
h1{{font:700 13mm 'Readex Pro';text-align:center}}
.sub{{text-align:center;font-size:3.8mm;color:#394634;margin-top:2mm}}
.grid{{flex:1;display:grid;grid-template-columns:repeat(4,1fr);gap:5mm 5mm;margin-top:8mm}}
.sw{{display:flex;flex-direction:column;align-items:center;text-align:center}}
.chip{{width:100%;aspect-ratio:1.25;border-radius:3mm;position:relative;box-shadow:0 .6mm 1.6mm rgba(46,59,42,.18)}}
.chip span{{position:absolute;top:2mm;left:2.4mm;font:500 3mm 'IBM Plex Mono';color:rgba(255,255,255,.85)}}
b{{font:600 4.2mm 'Readex Pro';margin-top:2.2mm}}
code{{font:500 3.4mm 'IBM Plex Mono';direction:ltr;margin-top:.6mm}}
small{{font:500 2.7mm 'IBM Plex Mono';direction:ltr;color:#5a6455;margin-top:.3mm}}
.ft{{display:flex;justify-content:space-between;align-items:center;font-size:3mm;color:#394634;border-top:.3mm solid rgba(46,59,42,.25);padding-top:3mm;margin-top:4mm}}
.ft img{{height:8mm}}
</style></head><body><div class="p">
<h1>درجات الأحمر</h1>
<div class="sub">من الفاتح للغامق ✦ اختاروا الرقم وأرسلوه لنا</div>
<div class="grid">{cells}</div>
<div class="ft"><span>الألوان على الشاشة تختلف شوي عن الطباعة حسب الورق</span><img src="../../logo-ar-green.png"><span dir="ltr">@kami.printing · 66606959</span></div>
</div></body></html>'''
open(os.path.join(HERE, 'reds.html'), 'w', encoding='utf-8').write(page)
print('ok')
