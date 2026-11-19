"""Build templates/project-story.html: Instagram story «لأصحاب المشاريع: نصمم وننفذ فكرتكم».
Theme from فهرس-التصاميم.md section 1, story size 1080x1920, content kept between y=250 and y=1600.
Render:
  python3 templates/project_story.py && PAGE=project-story.html OUTDIR=out/stories node templates/render.js
Photo: templates/photos/stories/winter-cups.jpg (real Kami work: winter hot-chocolate cups with tag and sticker).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'carousels.py'), encoding='utf-8').read()
src = src[:src.rindex('main()')]
cwd = os.getcwd(); os.chdir(HERE)
ns = {'__file__': os.path.join(HERE, 'carousels.py'), '__name__': 'carousels_lib'}
exec(compile(src, 'carousels.py', 'exec'), ns)
os.chdir(cwd)
hl, icon = ns['hl'], ns['icon']

STORY = f'''<section class="post story" id="story-projects-01">
  <svg class="wm"><use href="#star"/></svg><svg class="wm2"><use href="#star"/></svg>
  <header><img src="../brand/logo-en-cream.png"><div class="chip">{icon("sticker")}<span>لأصحاب المشاريع</span></div></header>
  <div class="txt">
    <h1>نصمم وننفذ<br>{hl("[[فكرتكم]]")}</h1>
    <div class="cap">من أول رسمة.. لين توصل بين إيدينكم</div>
  </div>
  <div class="frame"><img src="photos/stories/winter-cups.jpg"><span class="badge">من شغلنا</span></div>
  <div class="cta">أرسلوا لنا فكرتكم.. والباقي علينا</div>
  <footer><div class="fw">{icon("wa", "fwi")}<div><small>تواصل معنا عبر الواتساب</small><b>66606959</b></div></div>
  <div class="fr"><span class="h">@kami.printing</span></div></footer>
</section>'''

CSS = ns['CSS'] + '''
.post.story{height:1920px;background:linear-gradient(165deg,#B2BF9D 0%,#A7B591 50%,#9CAB86 100%)}
.story h1,.story .chip,.story .cta,.story .badge,.story .fw b{font-family:'Readex Pro','IBM Plex Sans Arabic',sans-serif!important}
.story .wm{width:760px;height:760px;left:-280px;bottom:260px;top:auto}
.story .wm2{width:300px;height:300px;right:-90px;top:420px}
.story header{top:250px}
.story .txt{position:absolute;left:64px;right:64px;top:380px;text-align:center}
.story h1{font-size:104px;font-weight:700;line-height:1.32;margin:0}
.story .cap{margin-top:22px;color:#394634;font-size:38px;font-weight:500}
.story .frame{position:absolute;left:110px;right:110px;top:760px;height:600px;border-radius:44px;overflow:hidden;
  border:12px solid var(--cream);box-shadow:0 28px 56px rgba(46,59,42,.25);transform:rotate(-1.5deg)}
.story .frame img{width:100%;height:100%;object-fit:cover;object-position:50% 52%;display:block}
.story .badge{position:absolute;right:26px;top:26px;background:var(--blush);color:var(--forest);font-weight:600;
  font-size:30px;padding:8px 26px;border-radius:30px;box-shadow:0 6px 14px rgba(46,59,42,.18)}
.story .cta{position:absolute;left:50%;transform:translateX(-50%);top:1405px;white-space:nowrap;background:var(--forest);
  color:var(--cream);font-weight:600;font-size:38px;padding:20px 56px;border-radius:60px}
.story footer{bottom:320px}
'''

page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Project Story</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=Alexandria:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{ns["defs"]}</svg>
{STORY}</body></html>'''
open(os.path.join(HERE, 'project-story.html'), 'w', encoding='utf-8').write(page)
print('ok')
