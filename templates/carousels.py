"""Build templates/carousels.html: all Kami Instagram carousels in one consistent
system (fixed header/footer, highlighted titles, icon grids, price cards, CTA).
Content lives in CAROUSELS below. Render with:
  python3 templates/carousels.py && PAGE=carousels.html OUTDIR=out/carousels node templates/render.js
"""
import os, re, html

HERE = os.path.dirname(os.path.abspath(__file__))
WA = '66606959'
HANDLE = '@kami.printing'

def hl(t):  # [[word]] -> highlighted span
    return re.sub(r'\[\[(.+?)\]\]', r'<span class="hl">\1</span>', t)

C = {}
C['launch'] = ('إطلاق الهوية', 'gift', [
    {'type': 'cover', 'logo': True, 'title': 'حكاية تبدأ<br>[[من التفاصيل]]', 'sub': 'أهلاً فيكم في كامي للطباعة'},
    {'type': 'features', 'kicker': 'خدماتنا', 'title': 'شنو نقدّم [[لكم؟]]', 'items': [
        ('gift', 'التوزيعات', 'لكل مناسبة توزيعة تشبهها'),
        ('printer', 'الطباعة', 'خامات مختارة وتشطيب نظيف'),
        ('pencil', 'الأدوات المدرسية', 'بداية مرتبة من أول يوم'),
        ('docs', 'تخليص المعاملات', 'معاملتك علينا.. ووقتك لك')]},
    {'type': 'features', 'kicker': 'ليش كامي؟', 'title': 'عناية [[بكل تفصيلة]]', 'items': [
        ('star', 'لمسة راقية', 'نشتغل على كل طلب كأنه لنا'),
        ('uv', 'تصميم على ذوقكم', 'الاسم والألوان حسب مناسبتكم'),
        ('truck', 'التوصيل متوفر', 'طلبكم يوصلكم لين الباب')]},
    {'type': 'cta', 'title': 'قولوا لنا مناسبتكم..<br>[[والباقي علينا]]', 'sub': 'حيّاكم على الواتساب'},
])
C['giveaways'] = ('التوزيعات', 'gift', [
    {'type': 'cover', 'icon': 'gift', 'title': 'أول انطباع عن فرحتكم..<br>[[يبدأ من التوزيعة]]', 'sub': 'توزيعات لكل مناسبة، بلمسة تشبهكم'},
    {'type': 'grid', 'kicker': 'توزيعات لكل مناسبة', 'title': 'مناسباتكم [[علينا]]', 'items': [
        ('baby', 'المواليد والاستقبال'), ('rings', 'الزواج والملكة'), ('cake', 'أعياد الميلاد'),
        ('ramadan', 'رمضان والقرقاعون'), ('gift', 'العيد'), ('bag', 'التوزيعات المدرسية')],
     'pill': 'نصمم التوزيعة على ذوقكم وثيم مناسبتكم'},
    {'type': 'features', 'kicker': 'تفاصيل تفرق', 'title': 'ليش توزيعاتنا [[غير؟]]', 'items': [
        ('tag', 'الاسم والتاريخ', 'بخط أنيق يليق بالمناسبة'),
        ('uv', 'ألوان الثيم', 'تمشي مع ألوان مناسبتكم'),
        ('gift', 'تغليف مرتب', 'بتفاصيل هادية وراقية')]},
    {'type': 'steps', 'kicker': 'طريقة الطلب', 'title': 'كيف [[تطلبون؟]]', 'items': [
        ('أرسلوا لنا مناسبتكم', 'النوع، العدد، والتاريخ'),
        ('نصمم على ذوقكم', 'الاسم والألوان والثيم'),
        ('نطبع ونغلّف', 'بعناية في كل تفصيلة'),
        ('نوصلها لكم', 'التوصيل متوفر')]},
    {'type': 'cta', 'title': 'احجزوا توزيعتكم..<br>[[من اليوم]]', 'sub': 'وقولوا لنا: شنو مناسبتكم الجاية؟'},
])
C['school'] = ('التوزيعات المدرسية', 'bag', [
    {'type': 'cover', 'icon': 'bag', 'title': 'بداية مرتبة..<br>[[لسنة أحلى]]', 'sub': 'توزيعات وأدوات مدرسية باسم طفلكم'},
    {'type': 'grid', 'kicker': 'للمدرسة', 'title': 'كل اللي [[يحتاجونه]]', 'items': [
        ('tag', 'ستيكرات أسماء'), ('pencil', 'أدوات مدرسية'), ('bag', 'توزيعات الصف'),
        ('gift', 'توزيعات نهاية السنة'), ('sticker', 'ستيكرات بقص'), ('laminate', 'تغليف حراري')],
     'pill': 'جاهزة من أول يوم دراسي'},
    {'type': 'features', 'kicker': 'لمين؟', 'title': 'تفاصيل [[تفرّحهم]]', 'items': [
        ('bag', 'للأمهات', 'تجهيز مرتب باسم طفلكم'),
        ('pencil', 'للمعلمات', 'توزيعات تفرّح طلابكم'),
        ('gift', 'للمدارس', 'طلبات الكميات بجودة ثابتة')]},
    {'type': 'cta', 'title': 'أرسلوا اسم الطالب..<br>[[ونجهزها لكم]]', 'sub': 'مع الثيم اللي تحبونه، على الواتساب'},
])
C['printing'] = ('الطباعة', 'printer', [
    {'type': 'cover', 'icon': 'printer', 'title': 'طباعة بجودة..<br>[[تبيّن الفرق]]', 'sub': 'خامات مختارة، وتشطيب نظيف'},
    {'type': 'grid', 'kicker': 'خدماتنا', 'title': 'خدمات [[الطباعة]]', 'items': [
        ('printer', 'طباعة عالية الجودة'), ('laminate', 'تغليف حراري'), ('sticker', 'ستيكرات بقص احترافي'),
        ('uv', 'ستيكرات UV'), ('acrylic', 'أكريليك'), ('cotton', 'قصاصات قطنية'),
        ('banner', 'طباعة البنرات'), ('card', 'بزنس كارد'), ('letter', 'طباعة Letterhead')],
     'pill': 'كل ما تحتاجه من طباعة وإبداع.. بلمسة جميلة'},
    {'type': 'cta', 'title': 'عندكم فكرة؟<br>[[نطبعها لكم]]', 'sub': 'أرسلوا لنا التفاصيل على الواتساب'},
])
C['clearance'] = ('تخليص المعاملات', 'docs', [
    {'type': 'cover', 'icon': 'docs', 'title': 'معاملتك علينا..<br>[[ووقتك لك]]', 'sub': 'للأفراد والشركات · بدون طوابير ولا مشاوير'},
    {'type': 'prices', 'groups': [('هيئة المعلومات والحكومة الإلكترونية', [
        ('تجديد / إصدار / بدل فاقد بطاقة الهوية', '1.500'),
        ('تحديث بيانات البطاقة الذكية', '1.500', 'الاجتماعية، الديانة، العائلية، التعليم، العمل، العنوان'),
        ('التقرير الائتماني من بنفت', '2.000'),
        ('شهادة الميلاد للمواليد الجدد / بدل فاقد، وشهادة الوفاة', '1.500', 'إصدار / بدل فاقد'),
        ('خدمة الإشعارات الحكومية', '1.500')])]},
    {'type': 'prices', 'groups': [('وزارة الإسكان', [
        ('تقديم طلب جديد', '4.000'),
        ('طلب برنامج مزايا', '5.000'),
        ('طلب تمويل للبناء أو الشراء أو الترميم', '4.000'),
        ('الإقرار لأفراد الأسرة والموافقة عليه', '0.500'),
        ('الإشعارات الحكومية', '1.500', 'تحديث بيانات الاتصال')])]},
    {'type': 'prices', 'groups': [
        ('وزارة العمل والتنمية الاجتماعية', [
            ('تسجيل وتحديث بيانات الباحثين عن عمل', '2.000'),
            ('تسجيل حضور المواعيد في معرض التوظيف الإلكتروني', '0.500'),
            ('ترشيح وظيفة في معرض التوظيف الإلكتروني', '1.000')]),
        ('المساعدات الاجتماعية / الخيرية الملكية', [
            ('تقديم خدمة غلاء المعيشة', '3.000'),
            ('غلاء اللحوم / تغيير الحساب / الإعاقة', '1.500'),
            ('مساعدات المؤسسة الملكية للأعمال الإنسانية', '5.000')])]},
    {'type': 'prices', 'groups': [('وزارة التربية والتعليم', [
        ('نسخ الإفادات وكشف الدرجات لطلبة المدارس', '1.500'),
        ('تحويل طلبة المدارس', '1.500'),
        ('طلب شهادات وإفادات', '1.500'),
        ('الاطلاع على نتائج الطلبة', '0.300', None, '+ الطباعة')])]},
    {'type': 'prices', 'groups': [('خدمات أخرى', [
        ('بطاقة سديم (بابكو)', '1.500'),
        ('مفتاح إلكتروني جديد', '1.000'),
        ('تغيير واسترجاع المفتاح الإلكتروني', '0.500'),
        ('الاطلاع على الفواتير أو مستحقات المحكمة', '0.300', 'بدون طباعة'),
        ('معاملات موقع سجلات', '3.000')])]},
    {'type': 'cta', 'title': 'أرسلوا نوع المعاملة..<br>[[وننجزها لكم]]', 'sub': 'نرد عليكم بالتفاصيل على الواتساب'},
])
C['collab'] = ('تعاون', 'rings', [
    {'type': 'cover', 'icon': 'card', 'title': 'منظمين الحفلات والشركات..<br>[[خلونا نشتغل سوا]]', 'sub': 'للفعاليات، الحفلات، وهدايا الشركات'},
    {'type': 'features', 'kicker': 'شنو نجهز لكم؟', 'title': 'شراكة [[تليق فيكم]]', 'items': [
        ('gift', 'توزيعات وهدايا', 'بهوية مناسبتكم أو شعار شركتكم'),
        ('banner', 'مطبوعات الفعاليات', 'بنرات، كروت، وستيكرات'),
        ('card', 'طلبات الكميات', 'بجودة ثابتة في كل قطعة')]},
    {'type': 'cta', 'title': 'اكتبوا «تعاون»..<br>[[ونرتب معاكم]]', 'sub': 'على الواتساب، ونحدد موعد يناسبكم'},
])
C['faq'] = ('الأسئلة الشائعة', 'docs', [
    {'type': 'cover', 'icon': 'tag', 'title': 'أسئلتكم..<br>[[وأجوبتنا]]', 'sub': 'كل اللي تحتاجون تعرفونه قبل الطلب'},
    {'type': 'faq', 'items': [
        ('هل التوصيل متوفر؟', 'إي نعم، التوصيل متوفر.'),
        ('أقدر أختار التصميم والألوان؟', 'أكيد، نصمم حسب ذوقكم وثيم مناسبتكم.')]},
    {'type': 'faq', 'items': [
        ('كيف أطلب توزيعات؟', 'أرسلوا لنا نوع المناسبة والعدد والتاريخ على الواتساب، ونرتب معاكم التفاصيل.'),
        ('كيف أطلب تخليص معاملة؟', 'أرسلوا نوع المعاملة على الواتساب، ونوضح لكم المطلوب والسعر.')]},
    {'type': 'cta', 'title': 'عندكم سؤال ثاني؟<br>[[حيّاكم]]', 'sub': 'نسعد بخدمتكم دايماً'},
])

AR = '٠١٢٣٤٥٦٧٨٩'
ar = lambda n: ''.join(AR[int(d)] for d in str(n))

def icon(name, cls='ic'):
    return f'<svg class="{cls}"><use href="#{name}"/></svg>'

def slide(key, tag, tagicon, s, i, n):
    t = s['type']; body = ''
    if t == 'cover':
        mid = ('<img class="coverlogo" src="../brand/logo-ar-cream.png">' if s.get('logo')
               else f'<div class="bigic">{icon(s["icon"])}</div>')
        body = f'''{mid}<h1 class="t-cover">{hl(s["title"])}</h1><div class="sub">{s["sub"]}</div>
        <div class="swipe">اسحبوا<svg viewBox="0 0 120 50"><path d="M110 10 C80 40 40 40 12 26"/><path d="M26 14 L10 26 L28 36"/></svg></div>'''
    elif t in ('grid', 'features', 'steps', 'prices', 'faq'):
        if t != 'prices' and t != 'faq':
            body = f'<div class="kicker">✦ {s["kicker"]} ✦</div><h2>{hl(s["title"])}</h2><div class="rule"></div>'
        if t == 'grid':
            cols = 3
            body += '<div class="grid">' + ''.join(
                f'<div class="gi"><div class="gc">{icon(ic)}</div><div class="gl">{lb}</div></div>' for ic, lb in s['items']) + '</div>'
            body += f'<div class="pill">{s["pill"]}</div>'
        elif t == 'features':
            body += '<div class="feats">' + ''.join(
                f'<div class="ft"><div class="gc sm">{icon(ic)}</div><div><div class="ftt">{a}</div><div class="ftd">{b}</div></div></div>'
                for ic, a, b in s['items']) + '</div>'
        elif t == 'steps':
            body += '<div class="steps">' + ''.join(
                f'<div class="st"><div class="sn">{ar(k + 1)}</div><div><div class="ftt">{a}</div><div class="ftd">{b}</div></div></div>'
                for k, (a, b) in enumerate(s['items'])) + '</div>'
        elif t == 'prices':
            multi = len(s['groups']) > 1
            body = '<div class="kicker">✦ خدماتنا لمعاملات ✦</div>'
            if not multi:
                body += f'<h2 class="ent">{s["groups"][0][0]}</h2><div class="rule"></div>'
            for g, rows in s['groups']:
                if multi:
                    body += f'<div class="gh">{g}</div>'
                r = ''
                for row in rows:
                    name, price = row[0], row[1]
                    note = row[2] if len(row) > 2 and row[2] else ''
                    extra = row[3] if len(row) > 3 else ''
                    r += (f'<div class="row"><div class="rn">{name}' + (f'<small>({note})</small>' if note else '') +
                          f'</div><div class="rp"><b>{price}</b> د.ب{(" " + extra) if extra else ""}</div></div>')
                body += f'<div class="card{" tight" if multi else ""}">{r}</div>'
            body += '<div class="cur">الأسعار بالدينار البحريني</div>'
        elif t == 'faq':
            body = '<div class="kicker">✦ الأسئلة الشائعة ✦</div><div class="faqs">' + ''.join(
                f'<div class="q">{q}</div><div class="a">{a}</div>' for q, a in s['items']) + '</div>'
    elif t == 'cta':
        body = f'''<div class="ctaw"><svg class="spk"><use href="#star"/></svg><h1 class="t-cta">{hl(s["title"])}</h1>
        <div class="sub">{s["sub"]}</div><div class="wa">{icon("wa", "wai")}<span>{WA}</span></div>
        <img class="ctalogo" src="../brand/logo-ar-cream.png"></div>'''
    return f'''<section class="post {t}" id="{key}-{i:02d}">
  <svg class="wm"><use href="#star"/></svg><svg class="wm2"><use href="#star"/></svg>
  <header><img src="../brand/logo-en-cream.png"><div class="chip">{icon(tagicon)}<span>{tag}</span></div></header>
  <main>{body}</main>
  <footer><div class="fw">{icon("wa", "fwi")}<div><small>تواصل معنا عبر الواتساب</small><b>{WA}</b></div></div>
  <div class="fr"><span class="h">{HANDLE}</span><span class="cnt">{ar(i)} من {ar(n)}</span></div></footer>
</section>'''

defs = open(os.path.join(HERE, 'services-grid.html'), encoding='utf-8').read()
defs = defs[defs.index('<defs>'):defs.index('</defs>') + 7]

CSS = '''
:root{--sage:#A7B591;--cream:#EDE9E0;--blush:#E2CDCC;--forest:#2E3B2A;--forest2:#384833;--line:rgba(46,59,42,.2)}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#999;display:flex;flex-wrap:wrap;gap:30px;padding:30px;font-family:'IBM Plex Sans Arabic',sans-serif}
.post{flex:none;width:1080px;height:1350px;position:relative;overflow:hidden;color:var(--forest);
  background:radial-gradient(circle at 80% 15%,#B4C19F 0%,#A7B591 55%,#9CAB86 100%)}
.wm{position:absolute;width:620px;height:620px;left:-230px;bottom:120px;fill:var(--cream);opacity:.18}
.wm2{position:absolute;width:260px;height:260px;right:-80px;top:240px;fill:var(--blush);opacity:.45}
header{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center;direction:ltr}
header img{height:78px}
.chip{display:flex;align-items:center;gap:14px;direction:rtl;font-family:Alexandria;font-weight:500;font-size:28px;color:var(--forest)}
.chip svg{width:40px;height:40px;fill:none;stroke:var(--forest);stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
main{position:absolute;top:180px;left:64px;right:64px;bottom:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
footer{position:absolute;left:64px;right:64px;bottom:52px;display:flex;justify-content:space-between;align-items:center;direction:ltr;border-top:1.5px solid var(--line);padding-top:26px}
.fw{display:flex;align-items:center;gap:14px}
.fwi{width:52px;height:52px;fill:none;stroke:var(--forest);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.fw small{display:block;font-size:20px;opacity:.75;direction:rtl}
.fw b{font-family:Alexandria;font-size:32px;font-weight:600;letter-spacing:1px}
.fr{display:flex;align-items:center;gap:20px}
.fr .h{font-size:26px;opacity:.85}
.cnt{background:var(--blush);color:var(--forest);font-family:Alexandria;font-weight:700;font-size:24px;padding:4px 20px;border-radius:30px;direction:rtl}
h1,h2{font-family:Alexandria;font-weight:700;line-height:1.45;letter-spacing:-.5px}
.hl{background:var(--blush);color:var(--forest);padding:0 18px;border-radius:10px;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.sub{font-size:34px;font-weight:400;opacity:.9;margin-top:26px;line-height:1.6}
.kicker{font-family:Alexandria;font-size:30px;font-weight:500;color:var(--forest);opacity:.85;letter-spacing:.5px}
h2{font-size:66px;margin-top:14px}
h2.ent{font-size:52px}
.rule{width:100%;height:1.5px;background:var(--line);margin:30px 0 34px}
/* cover */
.cover main{padding-bottom:40px}
.bigic{width:250px;height:250px;border-radius:50%;background:var(--cream);border:2px solid var(--forest);display:flex;align-items:center;justify-content:center;margin-bottom:50px;box-shadow:0 0 0 22px rgba(237,233,224,.3)}
.bigic svg{width:130px;height:130px;fill:none;stroke:var(--forest);stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round}
.coverlogo{width:420px;margin-bottom:60px}
.t-cover{font-size:80px}
.swipe{position:absolute;left:0;bottom:-10px;display:flex;align-items:center;gap:6px;font-family:Alexandria;font-size:28px;color:var(--forest);direction:rtl}
.swipe svg{width:120px;height:50px;fill:none;stroke:var(--forest);stroke-width:3.5;stroke-linecap:round;stroke-linejoin:round}
/* grid */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:30px 20px;width:100%}
.gi{display:flex;flex-direction:column;align-items:center;gap:14px}
.gc{width:136px;height:136px;border-radius:50%;background:var(--cream);border:2px solid var(--forest);display:flex;align-items:center;justify-content:center}
.gc svg{width:66px;height:66px;fill:none;stroke:var(--forest);stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}
.gc.sm{flex:none;width:118px;height:118px}.gc.sm svg{width:58px;height:58px}
.gl{font-size:29px;font-weight:500}
.grid:has(.gi:nth-child(7)) .gc{width:116px;height:116px}.grid:has(.gi:nth-child(7)) .gc svg{width:56px;height:56px}
.grid:has(.gi:nth-child(7)){gap:22px 20px}.grid:has(.gi:nth-child(7)) .gl{font-size:27px}
.pill{margin-top:64px;background:var(--forest);color:var(--cream);font-family:Alexandria;font-weight:600;font-size:30px;padding:16px 44px;border-radius:50px}
/* features + steps */
.feats,.steps{display:flex;flex-direction:column;gap:26px;width:100%;margin-top:6px}
.ft,.st{display:flex;align-items:center;gap:34px;text-align:right;background:rgba(237,233,224,.45);border:1.5px solid rgba(237,233,224,.8);border-radius:30px;padding:32px 36px}
.ftt{font-family:Alexandria;font-weight:600;font-size:40px}
.ftd{font-size:30px;opacity:.85;margin-top:6px}
.sn{flex:none;width:96px;height:96px;border-radius:50%;background:var(--blush);color:var(--forest);font-family:Alexandria;font-weight:700;font-size:50px;display:flex;align-items:center;justify-content:center}
.steps .st{padding:22px 34px}
/* prices */

.card{width:100%;background:var(--cream);color:var(--forest);border-radius:28px;padding:10px 36px;text-align:right}
.card.tight{padding:4px 32px;margin-bottom:22px}
.gh{align-self:flex-start;background:var(--forest);color:var(--cream);font-family:Alexandria;font-weight:600;font-size:28px;padding:6px 26px;border-radius:30px;margin:22px 0 14px}
.gh:first-of-type{margin-top:20px}
.row{display:flex;justify-content:space-between;align-items:center;gap:24px;padding:26px 0;border-bottom:2px dotted rgba(46,59,42,.25)}
.tight .row{padding:15px 0}
.row:last-child{border:0}
.rn{font-size:31px;font-weight:500;line-height:1.45}
.rn small{display:block;font-size:22px;font-weight:400;opacity:.7}
.rp{flex:none;background:var(--blush);border-radius:40px;padding:6px 22px;font-size:24px;font-weight:500;white-space:nowrap}
.rp b{font-family:Alexandria;font-size:30px;font-weight:700;direction:ltr;unicode-bidi:isolate}
.cur{margin-top:26px;font-size:24px;opacity:.7}
/* faq */
.faqs{display:flex;flex-direction:column;gap:26px;width:100%;margin-top:50px;text-align:right}
.q{align-self:flex-start;background:var(--blush);color:var(--forest);font-family:Alexandria;font-weight:600;font-size:44px;padding:24px 40px;border-radius:36px 36px 36px 8px;line-height:1.4}
.a{font-size:38px;line-height:1.7;padding:0 20px 50px;opacity:.95}
/* cta */
.cta main{justify-content:center}
.ctaw{display:flex;flex-direction:column;align-items:center}
.spk{width:64px;height:64px;fill:var(--cream);margin-bottom:34px}
.t-cta{font-size:76px}
.wa{margin-top:54px;display:flex;align-items:center;gap:20px;background:var(--forest);color:var(--cream);border-radius:60px;padding:16px 54px;direction:ltr}
.wa span{font-family:Alexandria;font-weight:700;font-size:64px;letter-spacing:2px}
.wai{width:64px;height:64px;fill:none;stroke:var(--cream);stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.ctalogo{width:230px;margin-top:70px;opacity:.95}
'''

def main():
    out = []
    for key, (tag, ic, slides) in C.items():
        for i, s in enumerate(slides, 1):
            out.append(slide(key, tag, ic, s, i, len(slides)))
    page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami Carousels</title>
<link href="https://fonts.googleapis.com/css2?family=Alexandria:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><svg width="0" height="0" style="position:absolute">{defs}</svg>
{''.join(out)}</body></html>'''
    open(os.path.join(HERE, 'carousels.html'), 'w', encoding='utf-8').write(page)
    print(len(out), 'slides')

main()
