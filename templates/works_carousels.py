"""«من أعمالنا» carousels from the owner's real work photos (templates/photos/works/), Kami theme.
Three carousels: مواليد، تخرج، ملكة وعرس. Reuses the bundle_carousel look (sage, Readex, cream frame + tilted blush card).
  python3 templates/works_carousels.py && PAGE=works-carousels.html OUTDIR=out/works node templates/render.js
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'bundle_carousel.py'), encoding='utf-8').read()
src = src[:src.rindex('main()')]
ns = {'__file__': os.path.join(HERE, 'bundle_carousel.py'), '__name__': 'bundle_lib'}
exec(compile(src, 'bundle_carousel.py', 'exec'), ns)
CSS, STAR, WA, ar = ns['CSS'], ns['STAR'], ns['WA'], ns['ar']
PH = os.path.join(HERE, 'photos/works')
GIFT = '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C9 3 12 8 12 8s3-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>'''


def prep(name, box=(952, 720), border=14, max_ratio=0.8):
    """Crop very tall/wide phone shots toward 4:5 / 4:3 (centre), then size to fit the frame box."""
    im = Image.open(os.path.join(PH, name + '.jpg')).convert('RGB')
    r = im.width / im.height
    if r < max_ratio:  # too tall
        h = round(im.width / max_ratio); y = (im.height - h) // 2
        im = im.crop((0, y, im.width, y + h))
    elif r > 4 / 3:
        w = round(im.height * 4 / 3); x = (im.width - w) // 2
        im = im.crop((x, 0, x + w, im.height))
    iw, ih = box[0] - 2 * border, box[1] - 2 * border
    k = min(iw / im.width, ih / im.height)
    w, h = round(im.width * k), round(im.height * k)
    out = f'{name}-fit.jpg'
    im.resize((w, h), Image.LANCZOS).save(os.path.join(PH, out), quality=94, subsampling=0)
    return out, w + 2 * border, h + 2 * border


def head(tag):
    return (f'<svg class="st st1" viewBox="0 0 100 100">{STAR}</svg><svg class="st st2" viewBox="0 0 100 100">{STAR}</svg>'
            f'<header><img src="../brand/logo-en-cream.png"><div class="chip">{GIFT}<span>{tag}</span></div></header>')


def foot(i, n):
    return (f'<footer><div class="fw">{WA}<div><small>تواصل معنا عبر الواتساب</small><b>66606959</b></div></div>'
            f'<div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(n)}</span></div></footer>')


def photo(sid, i, n, tag, l1, l2, sub, img, swipe=False):
    f, fw, fh = prep(img)
    top = 470; avail = 1350 - 150 - top - (40 if swipe else 0)
    y = top + (avail - fh) // 2; x = (1080 - fw) // 2
    return f'''<section class="post" id="{sid}-{i:02d}">{head(tag)}
  <div class="txt"><h1>{l1}<br><span class="hl">{l2}</span></h1><div class="cap">{sub}</div></div>
  <div class="card" style="left:{x}px;top:{y}px;width:{fw}px;height:{fh}px"></div>
  <div class="frame" style="left:{x}px;top:{y}px;width:{fw}px;height:{fh}px"><img src="photos/works/{f}"></div>
  {'<div class="swipe">اسحبوا ←</div>' if swipe else ''}{foot(i, n)}</section>'''


def cta(sid, i, n, tag, l1, l2, sub):
    return f'''<section class="post" id="{sid}-{i:02d}">{head(tag)}
  <div class="ctab"><svg class="spark" viewBox="0 0 100 100">{STAR}</svg><h1>{l1}<br><span class="hl">{l2}</span></h1>
  <div class="cap">{sub}</div><div class="wapill">{WA}<span>66606959</span></div>
  <img class="arlogo" src="../brand/logo-ar-cream.png"></div>{foot(i, n)}</section>'''


EXTRA = '''
.txt{top:160px}
h1{font-size:72px}
.ctab{position:absolute;left:64px;right:64px;top:300px;text-align:center;display:flex;flex-direction:column;align-items:center}
.ctab .spark{width:70px;height:70px;fill:#EDE9E0;margin-bottom:30px}
.ctab h1{font-size:84px}
.wapill{margin-top:60px;display:flex;align-items:center;gap:22px;background:#2E3B2A;color:#EDE9E0;border-radius:70px;padding:22px 70px;direction:ltr}
.wapill svg{width:64px;height:64px}
.wapill span{font:700 74px 'Readex Pro';letter-spacing:2px}
.arlogo{margin-top:70px;width:240px;opacity:.95}
'''

SETS = {
 'baby': ('توزيعات المواليد', 6, [
   ('p', 'من أعمالنا..', 'توزيعات المواليد', 'باسم مولودكم وعلى ثيم مناسبتكم ✦', 'baby-cups', True),
   ('p', 'ستيكر دائري..', 'برسمة واسم', 'رسمة ناعمة واسم المولود بالعربي والإنجليزي', 'baby-sticker', False),
   ('p', 'علب أسطوانية..', 'بنفس الثيم', 'نغلّف العلب بنفس تصميم الأكواب والستيكر', 'baby-tubes', False),
   ('p', 'تاق صغير..', 'باسم المولود', 'ورق بحواف مقصوصة يكمّل التوزيعة', 'baby-tag', False),
   ('p', 'وكلمة..', 'تفرّح أهلها', 'قصاصات بعبارات على ذوقكم', 'baby-note', False),
   ('c', 'مولودكم الجاي..', 'توزيعته علينا', 'أرسلوا الاسم والثيم على الواتساب 🤍'),
 ]),
 'grad': ('التخرج', 4, [
   ('p', 'من أعمالنا..', 'لمسات التخرج', 'كروت بصورة الخريج، وقصاصات بعبارتكم ✦', 'grad-cards', True),
   ('p', 'عبارة تخرجك..', 'بين يدينك', 'قصاصات بحواف مقصوصة وخط عربي أنيق', 'grad-quote', False),
   ('p', 'وكرت صغير..', 'يزيّن الورد', 'Officially Graduated بخط يدوي فوق باقة الورد', 'grad-flowers', False),
   ('c', 'خريج السنة..', 'نجهز له فرحته', 'أرسلوا الاسم والصورة والعبارة 🎓'),
 ]),
 'wed': ('الملكة والعرس', 4, [
   ('p', 'من أعمالنا..', 'لمسات الملكة', 'تفاصيل صغيرة تكمّل أحلى يوم ✦', 'wed-frame', True),
   ('p', 'قصاصة بعبارة..', 'من القلب', '«يا خير من اختاره الله لي» على ورق بحواف مقصوصة', 'wed-quote', False),
   ('p', 'وأكواب القهوة..', 'بستيكر الثيم', 'ستيكر بقص يمشي مع ألوان مناسبتكم', 'wed-cups', False),
   ('c', 'ملكتكم قريبة؟', 'التفاصيل علينا', 'أرسلوا التاريخ والثيم على الواتساب 🤍'),
 ]),
}


def main():
    out = []
    for sid, (tag, n, slides) in SETS.items():
        for i, s in enumerate(slides, 1):
            out.append(photo(sid, i, n, tag, *s[1:]) if s[0] == 'p' else cta(sid, i, n, tag, *s[1:]))
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Works Carousels</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA}</style></head><body>{''.join(out)}</body></html>'''
    open(os.path.join(HERE, 'works-carousels.html'), 'w', encoding='utf-8').write(page)
    print(len(out), 'slides')

main()
