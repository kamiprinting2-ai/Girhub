"""Second batch of «من أعمالنا» posts from the owner's work photos (templates/photos/works/), Kami theme.
Sets: المدرسية (6)، مواليد وأعياد ميلاد (5)، آراء زباينا (2)، ستيكرات ثواب (2). Same look as works_carousels.py.
  python3 templates/works_carousels2.py && PAGE=works-carousels2.html OUTDIR=out/works2 node templates/render.js
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'works_carousels.py'), encoding='utf-8').read()
src = src[:src.rindex('main()')]
ns = {'__file__': os.path.join(HERE, 'works_carousels.py'), '__name__': 'works_lib'}
exec(compile(src, 'works_carousels.py', 'exec'), ns)
PH = ns['PH']

# per-photo crop: (max tall ratio, vertical focus 0=top 1=bottom)
CROP = {'occ-frame': (0.62, 0.5), 'school-pencil': (0.8, 0.25), 'school-teacher': (0.8, 0.2),
        'school-melon': (0.8, 0.4), 'review-shell': (0.8, 1.0), 'occ-birthday': (0.8, 0.45)}


def prep(name, box=(952, 720), border=14, max_ratio=0.8):
    max_ratio, fy = CROP.get(name, (max_ratio, 0.5))
    im = Image.open(os.path.join(PH, name + '.jpg')).convert('RGB')
    r = im.width / im.height
    if r < max_ratio:
        h = round(im.width / max_ratio); y = round((im.height - h) * fy)
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


ns['prep'] = prep
ns['SETS'] = {
 'school': ('المدرسية', 6, [
   ('p', 'من أعمالنا..', 'تجهيزات المدرسة', 'باسم طفلكم وصفّه، من أول يوم ✦', 'school-pencil', True),
   ('p', 'ستيكرات الأسامي..', 'لكل أغراضه', 'بالعربي والإنجليزي، وبرسمة يحبها', 'school-labels', False),
   ('p', 'هدية المعلمة..', 'مقهى المعلمين', 'قهوة وحلاو وكرت باسم الطالب ☕', 'school-teacher', False),
   ('p', 'فواصل كتب..', 'تشجّع على القراية', 'مقصوصة بالكريكت برسمة البطيخ 🍉', 'school-melon', False),
   ('p', 'وستيكر كبير..', 'بشخصية يحبها', 'مقصوص على شكل الرسمة بالضبط', 'school-croc', False),
   ('c', 'طلبات المدرسة..', 'نجهزها لكم', 'أرسلوا الاسم والصف والثيم على الواتساب ✏️'),
 ]),
 'occ': ('مواليد وأعياد ميلاد', 5, [
   ('p', 'من أعمالنا..', 'ستيكرات بالاسم', 'اسم المولود بخط عربي مع الإنجليزي ✦', 'occ-stickers', True),
   ('p', 'أكواب المولود..', 'بثيم الفيل', 'نفس الاسم والرسمة على كل كوب', 'occ-mugs', False),
   ('p', 'برواز المولود..', 'باسمه ورسمته', 'لوحة بطبقات مقصوصة تبقى ذكرى', 'occ-frame', False),
   ('p', 'وعيد الميلاد الأول..', 'بكل تفاصيله', 'تاقات وقصاصات بعبارتكم وتاريخ اليوم', 'occ-birthday', False),
   ('c', 'مناسبتكم الجاية..', 'تفاصيلها علينا', 'أرسلوا الاسم والثيم على الواتساب 🤍'),
 ]),
 'review': ('آراء زباينا', 2, [
   ('p', 'من أعمالنا..', 'وكلام زباينا', '«حده حلو.. مرررتب» 🤍 توزيعة المحار باسم المولودة', 'review-shell', False),
   ('c', 'رضاكم..', 'أحلى شي عندنا', 'اطلبوا توزيعتكم على الواتساب'),
 ]),
 'thawab': ('ستيكرات ثواب', 2, [
   ('p', 'ستيكرات ثواب..', 'لأحبابكم', 'الفاتحة باسم المرحوم، بإطار هادي وخط واضح', 'thawab', False),
   ('c', 'ثواب يوصل..', 'بإذن الله', 'أرسلوا الاسم والعبارة على الواتساب'),
 ]),
}
ns['HERE'] = HERE
code = ns['main'].__code__
# write to a different html file
import types
src_main = src  # reuse main body but change output name
exec(compile(src[src.index('def main'):].replace("'works-carousels.html'", "'works-carousels2.html'"), 'main2', 'exec'), ns)
ns['main']()
