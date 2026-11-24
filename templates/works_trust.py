"""Trust series from the owner's real work photos: «ليش كامي؟» (6)، «مناسبات كثيرة» collage (2)، «كيف نجهز طلبكم» (5).
Same Kami look as works_carousels.py.
  python3 templates/works_trust.py && PAGE=works-trust.html OUTDIR=out/trust node templates/render.js
"""
import os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'works_carousels2.py'), encoding='utf-8').read()
src = src[:src.index("ns['SETS']")]
g = {'__file__': os.path.join(HERE, 'works_carousels2.py'), '__name__': 'trust_lib'}
exec(compile(src, 'works_carousels2.py', 'exec'), g)
ns, prep, PH = g['ns'], g['prep'], g['PH']
g['CROP'].update({'shell-boxes': (0.8, 0.45), 'salawat': (0.8, 0.35), 'travel': (0.8, 0.35), 'cup-sleeve': (0.8, 0.5)})
photo, cta, head, foot, CSS, EXTRA = ns['photo'], ns['cta'], ns['head'], ns['foot'], ns['CSS'], ns['EXTRA']

SETS = {
 'why': ('ليش كامي؟', 6, [
   ('p', 'ليش زباينا..', 'يرجعون لنا؟', 'لأن التفاصيل الصغيرة عندنا مو صغيرة ✦', 'shell-boxes', True),
   ('p', 'تصميم على فكرتكم..', 'مو قالب جاهز', 'الاسم والخط والرسمة على ذوقكم', 'occ-stickers', False),
   ('p', 'نطبع ونقص..', 'بأيدينا', 'طباعة وقص بالكريكت، وكل قطعة تطلع مرتبة', 'school-melon', False),
   ('p', 'على أي سطح..', 'تبونه', 'ورق، شفاف، أكواب، زجاج، علب وأكياس', 'salawat', False),
   ('p', 'وكلام زباينا..', 'يشهد لنا', '«حده حلو.. مرررتب» 🤍', 'review-shell', False),
   ('c', 'جربونا..', 'وبتشوفون الفرق', 'أرسلوا فكرتكم على الواتساب 🤍'),
 ]),
 'how': ('كيف نجهز طلبكم', 5, [
   ('p', 'من فكرتكم..', 'لين تستلمونها', 'خطوات بسيطة، وكلها على الواتساب ✦', 'school-sheets', True),
   ('p', '١. ترسلون الفكرة..', 'ونصممها لكم', 'الاسم والمناسبة والثيم، وإذا عندكم صورة مثال أرسلوها', 'travel', False),
   ('p', '٢. نطبع ونقص..', 'بدقة', 'ستيكر، تاقات، فواصل، على المقاس اللي يناسبكم', 'school-croc', False),
   ('p', '٣. نغلّف ونرتب..', 'حبة حبة', 'حتى لو الطلب بالجملة، كل قطعة بنفس الترتيب', 'packed-box', False),
   ('c', 'جاهزين..', 'لطلبكم الجاي', 'أرسلوا التفاصيل على الواتساب 🤍'),
 ]),
}

TILES = [('occ-mugs', 'مواليد'), ('grad-cards', 'تخرج'), ('wed-frame', 'ملكة'),
         ('school-pencil', 'مدرسية'), ('occ-cake', 'أعياد ميلاد'), ('school-teacher', 'هدايا المعلمين'),
         ('travel', 'سفر'), ('cup-sleeve', 'ضيافة'), ('salawat', 'ستيكرات دينية')]


def tile(name, size=300):
    im = ImageOps.fit(Image.open(os.path.join(PH, name + '.jpg')).convert('RGB'), (size * 2, size * 2), Image.LANCZOS, centering=(0.5, 0.45))
    out = f'{name}-tile.jpg'; im.save(os.path.join(PH, out), quality=92)
    return out


def collage():
    cells = ''.join(f'<div class="tl"><img src="photos/works/{tile(n)}"><span>{t}</span></div>' for n, t in TILES)
    return f'''<section class="post" id="many-01">{head('من أعمالنا')}
  <div class="txt"><h1>مناسبات كثيرة..<br><span class="hl">وخبرة وحدة</span></h1><div class="cap">كل هذا طلع من عندنا ✦ اسحبوا ←</div></div>
  <div class="grid">{cells}</div>{foot(1, 2)}</section>'''


GRID = '''
.grid{position:absolute;left:168px;right:168px;top:430px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.tl{position:relative;aspect-ratio:1;border-radius:22px;overflow:hidden;background:#EDE9E0;border:8px solid #EDE9E0;box-shadow:0 10px 24px rgba(46,59,42,.14)}
.tl img{width:100%;height:100%;object-fit:cover;border-radius:14px;display:block}
.tl span{position:absolute;bottom:10px;left:50%;transform:translateX(-50%);white-space:nowrap;background:rgba(237,233,224,.94);color:#2E3B2A;font:600 24px 'Readex Pro';padding:6px 18px;border-radius:30px}
'''

out = []
for sid, (tag, n, slides) in SETS.items():
    for i, s in enumerate(slides, 1):
        out.append(photo(sid, i, n, tag, *s[1:]) if s[0] == 'p' else cta(sid, i, n, tag, *s[1:]))
out.append(collage())
out.append(cta('many', 2, 2, 'من أعمالنا', 'مناسبتكم الجاية..', 'خلوها علينا', 'أرسلوا فكرتكم على الواتساب 🤍'))
page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Trust Posts</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA}{GRID}</style></head><body>{''.join(out)}</body></html>'''
open(os.path.join(HERE, 'works-trust.html'), 'w', encoding='utf-8').write(page)
print(len(out), 'slides')
