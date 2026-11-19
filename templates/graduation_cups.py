"""Custom cups & saucers carousel (photo, name or any design; graduation is one example) (4 slides, 1080x1350), editorial photo style.
Photos: AI mockups (ElevenLabs Seedream 5 Lite) in templates/photos/graduation/: g1-ar.png is g1 with the
misspelled English saucer text removed and «مبروك التخرج» (Amiri) printed along the rim.
Saucer text on g1-ar.png: python3 templates/saucer_text.py <text.png> (Amiri 400, along the front rim).
Render:
  python3 templates/graduation_cups.py && PAGE=graduation-cups.html OUTDIR=out/graduation node templates/render.js
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PH = os.path.join(HERE, 'photos/graduation')
src = open(os.path.join(HERE, 'carousels.py'), encoding='utf-8').read()
src = src[:src.rindex('main()')]
cwd = os.getcwd(); os.chdir(HERE)
ns = {'__file__': os.path.join(HERE, 'carousels.py'), '__name__': 'carousels_lib'}
exec(compile(src, 'carousels.py', 'exec'), ns)
os.chdir(cwd)
hl, icon, ar = ns['hl'], ns['icon'], ns['ar']


def crop(name, x0, out, size=(1080, 1350)):
    """4:5 crop starting at x0 from a 2560x1440 photo, resized once with Lanczos to the exact slide size."""
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    w = round(im.height * size[0] / size[1])
    im.crop((x0, 0, x0 + w, im.height)).resize(size, Image.LANCZOS).save(os.path.join(PH, out), quality=95, subsampling=0)


crop('g2.png', 520, 's1.jpg')
crop('g1-ar.png', 680, 's2.jpg')
crop('g3.png', 1150, 's3.jpg')
FW, FH = 952 - 24, 535 - 24  # CTA frame inner size (16:9-ish)
Image.open(os.path.join(PH, 'g3.png')).convert('RGB').resize((FW, round(FW * 1440 / 2560)), Image.LANCZOS) \
    .crop((0, 0, FW, FH)).save(os.path.join(PH, 's4.jpg'), quality=95, subsampling=0)

N = 4
TAG = 'أكواب وصحون'


def head(logo='logo-en-green.png'):
    return f'<header><img src="../brand/{logo}"><div class="chip">{icon("gift")}<span>{TAG}</span></div></header>'


def foot(i, dark=True):
    return f'''<footer class="pf"><span class="note">صور توضيحية</span>
  <div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(N)}</span></div></footer>'''


def photo(i, img, kicker, title, sub):
    return f'''<section class="post ed" id="grad-{i:02d}" style="background-image:url(photos/graduation/{img})">
  <div class="veil"></div>{head()}
  <div class="txt">{f'<div class="kick">{kicker}</div>' if kicker else ''}<h2>{hl(title)}</h2><div class="cap">{sub}</div></div>
  {foot(i)}</section>'''


def cta(i):
    return f'''<section class="post cta4" id="grad-{i:02d}">
  <svg class="wm"><use href="#star"/></svg><svg class="wm2"><use href="#star"/></svg>
  <header><img src="../brand/logo-en-cream.png"><div class="chip">{icon("gift")}<span>{TAG}</span></div></header>
  <div class="txt"><h2>نصمم وننفذ<br>{hl("[[على طلبكم]]")}</h2><div class="cap">أرسلوا الصورة أو الاسم أو فكرتكم.. والباقي علينا</div></div>
  <div class="frame"><img src="photos/graduation/s4.jpg"></div>
  <div class="wa">{icon("wa", "wai")}<span>66606959</span></div>
  <footer><span class="h">للطلب والاستفسار واتساب</span>
  <div class="fr"><span class="h">@kami.printing</span><span class="cnt">{ar(i)} من {ar(N)}</span></div></footer></section>'''


SLIDES = [
    photo(1, 's1.jpg', 'أكواب وصحون بتصميمكم', 'صورتكم..<br>[[تنطبع]] على كوب', 'صورة، اسم، أو أي تصميم تبونه'),
    photo(2, 's2.jpg', '', 'عبارة [[على ذوقكم]]', 'تخرج، مواليد، أعياد ميلاد.. أو هدية بدون مناسبة'),
    photo(3, 's3.jpg', '', 'وبالاسم [[اللي تبونه]]', 'نكتب الاسم بالخط واللون اللي يعجبكم'),
    cta(4),
]

CSS = ns['CSS'] + '''
h2,.chip,.cnt,.kick,.wa span,.fw b{font-family:'Readex Pro','IBM Plex Sans Arabic',sans-serif!important}
.ed{background-size:cover;background-position:center}
.ed .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(247,243,236,.97) 0%,rgba(247,243,236,.9) 24%,rgba(247,243,236,0) 42%,
  rgba(247,243,236,0) 84%,rgba(247,243,236,.85) 100%)}
.ed .txt{position:absolute;left:64px;right:64px;top:168px;text-align:center;display:flex;flex-direction:column;align-items:center}
.ed .kick{font-size:28px;font-weight:500;letter-spacing:1px;color:#394634;margin-bottom:10px}
.ed h2{font-size:74px;font-weight:700;line-height:1.3;margin:0;color:var(--forest)}
.ed .cap{margin-top:14px;font-size:32px;font-weight:500;color:#394634}
.pf{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;align-items:center;direction:ltr}
.pf .note{font-size:20px;color:#394634;opacity:.8;direction:rtl}
.pf .h{font-size:26px;color:var(--forest)}
.cta4{background:linear-gradient(165deg,#B2BF9D 0%,#A7B591 50%,#9CAB86 100%)}
.cta4 .txt{position:absolute;left:64px;right:64px;top:170px;text-align:center}
.cta4 h2{font-size:80px;font-weight:700;line-height:1.3;margin:0}
.cta4 .cap{margin-top:16px;font-size:34px;font-weight:500;color:#394634}
.cta4 .frame{position:absolute;left:64px;right:64px;top:560px;height:535px;border-radius:40px;overflow:hidden;border:12px solid var(--cream);
  box-shadow:0 24px 50px rgba(46,59,42,.22)}
.cta4 .frame img{width:928px;height:511px;display:block}
.cta4 .wa{position:absolute;left:50%;transform:translateX(-50%);top:1126px;margin:0;padding:12px 44px}
'''

page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Graduation Cups</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=Alexandria:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{ns["defs"]}</svg>
{''.join(SLIDES)}</body></html>'''
open(os.path.join(HERE, 'graduation-cups.html'), 'w', encoding='utf-8').write(page)
print('ok')
