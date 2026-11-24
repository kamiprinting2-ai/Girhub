"""«كيف نجهز طلبكم» تعديل 1: real order «دانة» step by step (8 slides, تعديل 2: بدون سلايد الهوية). Same Kami look as works_carousels.py.
  python3 templates/works_how_dana.py && PAGE=works-how-dana.html OUTDIR=out/how-dana node templates/render.js
"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'works_carousels2.py'), encoding='utf-8').read()
src = src[:src.index("ns['SETS']")]
g = {'__file__': os.path.join(HERE, 'works_carousels2.py'), '__name__': 'dana_lib'}
exec(compile(src, 'works_carousels2.py', 'exec'), g)
ns = g['ns']
g['CROP'].update({'dana-ribbons': (0.8, 0.45), 'dana-whatsapp': (0.7, 0.0), 'dana-cutting': (0.8, 0.55),
                  'dana-note': (0.8, 0.3), 'dana-tag': (0.8, 0.6), 'dana-display': (0.8, 0.7), 'dana-boxed': (0.8, 0.5)})
photo, cta, CSS, EXTRA = ns['photo'], ns['cta'], ns['CSS'], ns['EXTRA']
TAG, N = 'كيف نجهز طلبكم', 8
S = [
 ('كيف نجهز طلبكم؟', 'طلب دانة من البداية', 'قصة طلب حقيقي، خطوة بخطوة ✦', 'dana-shell', True),
 ('١. نرسل العينة..', 'قبل التنفيذ', '«حده حلو.. مرررتب» كان رد الزبونة على العينة 🤍', 'dana-whatsapp', False),
 ('٢. نطبع ونقص..', 'بالكريكت', 'تاقات على شكل المحارة، مقصوصة بدقة', 'dana-cutting', False),
 ('٣. نركّب يدوي..', 'قطعة قطعة', 'كل تاق يدخل فيه الشريط باليد', 'dana-ribbons', False),
 ('٤. نكمّل التفاصيل..', 'بعبارتكم', '«أنا أول فرحة لماما وبابا» على ورق بحواف مقصوصة', 'dana-note', False),
 ('٥. نغلّف ونرتب..', 'حبة حبة', 'علب شفافة، وكل توزيعة بمكانها', 'dana-boxed', False),
 ('٦. ويوم المناسبة..', 'كل شي جاهز', 'علب دانة وتوزيعاتها على الطاولة', 'dana-display', False),
]
out = [photo('how', i, N, TAG, *s) for i, s in enumerate(S, 1)]
out.append(cta('how', 8, N, TAG, 'مناسبتكم الجاية..', 'نجهزها بنفس الاهتمام', 'أرسلوا التفاصيل على الواتساب 🤍'))
page = f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>Kami How Dana</title>
<link href="https://fonts.googleapis.com/css2?family=Readex+Pro:wght@500;600;700&family=IBM+Plex+Sans+Arabic:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}{EXTRA}</style></head><body>{''.join(out)}</body></html>'''
open(os.path.join(HERE, 'works-how-dana.html'), 'w', encoding='utf-8').write(page)
print(len(out), 'slides')
