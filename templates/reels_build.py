"""Build Kami's photo/footage reels as HyperFrames projects (1080x1920).
Each video: shots (image with slow camera push, or real footage), Arabic text cards, an end card with the
WhatsApp number, and a real-recording sound plan. Run from the repo root:
  python3 templates/reels_build.py <video-key> <project-folder> <assets-folder>
Theme: sage/cream/blush/forest, Readex Pro headings, IBM Plex Sans Arabic text (SESSION_HANDOFF decisions).
"""
import json, os, re, shutil, sys

V = {
 'favors': {
  'title': 'توزيعات المواليد', 'dur': 15.5,
  'shots': [
   {'src': 'girl.jpg', 't': 0, 'd': 4.6, 'pos': '50% 40%', 'dy': 380, 'z': [1.0, 1.06], 'o': '50% 60%'},
   {'src': 'logo-stickers.jpg', 't': 4.6, 'd': 3.0, 'pos': '50% 55%', 'z': [1.08, 1.0], 'o': '45% 60%'},
   {'src': 'ribbon.mp4', 't': 7.6, 'd': 3.0, 'pos': '50% 50%', 'ms': 0.5, 'band': 760, 'z': [1.0, 1.04], 'o': '50% 55%'},
   {'src': 'abaya_gift.jpg', 't': 10.6, 'd': 2.3, 'pos': '50% 40%', 'dy': 330, 'z': [1.0, 1.05], 'o': '50% 55%'},
  ],
  'texts': [
   {'t': 0, 'e': 4.5, 'kick': 'توزيعات المواليد', 'h': 'مولودكم يستاهل<br>[[توزيعة بهالتفاصيل]]'},
   {'t': 4.75, 'e': 7.5, 'num': '١', 'h': 'ستيكر [[بالاسم والتاريخ]]'},
   {'t': 7.75, 'e': 10.5, 'num': '٢', 'h': 'تغليف [[بلون الثيم]]'},
   {'t': 10.75, 'e': 12.8, 'num': '٣', 'h': 'توصيل [[لين الباب]]'},
  ],
  'end': {'t': 12.9, 'h': 'احجزوا توزيعتكم<br>[[من اليوم]]', 'sub': 'قولوا لنا اسم المولود والتاريخ والثيم'},
  'sfx': [
   {'t': 0.05, 'lib': 'cord-pull', 'gain_db': -4, 'why': 'the ribbon on the box she holds'},
   {'t': 4.62, 'lib': 'card-flip', 'gain_db': -2, 'why': 'the stickers come into view'},
   {'t': 7.9, 'lib': 'cord-pull', 'gain_db': -1, 'why': 'hands pull the ribbon tight'},
   {'t': 8.8, 'lib': 'cloth-rustle', 'cut': [0.0, 0.8], 'gain_db': -7, 'why': 'the ribbon tied into a bow'},
   {'t': 12.92, 'lib': 'cardboard-lid', 'gain_db': -3, 'why': 'the box closed: the end card'},
  ],
 },
 'packing': {
  'title': 'تجهيز طلب', 'dur': 17.0,
  'shots': [
   {'src': 'unbox.jpg', 't': 0, 'd': 3.4, 'pos': '50% 50%', 'z': [1.15, 1.0], 'o': '48% 52%'},
   {'src': 'logo-stickers.jpg', 't': 3.4, 'd': 2.8, 'pos': '50% 55%', 'z': [1.0, 1.08], 'o': '45% 60%'},
   {'src': 'thank-cards.jpg', 't': 6.2, 'd': 2.6, 'pos': '50% 50%', 'z': [1.0, 1.08], 'o': '55% 45%'},
   {'src': 'ribbon.mp4', 't': 8.8, 'd': 2.6, 'pos': '50% 50%', 'ms': 4.0, 'band': 760, 'z': [1.0, 1.04], 'o': '50% 55%'},
   {'src': 'hijab_box.jpg', 't': 11.4, 'd': 2.6, 'pos': '50% 40%', 'dy': 300, 'z': [1.0, 1.06], 'o': '50% 55%'},
  ],
  'texts': [
   {'t': 0, 'e': 3.3, 'kick': 'لمشروعكم', 'h': 'شوفوا كيف<br>[[نجهّز طلبكم]] ✦'},
   {'t': 3.55, 'e': 6.1, 'num': '١', 'h': 'ستيكر [[الشعار]]'},
   {'t': 6.35, 'e': 8.7, 'num': '٢', 'h': 'بطاقة [[الشكر]]'},
   {'t': 8.95, 'e': 11.3, 'num': '٣', 'h': 'تغليف [[بعناية]]'},
   {'t': 11.55, 'e': 13.9, 'num': '٤', 'h': 'ويوصل [[لزبونكم]]'},
  ],
  'end': {'t': 14.0, 'h': 'مشروعكم يستاهل<br>[[هالتفاصيل]]', 'sub': 'أرسلوا شعاركم ونجهّز لكم مطبوعاتكم'},
  'sfx': [
   {'t': 0.05, 'lib': 'wrapping-paper', 'cut': [0.0, 0.9], 'gain_db': -2, 'why': 'the tissue in the open box'},
   {'t': 3.42, 'lib': 'card-deal', 'gain_db': -3, 'why': 'the stickers fanned in her hand'},
   {'t': 6.22, 'lib': 'card-flip', 'gain_db': -2, 'why': 'the thank-you cards'},
   {'t': 9.1, 'lib': 'cord-pull', 'gain_db': -1, 'why': 'the ribbon pulled tight'},
   {'t': 14.02, 'lib': 'cardboard-lid', 'gain_db': -3, 'why': 'the box closed: the end card'},
  ],
 },
 'clearance': {
  'title': 'تخليص المعاملات', 'dur': 17.5,
  'shots': [
   {'src': 'hijab_phone.mp4', 't': 0, 'd': 4.2, 'pos': '50% 50%', 'ms': 0.3, 'z': [1.0, 1.06], 'o': '50% 60%'},
   {'src': 'printer.mp4', 't': 4.2, 'd': 3.8, 'pos': '45% 50%', 'ms': 2.0, 'band': 760, 'z': [1.05, 1.0], 'o': '50% 50%'},
   {'src': 'woman_printer.mp4', 't': 8.0, 'd': 3.6, 'pos': '55% 50%', 'ms': 4.6, 'band': 760, 'z': [1.0, 1.05], 'o': '60% 55%'},
   {'src': 'hijab_laptop.mp4', 't': 11.6, 'd': 2.8, 'pos': '50% 50%', 'ms': 1.0, 'z': [1.04, 1.1], 'o': '50% 50%'},
  ],
  'texts': [
   {'t': 0, 'e': 4.1, 'kick': 'تخليص المعاملات', 'h': 'معاملتك بـ [[١٫٥ دينار]]<br>وأنت في بيتك؟'},
   {'t': 4.35, 'e': 7.9, 'prices': [('البطاقة الذكية', '1.500'), ('الإسكان: طلب جديد', '4.000'), ('برنامج مزايا', '5.000')]},
   {'t': 8.15, 'e': 11.5, 'prices': [('الباحثين عن عمل', '2.000'), ('معاملات سجلات', '3.000'), ('شهادة ميلاد', '1.500')]},
   {'t': 11.75, 'e': 14.3, 'kick': 'بدون طوابير', 'h': 'أرسل نوع المعاملة<br>[[على الواتساب]]'},
  ],
  'end': {'t': 14.4, 'h': 'معاملتك علينا..<br>[[ووقتك لك]]', 'sub': 'للأفراد والشركات · الأسعار بالدينار البحريني'},
  'sfx': [
   {'t': 0.05, 'lib': 'button-click', 'gain_db': -6, 'why': 'she taps her phone'},
   {'t': 4.22, 'lib': 'page-flip', 'gain_db': -2, 'why': 'paper going through the printer'},
   {'t': 5.0, 'lib': 'card-deal', 'gain_db': -5, 'why': 'the price cards land'},
   {'t': 8.9, 'lib': 'page-flip', 'gain_db': 0, 'why': 'the printout taken from the tray'},
   {'t': 14.42, 'lib': 'card-flip', 'gain_db': -3, 'why': 'the end card'},
  ],
 },
 'national': {
  'title': 'العيد الوطني', 'dur': 17.0, 'national': True, 'voice': 'assets/vo/vo.wav',
  'shots': [
   {'src': 'girl.jpg', 't': 0, 'd': 4.4, 'pos': '50% 40%', 'dy': 380, 'z': [1.0, 1.06], 'o': '50% 60%'},
   {'src': 'FLAG', 't': 4.4, 'd': 2.0, 'z': [1.0, 1.04], 'o': '50% 50%'},
   {'src': 'abaya_gift.jpg', 't': 6.4, 'd': 1.8, 'pos': '50% 40%', 'dy': 330, 'z': [1.0, 1.05], 'o': '50% 55%'},
   {'src': 'logo-stickers.jpg', 't': 8.2, 'd': 2.0, 'pos': '50% 55%', 'z': [1.08, 1.0], 'o': '45% 60%'},
   {'src': 'shopfront.jpg', 't': 10.2, 'd': 2.65, 'pos': '50% 40%', 'z': [1.0, 1.08], 'o': '55% 35%'},
  ],
  'texts': [
   {'t': 0, 'e': 4.3, 'kick': 'العيد الوطني البحريني', 'h': 'كل عام<br>[[والبحرين بخير]]', 'cls': 'red'},
   {'t': 4.5, 'e': 6.35, 'kick': '١٦ ديسمبر', 'h': 'جهّزنا لكم<br>[[للعيد الوطني]]', 'cls': 'onflag'},
   {'t': 6.5, 'e': 8.15, 'num': '١', 'h': 'توزيعات [[بألوان العلم]]', 'cls': 'red'},
   {'t': 8.3, 'e': 10.15, 'num': '٢', 'h': 'ستيكرات و[[بطاقات تهنئة]]', 'cls': 'red'},
   {'t': 10.3, 'e': 12.75, 'num': '٣', 'h': 'بنرات [[للمدارس والشركات]]', 'cls': 'red'},
  ],
  'end': {'t': 12.85, 'h': 'احجزوا<br>[[من اليوم]]', 'sub': 'كل عام والبحرين بخير ✦'},
  'sfx': [
   {'t': 4.12, 'lib': 'cloth-rustle', 'cut': [0.0, 0.45], 'gain_db': -2, 'why': 'the flag sweeps in, in the pause'},
   {'t': 6.22, 'lib': 'card-deal', 'gain_db': -3, 'why': 'the favors, in the pause'},
   {'t': 15.0, 'lib': 'card-flip', 'gain_db': -4, 'why': 'the end card settles after the last word'},
  ],
 },
}

def hl(s):
    return re.sub(r'\[\[(.+?)\]\]', r'<span class="hl">\1</span>', s)

CSS = '''
@font-face{font-family:Display;src:url(assets/fonts/display.ttf)}
@font-face{font-family:Second;src:url(assets/fonts/text.ttf)}
:root{--sage:#A7B591;--cream:#EDE9E0;--blush:#E2CDCC;--forest:#2E3B2A}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#2E3B2A}
#root{position:relative;width:100%;height:100%;overflow:hidden}
.shot{position:absolute;inset:0;overflow:hidden;opacity:0}
.shot img,.shot video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.shot .blur{filter:blur(38px) brightness(.8);transform:scale(1.25)}
.shot video.band{inset:auto;left:0;width:1080px;height:608px;object-fit:cover;border-top:6px solid #EDE9E0;border-bottom:6px solid #EDE9E0;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.scrim{position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,rgba(30,40,28,.82) 0%,rgba(30,40,28,.45) 30%,rgba(30,40,28,0) 48%),
             linear-gradient(0deg,rgba(30,40,28,.75) 0%,rgba(30,40,28,0) 22%)}
.brand{position:absolute;left:70px;bottom:440px;display:flex;align-items:center;gap:18px;direction:ltr}
.brand img{height:62px}
.brand span{font-family:Second;font-size:30px;color:#EDE9E0;opacity:.9}
.card{position:absolute;left:90px;right:150px;top:250px;display:flex;flex-direction:column;align-items:center;text-align:center;opacity:0}
.kick{font-family:Second;font-size:38px;color:#EDE9E0;opacity:.95;margin-bottom:14px}
.num{width:96px;height:96px;border-radius:50%;background:#E2CDCC;color:#2E3B2A;font-family:Display;font-size:56px;
  display:flex;align-items:center;justify-content:center;margin-bottom:22px}
h1{font-family:Display;font-weight:700;color:#EDE9E0;font-size:92px;line-height:1.38;text-shadow:0 4px 24px rgba(0,0,0,.35)}
h1.sm{font-size:84px}
.hl{background:#E2CDCC;color:#2E3B2A;border-radius:16px;padding:0 20px;text-shadow:none;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.prices{width:100%;display:flex;flex-direction:column;gap:22px;margin-top:6px}
.pr{display:flex;justify-content:space-between;align-items:center;background:rgba(237,233,224,.96);border-radius:30px;padding:26px 34px;opacity:0}
.pr .n{font-family:Second;font-size:44px;color:#2E3B2A;font-weight:500}
.pr .p{font-family:Display;font-size:50px;color:#2E3B2A;background:#E2CDCC;border-radius:40px;padding:4px 26px;direction:ltr;white-space:nowrap}
.pr .p small{font-family:Second;font-size:30px;margin-left:8px}
.flag{position:absolute;inset:0;width:100%;height:100%}
.strip{position:absolute;left:0;top:0;width:1080px;height:60px;z-index:5}
.red .hl{background:#CE1126;color:#FFFFFF}
.card.onflag{left:440px;right:60px;top:690px}
.card.onflag h1{font-size:96px;text-shadow:none}
.card.onflag .hl{background:#FFFFFF;color:#CE1126}
.card.onflag .kick{color:#FFFFFF}
.strip{z-index:10}
#end{position:absolute;inset:0;opacity:0;background:linear-gradient(165deg,#B2BF9D 0%,#A7B591 50%,#9CAB86 100%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 110px 160px}
#end .st{position:absolute;fill:#EDE9E0;opacity:.18;width:760px;height:760px;left:-300px;bottom:180px}
#end .st2{position:absolute;fill:#E2CDCC;opacity:.5;width:300px;height:300px;right:-90px;top:330px}
#end .logo{width:400px;margin-bottom:70px}
#end h1{color:#2E3B2A;text-shadow:none;font-size:90px}
#end .sub{font-family:Second;font-size:40px;color:#394634;margin-top:30px;line-height:1.6}
#end .wa{margin-top:60px;display:flex;align-items:center;gap:20px;background:#2E3B2A;color:#EDE9E0;border-radius:70px;padding:22px 60px;direction:ltr}
#end .wa b{font-family:Display;font-size:70px;letter-spacing:2px}
#end .wa svg{width:66px;height:66px;fill:none;stroke:#EDE9E0;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
#end .handle{font-family:Second;font-size:34px;color:#2E3B2A;margin-top:30px;direction:ltr}
'''

STAR = '<svg class="{c}" viewBox="0 0 100 100"><path d="M50 0Q50 50 100 50Q50 50 50 100Q50 50 0 50Q50 50 50 0Z"/></svg>'
WA = '<svg viewBox="0 0 24 24"><path d="M3.5 20.5l1.3-4.2A8.5 8.5 0 1 1 8 19.4z"/><path d="M9 8.5c0 3 2.5 6.5 6.5 6.5l1-1.5-2-1-1 1c-1.2-.5-2.5-1.8-3-3l1-1-1-2z"/></svg>'

def build(key, proj, assets):
    v = V[key]; D = v['dur']
    os.makedirs(os.path.join(proj, 'assets', 'fonts'), exist_ok=True)
    os.makedirs(os.path.join(proj, 'plan'), exist_ok=True)
    for f in ['display.ttf', 'text.ttf']:
        shutil.copy(os.path.join(assets, 'fonts', f), os.path.join(proj, 'assets', 'fonts', f))
    for f in ['logo-en-cream.png', 'logo-en-green.png']:
        shutil.copy(os.path.join('brand', f), os.path.join(proj, 'assets', f))
    els, tl = [], []
    for i, s in enumerate(v['shots']):
        sid = f's{i}'
        if s['src'] == 'FLAG':  # the Bahrain flag drawn in code: white hoist, five white points, red field
            pts = ' '.join(f'{x},{y}' for k in range(5) for x, y in ((300, k * 384), (430, k * 384 + 192))) + ' 300,1920'
            media = (f'<svg class="flag" viewBox="0 0 1080 1920" preserveAspectRatio="none"><rect width="1080" height="1920" fill="#CE1126"/>'
                     f'<polygon fill="#FFFFFF" points="0,0 {pts} 0,1920"/></svg>')
            els.append(f'<div class="shot" id="{sid}" style="transform-origin:{s["o"]}">{media}</div>')
            z0, z1 = s['z']
            tl.append(f'tl.set("#{sid}",{{opacity:1,scale:{z0}}},{s["t"]});tl.to("#{sid}",{{scale:{z1},duration:{s["d"]},ease:"none"}},{s["t"]});'
                      f'tl.fromTo("#{sid} polygon",{{x:-520}},{{x:0,duration:0.6,ease:"power3.out"}},{s["t"]});'
                      f'tl.set("#{sid}",{{opacity:0}},{s["t"] + s["d"]});')
            continue
        shutil.copy(os.path.join(assets, s['src']), os.path.join(proj, 'assets', s['src']))
        if s['src'].endswith('.mp4'):
            vid = lambda k, cls, st: (f'<video id="{sid}{k}" class="clip {cls}" src="assets/{s["src"]}" data-start="{s["t"]}" data-duration="{s["d"]}" '
                     f'data-media-start="{s.get("ms", 0)}" data-track-index="{i * 2 + 1 + (k == "b")}" muted playsinline style="{st}"></video>')
            if s.get('band'):  # the whole 16:9 frame as a band, over a blurred copy of itself
                media = vid('b', 'blur', '') + vid('v', 'band', f'top:{s["band"]}px')
            else:
                media = vid('v', '', f'object-position:{s["pos"]}')
        else:
            if s.get('dy'):  # move the picture down so the headline sits above the face
                media = (f'<img class="blur" src="assets/{s["src"]}">'
                         f'<img src="assets/{s["src"]}" style="top:{s["dy"]}px;height:1920px;bottom:auto;object-position:{s["pos"]}">')
            else:
                media = f'<img src="assets/{s["src"]}" style="object-position:{s["pos"]}">'
        els.append(f'<div class="shot" id="{sid}" style="transform-origin:{s["o"]}">{media}</div>')
        z0, z1 = s['z']
        tl.append(f'tl.set("#{sid}",{{opacity:1,scale:{z0}}},{s["t"]});'
                  f'tl.to("#{sid}",{{scale:{z1},duration:{s["d"]},ease:"none"}},{s["t"]});'
                  f'tl.set("#{sid}",{{opacity:0}},{s["t"] + s["d"]});')
    els.append('<div class="scrim"></div>')
    if v.get('national'):  # a thin red-white national strip along the top, serrated like the flag
        teeth = ''.join(f'<polygon points="{x},0 {x + 54},0 {x + 27},26" fill="#FFFFFF"/>' for x in range(0, 1080, 54))
        els.append(f'<svg id="strip" class="strip" viewBox="0 0 1080 60"><rect width="1080" height="60" fill="#CE1126"/>{teeth}</svg>')
    els.append('<div class="brand" id="brand"><img src="assets/logo-en-cream.png"><span>@kami.printing</span></div>')
    for i, c in enumerate(v['texts']):
        cid = f'c{i}'
        inner = ''
        if c.get('kick'):
            inner += f'<div class="kick" dir="rtl">✦ {c["kick"]} ✦</div>'
        if c.get('num'):
            inner += f'<div class="num">{c["num"]}</div>'
        if c.get('h'):
            inner += f'<h1 dir="rtl" class="{"sm" if c.get("num") else ""}">{hl(c["h"])}</h1>'
        if c.get('prices'):
            inner += '<div class="prices">' + ''.join(
                f'<div class="pr" id="{cid}p{k}"><span class="n" dir="rtl">{n}</span><span class="p">{p}<small>BD</small></span></div>'
                for k, (n, p) in enumerate(c['prices'])) + '</div>'
        els.append(f'<div class="card {c.get("cls", "")}" id="{cid}">{inner}</div>')
        t0, t1 = c['t'], c['e']
        if t0 == 0:  # the hook is readable on frame 0, already moving
            tl.append(f'tl.fromTo("#{cid}",{{opacity:1,y:24}},{{y:0,duration:0.6,ease:"power2.out"}},0);')
        else:
            tl.append(f'tl.fromTo("#{cid}",{{opacity:0,y:50}},{{opacity:1,y:0,duration:0.45,ease:"power3.out"}},{t0});')
        for k in range(len(c.get('prices', []))):
            tl.append(f'tl.fromTo("#{cid}p{k}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.4,ease:"power3.out"}},{t0 + 0.15 + k * 0.55:.2f});')
        tl.append(f'tl.to("#{cid}",{{opacity:0,y:-30,duration:0.25,ease:"power2.in"}},{t1 - 0.25:.2f});')
    e = v['end']
    els.append(f'''<div id="end">{STAR.format(c="st")}{STAR.format(c="st2")}
<img class="logo" src="assets/logo-en-green.png"><h1 dir="rtl">{hl(e["h"])}</h1><div class="sub" dir="rtl">{e["sub"]}</div>
<div class="wa">{WA}<b>66606959</b></div><div class="handle">@kami.printing</div></div>''')
    tl.append(f'tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:0.4}},{e["t"]});'
              f'tl.fromTo("#end .logo",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power3.out"}},{e["t"] + 0.1:.2f});'
              f'tl.fromTo("#end h1",{{y:50,opacity:0}},{{y:0,opacity:1,duration:0.5,ease:"power3.out"}},{e["t"] + 0.25:.2f});'
              f'tl.fromTo("#end .sub",{{opacity:0}},{{opacity:1,duration:0.4}},{e["t"] + 0.6:.2f});'
              f'tl.fromTo("#end .wa",{{scale:0.85,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.6)"}},{e["t"] + 0.8:.2f});'
              f'tl.fromTo("#end .st",{{rotation:0}},{{rotation:25,duration:{D - e["t"]:.2f},ease:"none"}},{e["t"]});'
              f'tl.to("#brand",{{opacity:0,duration:0.3}},{e["t"]});')
    audio = (f'<audio id="mix" class="clip" src="assets/mix.wav" data-start="0" data-duration="{D}" data-track-index="20" data-volume="1"></audio>'
             if os.path.exists(os.path.join(proj, 'assets', 'mix.wav')) else '')
    html = f'''<!doctype html>
<html lang="ar" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-fps="30" data-width="1080" data-height="1920">
{chr(10).join(els)}
{audio}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{chr(10).join(tl)}
tl.set({{}},{{}},{D});
window.__timelines["main"] = tl;
</script></body></html>'''
    open(os.path.join(proj, 'index.html'), 'w', encoding='utf-8').write(html)
    plan = {'duration': D, 'bed': [], 'pictures': [{'from': 0, 'to': D, 'material': 'paper'}],
            'effects': [{**x, 'align': 'attack'} for x in v['sfx']]}
    if v.get('voice'):
        plan['voice'] = {'file': v['voice'], 'at': 0.0}
    json.dump(plan, open(os.path.join(proj, 'plan', 'sound.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('built', key, D, 's')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], sys.argv[3])
