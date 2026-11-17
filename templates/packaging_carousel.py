"""Build templates/packaging-carousel.html: «مشروعكم يحتاج هالمطبوعات» carousel.
Product photo slides + the shared Kami carousel system from carousels.py.
Render:
  python3 templates/packaging_carousel.py && PAGE=packaging-carousel.html OUTDIR=out/packaging node templates/render.js
Photos live in templates/photos/packaging/.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'carousels.py'), encoding='utf-8').read()
src = src[:src.rindex('main()')]  # reuse CSS, icons, slide() without writing carousels.html
cwd = os.getcwd(); os.chdir(HERE)
ns = {'__file__': os.path.join(HERE, 'carousels.py'), '__name__': 'carousels_lib'}
exec(compile(src, 'carousels.py', 'exec'), ns)
os.chdir(cwd)
hl, icon, ar, slide, mascot = ns['hl'], ns['icon'], ns['ar'], ns['slide'], ns['mascot']
TAG, TAGIC = 'لمشروعكم', 'tag'

# (photo, title, sub, text position: top|bottom)
PHOTOS = [
    ('logo-stickers', 'ستيكرات [[الشعار]]', 'بقص احترافي، تختمون فيها كل كيس وعلبة', 'top'),
    ('uv-stickers', 'ستيكرات [[UV]]', 'لمعة بارزة تعطي منتجكم طابع فخم', 'bottom'),
    ('thank-cards', 'بطاقات [[الشكر]]', 'مع كل طلبية، ومكان تكتبون فيه اسم زبونكم', 'top'),
    ('business-cards', '[[بزنس كارد]]', 'حساباتكم ورقمكم في يد زبونكم دايماً', 'top'),
    ('cotton-labels', 'قصاصات [[قطنية]]', 'لمسة أنيقة لمشاريع الملابس والإكسسوارات', 'bottom'),
    ('folding-boxes', 'علب [[مطوية]]', 'تغليف يعطي كل منتج تبيعونه طابع فخم', 'top'),
]
N = 3 + len(PHOTOS) + 1

def head():
    return f'<header><img src="../brand/logo-en-cream.png"><div class="chip">{icon(TAGIC)}<span>{TAG}</span></div></header>'

def foot(i):
    return f'''<footer><div class="fw">{icon("wa", "fwi")}<div><small>تواصل معنا عبر الواتساب</small><b>66606959</b></div></div>
  <div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(N)}</span></div></footer>'''

def cover(i):
    return f'''<section class="post ph cov" id="pack-{i:02d}" style="--img:url(photos/packaging/unbox.jpg)">
  <div class="tint"></div>{head()}
  <main><svg class="spark"><use href="#star"/></svg>
  <h1 class="t-cover">مشروعكم يحتاج<br>[[هالمطبوعات]]</h1>
  <div class="sub">تفاصيل صغيرة.. تخلي طلبياتكم أفخم</div>
  <div class="swipe">اسحبوا<svg viewBox="0 0 120 50"><path d="M110 10 C80 40 40 40 12 26"/><path d="M26 14 L10 26 L28 36"/></svg></div></main>
  {foot(i)}</section>'''.replace('[[هالمطبوعات]]', '<span class="hl">هالمطبوعات</span>')

def stake(i):
    return f'''<section class="post stk" id="pack-{i:02d}">
  <svg class="wm"><use href="#star"/></svg><svg class="wm2"><use href="#star"/></svg>{head()}
  <main><div class="mas">{mascot("gift", "open")}</div>
  <h1 class="t-cover">أول شي يشوفه زبونكم..<br>{hl("[[التغليف]]")}</h1>
  <div class="sub">قبل لا يجرّب منتجكم، يحكم عليه من شكله</div></main>
  {foot(i)}</section>'''

def photo(i, name, title, sub, pos):
    return f'''<section class="post ph {pos}" id="pack-{i:02d}" style="--img:url(photos/packaging/{name}.jpg)">
  <div class="scrim"></div>{head()}
  <div class="txt"><h2>{hl(title)}</h2><div class="cap">{sub}</div></div>
  {foot(i)}</section>'''

CSS = ns['CSS'] + '''
.ph{background:var(--img) center/cover}
.ph header img{filter:brightness(0) saturate(100%) invert(19%) sepia(10%) saturate(1200%) hue-rotate(60deg) brightness(.9)}
.ph .scrim{position:absolute;inset:0;pointer-events:none}
.ph.top .scrim{background:linear-gradient(180deg,rgba(237,233,224,.96) 0%,rgba(237,233,224,.82) 26%,rgba(237,233,224,0) 46%),linear-gradient(0deg,rgba(237,233,224,.9) 0%,rgba(237,233,224,0) 16%)}
.ph.bottom .scrim{background:linear-gradient(180deg,rgba(237,233,224,.85) 0%,rgba(237,233,224,0) 14%),linear-gradient(0deg,rgba(237,233,224,.97) 0%,rgba(237,233,224,.85) 28%,rgba(237,233,224,0) 48%)}
.ph .txt{position:absolute;left:64px;right:64px;text-align:center;display:flex;flex-direction:column;align-items:center}
.ph.top .txt{top:170px}.ph.bottom .txt{bottom:190px}
.ph h2{font-size:86px;margin:0}
.ph .cap{margin-top:22px;background:var(--forest);color:var(--cream);font-size:34px;font-weight:500;padding:12px 38px;border-radius:50px}
.ph footer{border-top-color:rgba(46,59,42,.25)}
.cov .tint{position:absolute;inset:0;background:linear-gradient(180deg,rgba(46,59,42,.55),rgba(46,59,42,.35) 45%,rgba(46,59,42,.7));}
.cov header img{filter:none}.cov .chip{color:var(--cream)}.cov .chip svg{stroke:var(--cream)}
.cov main{color:var(--cream)}.cov .t-cover{font-size:96px;color:var(--cream);text-shadow:0 4px 30px rgba(0,0,0,.25)}
.cov .hl{color:var(--forest)}.cov .sub{color:var(--cream);opacity:1}
.cov .spark{width:90px;height:90px;fill:var(--blush);margin-bottom:30px}
.cov .swipe,.cov .swipe svg{color:var(--cream);stroke:var(--cream)}
.cov footer{border-top-color:rgba(237,233,224,.4)}.cov footer,.cov .fw b{color:var(--cream)}.cov .fwi{stroke:var(--cream)}
.cov .fr .h{color:var(--cream)}
.stk .mas svg{width:520px}
'''

def main():
    out = [cover(1), stake(2)]
    for k, p in enumerate(PHOTOS):
        out.append(photo(3 + k, *p))
    i = 3 + len(PHOTOS)
    out.append(slide('school', TAG, TAGIC, {'type': 'grid', 'kicker': 'الملخص', 'title': 'كل اللي يحتاجه [[مشروعكم]]', 'items': [
        ('sticker', 'ستيكرات الشعار'), ('uv', 'ستيكرات UV'), ('letter', 'بطاقات الشكر'),
        ('card', 'بزنس كارد'), ('cotton', 'قصاصات قطنية'), ('gift', 'علب مطوية')],
        'pill': 'كلها بشعار مشروعكم وألوانه'}, i, N).replace('id="school-', 'id="pack-'))
    out.append(slide('school', TAG, TAGIC, {'type': 'cta', 'title': 'احفظوا البوست..<br>[[وأرسلوا لنا شعاركم]]',
        'sub': 'ونجهز لكم مطبوعات مشروعكم'}, i + 1, N).replace('id="school-', 'id="pack-'))
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Packaging Carousel</title>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{ns["defs"]}</svg>
{''.join(out)}</body></html>'''
    open(os.path.join(HERE, 'packaging-carousel.html'), 'w', encoding='utf-8').write(page)
    print(len(out), 'slides')

main()
