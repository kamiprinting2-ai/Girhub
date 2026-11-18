"""Build the Kami Printing website (GitHub Pages, served from /docs).
Run: python3 docs/build.py   -> docs/index.html, docs/en.html, sitemap.xml, robots.txt, llms.txt
Owner rule: never write the street address or area name in new content; the map link carries location.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = 'https://kamiprinting2-ai.github.io/Girhub/'
WA = '97366606959'
PHONE = '+97366606959'
IG = 'https://www.instagram.com/kami.printing'
MAP = 'https://www.google.com/maps/place/?q=place_id:ChIJB8Y4VgCvST4RufQY7uBzAuM'
REVIEW = 'https://search.google.com/local/writereview?placeid=ChIJB8Y4VgCvST4RufQY7uBzAuM'
UPDATED = '2026-11-18'

PRINT = [
    ('ستيكرات الشعار بقص احترافي', 'Die-cut logo stickers', 'ستيكرات بشعار مشروعكم لكل كيس وعلبة وطلبية.'),
    ('ستيكرات UV', 'UV / DTF stickers', 'ستيكرات لامعة بارزة للعلب والجارات والمنتجات.'),
    ('بطاقات الشكر', 'Thank-you cards', 'بطاقات شكر للطلبيات، وفيها مكان لاسم الزبون.'),
    ('بزنس كارد', 'Business cards', 'كروت شخصية بخامات مختارة.'),
    ('علب مطوية مطبوعة', 'Printed folding boxes', 'علب منتجات بهوية مشروعكم.'),
    ('قصاصات قطنية', 'Cotton clothing labels', 'ليبلات قطنية للملابس والإكسسوارات.'),
    ('طباعة البنرات', 'Banner printing', 'بنرات للمحلات والفعاليات.'),
    ('أكريليك', 'Acrylic printing', 'لوحات وقطع أكريليك مطبوعة.'),
    ('تغليف حراري', 'Lamination', 'تغليف الأوراق والشهادات.'),
    ('طباعة Letterhead', 'Letterhead printing', 'أوراق رسمية بشعار الشركة.'),
]
FAVORS = [
    ('توزيعات المواليد والاستقبال', 'Baby shower & newborn favors'),
    ('توزيعات الزواج والملكة', 'Wedding favors'),
    ('توزيعات أعياد الميلاد', 'Birthday favors'),
    ('توزيعات رمضان والقرقاعون', 'Ramadan & Gerga\'oon favors'),
    ('توزيعات العيد', 'Eid favors'),
    ('التوزيعات المدرسية ونهاية السنة', 'School & end-of-year favors'),
    ('ستيكرات أسماء مدرسية', 'School name stickers'),
]
CLEAR = [
    ('هيئة المعلومات والحكومة الإلكترونية', [
        ('تجديد / إصدار / بدل فاقد بطاقة الهوية', '1.500'),
        ('تحديث بيانات البطاقة الذكية', '1.500'),
        ('التقرير الائتماني من بنفت', '2.000'),
        ('شهادة الميلاد أو الوفاة (إصدار / بدل فاقد)', '1.500'),
        ('خدمة الإشعارات الحكومية', '1.500')]),
    ('وزارة الإسكان', [
        ('تقديم طلب جديد', '4.000'),
        ('طلب برنامج مزايا', '5.000'),
        ('طلب تمويل للبناء أو الشراء أو الترميم', '4.000'),
        ('الإقرار لأفراد الأسرة والموافقة عليه', '0.500')]),
    ('وزارة العمل والتنمية الاجتماعية', [
        ('تسجيل وتحديث بيانات الباحثين عن عمل', '2.000'),
        ('تسجيل حضور المواعيد في معرض التوظيف', '0.500'),
        ('ترشيح وظيفة في معرض التوظيف', '1.000'),
        ('خدمة غلاء المعيشة', '3.000'),
        ('غلاء اللحوم / تغيير الحساب / الإعاقة', '1.500'),
        ('مساعدات المؤسسة الملكية للأعمال الإنسانية', '5.000')]),
    ('وزارة التربية والتعليم', [
        ('نسخ الإفادات وكشف الدرجات', '1.500'),
        ('تحويل طلبة المدارس', '1.500'),
        ('طلب شهادات وإفادات', '1.500'),
        ('الاطلاع على نتائج الطلبة (+ الطباعة)', '0.300')]),
    ('خدمات أخرى', [
        ('بطاقة سديم (بابكو)', '1.500'),
        ('مفتاح إلكتروني جديد', '1.000'),
        ('تغيير واسترجاع المفتاح الإلكتروني', '0.500'),
        ('الاطلاع على الفواتير أو مستحقات المحكمة', '0.300'),
        ('معاملات موقع سجلات', '3.000')]),
]
FAQ = [
    ('وين أطبع ستيكرات بشعار مشروعي في البحرين؟',
     'كامي للطباعة (Kami Printing) يطبع ستيكرات الشعار بقص احترافي وستيكرات UV للمشاريع المنزلية والمتاجر في البحرين، مع بطاقات الشكر والعلب المطوية. اطلبوا على الواتساب 66606959.'),
    ('منو يسوي توزيعات مواليد وزواج في البحرين؟',
     'كامي للطباعة يجهّز توزيعات المواليد والاستقبال والزواج والملكة وأعياد الميلاد، بالاسم والتاريخ وألوان ثيم المناسبة، والتوصيل متوفر.'),
    ('هل عندكم توزيعات مدرسية باسم الطالب؟',
     'نعم، توزيعات الصف ونهاية السنة وستيكرات الأسماء والأدوات المدرسية، باسم الطالب والثيم اللي تحبونه.'),
    ('هل تخلصون معاملات حكومية؟',
     'نعم، للأفراد والشركات: البطاقة الذكية، الإسكان (طلب جديد ومزايا)، العمل والتنمية الاجتماعية، التربية والتعليم، سجلات وغيرها. الأسعار من 0.300 إلى 5.000 د.ب.'),
    ('هل التوصيل متوفر؟', 'نعم، التوصيل متوفر في البحرين.'),
    ('كيف أطلب؟', 'أرسلوا على الواتساب 66606959 نوع الطلب والعدد والتاريخ، ونرتب معاكم التصميم والتفاصيل.'),
    ('متى الدوام؟', 'السبت إلى الخميس: 8 صباحاً إلى 2 ظهراً و4 إلى 10 مساءً. الجمعة: 4 إلى 10 مساءً.'),
]

def jsonld(lang):
    days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']
    biz = {
        '@context': 'https://schema.org', '@type': ['LocalBusiness', 'Store'],
        '@id': BASE + '#business',
        'name': 'Kami Printing', 'alternateName': ['كامي للطباعة', 'Kami Printing Bahrain'],
        'description': 'Print shop and party favors in Bahrain: logo stickers, UV stickers, thank-you cards, business cards, printed boxes, cotton labels, banners, acrylic, baby/wedding/school favors, school supplies, and government transaction clearance.',
        'url': BASE, 'telephone': PHONE, 'image': BASE + 'assets/kami-printing-shop-bahrain.jpg',
        'logo': BASE + 'assets/kami-printing-logo.png', 'hasMap': MAP, 'sameAs': [IG, MAP],
        'address': {'@type': 'PostalAddress', 'addressCountry': 'BH'},
        'areaServed': {'@type': 'Country', 'name': 'Bahrain'},
        'priceRange': 'BD 0.3–5',
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': days, 'opens': '08:00', 'closes': '14:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': days, 'opens': '16:00', 'closes': '22:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Friday', 'opens': '16:00', 'closes': '22:00'}],
        'knowsAbout': ['printing', 'stickers', 'party favors', 'توزيعات', 'school favors', 'government transaction clearance', 'تخليص معاملات'],
        'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Services', 'itemListElement': [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': en, 'alternateName': ar}} for ar, en, _ in PRINT] + [
            {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': en, 'alternateName': ar}} for ar, en in FAVORS] + [
            {'@type': 'Offer', 'price': p, 'priceCurrency': 'BHD', 'itemOffered': {'@type': 'Service', 'name': n, 'category': g}}
            for g, rows in CLEAR for n, p in rows]},
    }
    faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return [biz, faq] if lang == 'ar' else [biz]

CSS = '''
:root{--sage:#A7B591;--s1:#B2BF9D;--s2:#9CAB86;--cream:#EDE9E0;--blush:#E2CDCC;--forest:#2E3B2A;--forest2:#394634}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'IBM Plex Sans Arabic',system-ui,sans-serif;color:var(--forest);background:var(--cream);line-height:1.8}
a{color:inherit}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header.hero{background:linear-gradient(165deg,var(--s1),var(--sage) 50%,var(--s2));padding:28px 0 60px}
nav{display:flex;justify-content:space-between;align-items:center;gap:12px}
nav img{height:58px}
nav .lang{font-weight:600;text-decoration:none;background:var(--cream);padding:6px 16px;border-radius:30px;font-size:15px}
.hgrid{display:grid;grid-template-columns:1.2fr .8fr;gap:36px;align-items:center;margin-top:40px}
h1,h2,h3{font-family:'Readex Pro','IBM Plex Sans Arabic',sans-serif;line-height:1.35}
h1{font-size:clamp(32px,5vw,52px)}
.hl{background:var(--blush);border-radius:10px;padding:0 12px}
.lead{font-size:19px;margin-top:16px;color:var(--forest2)}
.cta{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:40px;font-weight:600;text-decoration:none;font-size:17px}
.btn.p{background:var(--forest);color:var(--cream)}.btn.s{background:var(--cream)}
.hero img.shop{width:100%;border-radius:28px;border:8px solid var(--cream);box-shadow:0 20px 40px rgba(46,59,42,.2)}
section{padding:56px 0}
section h2{font-size:clamp(26px,3.6vw,36px);margin-bottom:8px}
section .intro{color:var(--forest2);margin-bottom:26px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}
.card{background:#fff;border-radius:20px;padding:20px;border:1px solid rgba(46,59,42,.1)}
.card h3{font-size:19px}.card p{font-size:15px;color:var(--forest2)}
.card small{display:block;font-size:13px;opacity:.6;direction:ltr;text-align:right}
.alt{background:#fff}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-top:24px}
.gal img{width:100%;border-radius:16px;display:block}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:18px;overflow:hidden;margin-bottom:18px}
caption{text-align:right;font-family:'Readex Pro';font-weight:600;padding:12px 4px;font-size:19px}
td{padding:11px 16px;border-bottom:1px dotted rgba(46,59,42,.25)}
td.p{white-space:nowrap;font-weight:700;text-align:left;direction:ltr}
details{background:#fff;border-radius:16px;padding:14px 20px;margin-bottom:10px}
summary{cursor:pointer;font-weight:600;font-size:17px}
details p{margin-top:8px;color:var(--forest2)}
.info{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
footer{background:var(--forest);color:var(--cream);padding:36px 0;font-size:15px}
footer a{color:var(--cream)}
@media(max-width:760px){.hgrid{grid-template-columns:1fr}.hero img.shop{max-width:340px;margin:0 auto;display:block}}
'''

def page_ar():
    pr = ''.join(f'<div class="card"><h3>{a}</h3><small>{e}</small><p>{d}</p></div>' for a, e, d in PRINT)
    fv = ''.join(f'<div class="card"><h3>{a}</h3><small>{e}</small></div>' for a, e in FAVORS)
    cl = ''.join(f'<table><caption>{g}</caption>' + ''.join(f'<tr><td>{n}</td><td class="p">{p} BD</td></tr>' for n, p in rows) + '</table>' for g, rows in CLEAR)
    fq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>كامي للطباعة | Kami Printing البحرين: طباعة وستيكرات وتوزيعات وتخليص معاملات</title>
<meta name="description" content="كامي للطباعة (Kami Printing) في البحرين: ستيكرات الشعار وUV، بطاقات الشكر، بزنس كارد، علب مطوية، بنرات، توزيعات المواليد والزواج والمدارس، وتخليص المعاملات الحكومية. واتساب 66606959.">
<link rel="canonical" href="{BASE}"><link rel="alternate" hreflang="ar" href="{BASE}"><link rel="alternate" hreflang="en" href="{BASE}en.html">
<link rel="icon" href="assets/icon.png">
<meta property="og:type" content="website"><meta property="og:title" content="كامي للطباعة | Kami Printing"><meta property="og:description" content="طباعة وستيكرات وتوزيعات وتخليص معاملات في البحرين"><meta property="og:image" content="{BASE}assets/kami-printing-shop-bahrain.jpg"><meta property="og:url" content="{BASE}"><meta property="og:locale" content="ar_BH">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(jsonld('ar'), ensure_ascii=False)}</script>
<style>{CSS}</style></head><body>
<header class="hero"><div class="wrap">
<nav><img src="assets/kami-printing-logo.png" alt="شعار كامي للطباعة Kami Printing"><a class="lang" href="en.html" hreflang="en">English</a></nav>
<div class="hgrid"><div>
<h1>كامي للطباعة<br><span class="hl">Kami Printing</span></h1>
<p class="lead"><strong>محل طباعة وتوزيعات في البحرين.</strong> نطبع ستيكرات الشعار وستيكرات UV وبطاقات الشكر والبزنس كارد والعلب المطوية، ونجهّز توزيعات المواليد والزواج والمدارس، ونخلّص المعاملات الحكومية للأفراد والشركات. التوصيل متوفر.</p>
<div class="cta"><a class="btn p" href="https://wa.me/{WA}">اطلبوا على الواتساب 66606959</a><a class="btn s" href="{IG}">إنستقرام <bdi dir="ltr">@kami.printing</bdi></a><a class="btn s" href="{MAP}">موقعنا على الخريطة</a></div>
</div><img class="shop" src="assets/kami-printing-shop-bahrain.jpg" alt="واجهة محل كامي للطباعة Kami Printing في البحرين" width="720" height="900"></div>
</div></header>
<main>
<section><div class="wrap"><h2>خدمات <span class="hl">الطباعة</span></h2><p class="intro">مطبوعات بهوية مشروعكم، للمشاريع المنزلية والمتاجر والشركات.</p><div class="cards">{pr}</div>
<div class="gal"><img src="assets/business.jpg" alt="مطبوعات المشاريع: ستيكرات وبطاقات شكر وعلب من كامي للطباعة" loading="lazy"><img src="assets/printing.jpg" alt="خدمات الطباعة في كامي للطباعة" loading="lazy"></div></div></section>
<section class="alt"><div class="wrap"><h2>التوزيعات <span class="hl">لكل مناسبة</span></h2><p class="intro">نصمم التوزيعة بالاسم والتاريخ وألوان ثيم المناسبة، ونغلّفها بعناية.</p><div class="cards">{fv}</div>
<div class="gal"><img src="assets/giveaways.jpg" alt="توزيعات مواليد وزواج من كامي للطباعة" loading="lazy"><img src="assets/school.jpg" alt="توزيعات مدرسية باسم الطالب" loading="lazy"></div></div></section>
<section><div class="wrap"><h2>تخليص <span class="hl">المعاملات</span></h2><p class="intro">معاملتك علينا، ووقتك لك. للأفراد والشركات. الأسعار بالدينار البحريني (آخر تحديث {UPDATED}).</p>{cl}</div></section>
<section class="alt"><div class="wrap"><h2>الأسئلة <span class="hl">الشائعة</span></h2><div style="margin-top:18px">{fq}</div></div></section>
<section><div class="wrap info">
<div class="card"><h3>الدوام</h3><p>السبت إلى الخميس: 8 AM – 2 PM و 4 PM – 10 PM<br>الجمعة: 4 PM – 10 PM</p></div>
<div class="card"><h3>تواصل معنا</h3><p>واتساب: <a href="https://wa.me/{WA}">66606959</a><br>إنستقرام: <a href="{IG}"><bdi dir="ltr">@kami.printing</bdi></a></p></div>
<div class="card"><h3>قيّمونا على قوقل</h3><p>رأيكم يفرق معانا. <a href="{REVIEW}">اكتبوا تقييمكم هنا</a></p></div>
</div></section>
</main>
<footer><div class="wrap">© كامي للطباعة · Kami Printing · البحرين · <a href="en.html">English</a></div></footer>
</body></html>'''

def page_en():
    pr = ''.join(f'<div class="card"><h3>{e}</h3><small>{a}</small></div>' for a, e, _ in PRINT)
    fv = ''.join(f'<div class="card"><h3>{e}</h3><small>{a}</small></div>' for a, e in FAVORS)
    return f'''<!doctype html><html lang="en" dir="ltr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kami Printing Bahrain | Print shop, stickers, party favors and transaction clearance</title>
<meta name="description" content="Kami Printing (كامي للطباعة) is a print shop in Bahrain: logo and UV stickers, thank-you cards, business cards, printed boxes, banners, baby/wedding/school favors and government transaction clearance. WhatsApp +973 6660 6959.">
<link rel="canonical" href="{BASE}en.html"><link rel="alternate" hreflang="ar" href="{BASE}"><link rel="alternate" hreflang="en" href="{BASE}en.html">
<link rel="icon" href="assets/icon.png">
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">{json.dumps(jsonld('en'), ensure_ascii=False)}</script>
<style>{CSS} .card small{{text-align:left;direction:rtl}}</style></head><body>
<header class="hero"><div class="wrap">
<nav><img src="assets/kami-printing-logo.png" alt="Kami Printing logo"><a class="lang" href="./" hreflang="ar">العربية</a></nav>
<div class="hgrid"><div>
<h1>Kami Printing <span class="hl">Bahrain</span></h1>
<p class="lead"><strong>A print shop and party-favor studio in Bahrain.</strong> Logo stickers, UV stickers, thank-you cards, business cards, printed folding boxes, cotton labels, banners and acrylic; baby, wedding and school favors; school supplies; and government transaction clearance for individuals and companies. Delivery available.</p>
<div class="cta"><a class="btn p" href="https://wa.me/{WA}">Order on WhatsApp +973 6660 6959</a><a class="btn s" href="{IG}">Instagram</a><a class="btn s" href="{MAP}">Google Maps</a></div>
</div><img class="shop" src="assets/kami-printing-shop-bahrain.jpg" alt="Kami Printing shop front in Bahrain" width="720" height="900"></div>
</div></header>
<main>
<section><div class="wrap"><h2>Printing services</h2><div class="cards">{pr}</div></div></section>
<section class="alt"><div class="wrap"><h2>Party &amp; school favors</h2><div class="cards">{fv}</div></div></section>
<section><div class="wrap"><h2>Government transaction clearance</h2><p class="intro">Smart ID card, housing (new application, Mazaya), labour and social development, education certificates, Sijilat and more. Prices from BD 0.300 to BD 5.000. Full price list on the <a href="./">Arabic page</a>.</p></div></section>
<section class="alt"><div class="wrap info">
<div class="card"><h3>Hours</h3><p>Sat–Thu: 8 AM – 2 PM and 4 PM – 10 PM<br>Fri: 4 PM – 10 PM</p></div>
<div class="card"><h3>Contact</h3><p>WhatsApp <a href="https://wa.me/{WA}">+973 6660 6959</a><br>Instagram <a href="{IG}">@kami.printing</a></p></div>
</div></section></main>
<footer><div class="wrap">© Kami Printing · كامي للطباعة · Bahrain</div></footer></body></html>'''

def main():
    w = lambda n, s: open(os.path.join(HERE, n), 'w', encoding='utf-8').write(s)
    w('index.html', page_ar()); w('en.html', page_en())
    w('robots.txt', f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    w('sitemap.xml', f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
      f'<url><loc>{BASE}</loc><lastmod>{UPDATED}</lastmod></url>\n<url><loc>{BASE}en.html</loc><lastmod>{UPDATED}</lastmod></url>\n</urlset>\n')
    lines = [f'# Kami Printing (كامي للطباعة)', '', '> Print shop and party-favor studio in Bahrain. WhatsApp +973 6660 6959, Instagram @kami.printing. Delivery available.', '',
             '## Printing', *[f'- {e} ({a})' for a, e, _ in PRINT], '', '## Favors', *[f'- {e} ({a})' for a, e in FAVORS], '',
             '## Government transaction clearance (BHD)', *[f'- {g}: {n}: {p}' for g, rows in CLEAR for n, p in rows], '',
             '## Hours', '- Sat–Thu 08:00–14:00 and 16:00–22:00; Fri 16:00–22:00', '',
             '## Links', f'- Arabic: {BASE}', f'- English: {BASE}en.html', f'- Google Maps: {MAP}', f'- Instagram: {IG}']
    w('llms.txt', '\n'.join(lines) + '\n')
    w('.nojekyll', '')
    print('built')

main()
