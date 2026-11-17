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

# Theme from the local design index (فهرس-التصاميم.md): sage gradient #B2BF9D -> #9CAB86 with two
# four-point stars, Readex Pro 700 headings, IBM Plex Sans Arabic body, #2E3B2A text, #394634 secondary,
# cream #EDE9E0, blush highlight #E2CDCC. Logo top-left, section title top-right, footer with page count.
# Note from the index: avoid «في» in Readex headings (the ي loses its dots).
# (photo file, title, sub, object-position)
PHOTOS = [
    ('logo-stickers-wide', 'ستيكرات [[الشعار]]', 'بقص احترافي، تختمون فيها كل كيس وعلبة', '50% 60%'),
    ('uv-stickers-wide', 'ستيكرات [[UV]]', 'لمعة بارزة تعطي منتجكم طابع فخم', '50% 55%'),
    ('thank-cards', 'بطاقات [[الشكر]]', 'مع كل طلبية، ومكان تكتبون فيه اسم زبونكم', '50% 55%'),
    ('business-cards', '[[بزنس كارد]]', 'حساباتكم ورقمكم بيد زبونكم دايماً', '50% 50%'),
    ('cotton-labels', 'قصاصات [[قطنية]]', 'لمسة أنيقة لمشاريع الملابس والإكسسوارات', '50% 40%'),
    ('folding-boxes', 'علب [[مطوية]]', 'تغليف يعطي كل منتج تبيعونه طابع فخم', '50% 50%'),
]
N = 3 + len(PHOTOS) + 1

def head():
    return f'<header><img src="../brand/logo-en-cream.png"><div class="chip">{icon(TAGIC)}<span>{TAG}</span></div></header>'

def foot(i):
    return f'''<footer><div class="fw">{icon("wa", "fwi")}<div><small>تواصل معنا عبر الواتساب</small><b>66606959</b></div></div>
  <div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(N)}</span></div></footer>'''

STARS = '<svg class="wm"><use href="#star"/></svg><svg class="wm2"><use href="#star"/></svg>'

def frame(src, pos):
    return f'<div class="frame"><img src="photos/packaging/{src}.jpg" style="object-position:{pos}"></div>'

def cover(i):
    return f'''<section class="post ph cov" id="pack-{i:02d}">{STARS}{head()}
  <div class="txt"><h1>مشروعكم يحتاج<br>{hl("[[هالمطبوعات]]")}</h1><div class="cap">تفاصيل صغيرة.. تخلي طلبياتكم أفخم</div></div>
  {frame("unbox-wide", "50% 50%")}
  <div class="swipe">اسحبوا<svg viewBox="0 0 120 50"><path d="M110 10 C80 40 40 40 12 26"/><path d="M26 14 L10 26 L28 36"/></svg></div>
  {foot(i)}</section>'''

def stake(i):
    return f'''<section class="post stk" id="pack-{i:02d}">{STARS}{head()}
  <main><div class="mas">{mascot("gift", "open")}</div>
  <h1 class="t-cover">أول شي يشوفه زبونكم..<br>{hl("[[التغليف]]")}</h1>
  <div class="sub">قبل لا يجرّب منتجكم، يحكم عليه من شكله</div></main>
  {foot(i)}</section>'''

def photo(i, name, title, sub, pos):
    return f'''<section class="post ph" id="pack-{i:02d}">{STARS}{head()}
  <div class="txt"><h2>{hl(title)}</h2><div class="cap">{sub}</div></div>
  {frame(name, pos)}
  {foot(i)}</section>'''

CSS = ns['CSS'] + '''
.post{background:linear-gradient(165deg,#B2BF9D 0%,#A7B591 50%,#9CAB86 100%)}
h1,h2,.t-cover,.t-cta,.ftt,.kicker,.chip,.pill,.cnt,.fw b,.gh,.q,.sn,.wa span{font-family:'Readex Pro','IBM Plex Sans Arabic',sans-serif!important}
h1,h2{font-weight:700}
.ph .txt{position:absolute;left:64px;right:64px;top:168px;text-align:center;display:flex;flex-direction:column;align-items:center}
.ph h2{font-size:80px;margin:0;line-height:1.3}
.ph.cov h1{font-size:78px;margin:0;line-height:1.35}
.ph .cap{margin-top:18px;color:#394634;font-size:34px;font-weight:500}
.frame{position:absolute;left:64px;right:64px;top:430px;bottom:196px;border-radius:40px;overflow:hidden;
  border:10px solid var(--cream);box-shadow:0 24px 50px rgba(46,59,42,.22)}
.frame img{width:100%;height:100%;object-fit:cover;display:block}
.cov .frame{top:520px;bottom:250px}
.cov .swipe{position:absolute;left:64px;bottom:190px;display:flex;align-items:center;gap:6px;font-family:'Readex Pro';font-size:28px;color:var(--forest);direction:rtl}
.cov .swipe svg{width:120px;height:50px;fill:none;stroke:var(--forest);stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round}
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
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=Alexandria:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{ns["defs"]}</svg>
{''.join(out)}</body></html>'''
    open(os.path.join(HERE, 'packaging-carousel.html'), 'w', encoding='utf-8').write(page)
    print(len(out), 'slides')

main()
