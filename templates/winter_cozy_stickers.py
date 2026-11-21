"""Winter cozy stickers at print sizes: big 4.5 cm, small 3 cm (longest side), 300 DPI.
Source: brand/stickers/winter-cozy/الصفحة-الأصلية.webp (the owner's transparent sheet, same as Drive
«ستيكرات شتوية كريكت/المصدر»). Each sticker is cut out, upscaled x4 with EDSR (OpenCV dnn_superres) when
the model is given, then sized exactly and laid out on A4 pages.
  python3 templates/winter_cozy_stickers.py [path/to/EDSR_x4.pb]
Out: brand/stickers/winter-cozy/{4.5سم,3سم}/*.png, A4-صفحة-N.png, ستيكرات-شتوية-A4.pdf, معاينة.jpg
"""
import os, sys
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'brand/stickers/winter-cozy')
DPI = 300
cm = lambda v: round(v / 2.54 * DPI)
BIG, SMALL = cm(4.5), cm(3.0)

NAMES = ['تفاحة وكتب', 'دفء القهوة', 'لحظات لنفسي', 'دفا و وناسة', 'قلبي دافي', 'ظرف ثلج', 'فانوس', 'الجو يونس',
         'قفازات وردية', 'رجل الثلج', 'تحذير ثلج', 'ساعة رملية', 'قلب صوف', 'رجل الثلج بسماعات', 'طاقية صوف',
         'ندفة ثلج 1', 'جوراب', 'شمعة', 'قفازات زرقاء', 'كوب كاكاو', 'ندفة ثلج 2', 'ندفة ثلج 3', 'ندفة ثلج 4',
         'ندفة ثلج 5', 'ندفة ثلج 6', 'ندفة ثلج 7', 'But First Hot Chocolate', 'مارشميلو', 'كوكيز 1', 'كوكيز 2',
         'Cozy Vibes', 'قرفة', 'غيمة ثلج', 'Hello Winter', 'قلب بني 1', 'قلب بني 2', 'هلا بالشتاء', 'قلب بني 3',
         'قلب بني 4', 'قلب صوف 2', 'قلب بني 5', 'قلب بني 6', 'قلب بني 7', 'أجواء شتوية', 'قلب بني 8',
         'حلاته باللمة', 'رشفة سعادة', 'دفي قلبك']
SMALL_IDX = {15, 20, 21, 22, 23, 24, 25, 34, 35, 37, 38, 40, 41, 42, 44}


def cut(sheet):
    a = np.array(sheet)
    m = (a[:, :, 3] > 10).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((15, 15), np.uint8)), 8)
    comps = [(tuple(int(v) for v in st[i][:4]), i) for i in range(1, n) if st[i][4] > 200]
    comps.sort(key=lambda c: (c[0][1] // 60, c[0][0]))
    # the lone dot under «دفي قلبك» joins the word above it
    merged = []
    for b, i in comps:
        if b[2] < 40 and b[3] < 40 and merged:
            pb, pi = merged[-1]
            x0, y0 = min(pb[0], b[0]), min(pb[1], b[1])
            x1, y1 = max(pb[0] + pb[2], b[0] + b[2]), max(pb[1] + pb[3], b[1] + b[3])
            merged[-1] = ((x0, y0, x1 - x0, y1 - y0), pi + [i])
        else:
            merged.append((b, [i]))
    assert len(merged) == len(NAMES), len(merged)
    out = []
    for (x, y, w, h), ids in merged:
        keep = np.isin(lab, ids)[y:y + h, x:x + w]
        crop = a[y:y + h, x:x + w].copy()
        crop[~keep] = 0
        out.append(Image.fromarray(crop))
    return out


def upscale(img, sr):
    img = np.array(img)
    rgb = img[:, :, :3].astype(np.float32); al = img[:, :, 3:4].astype(np.float32) / 255
    flat = (rgb * al + 255 * (1 - al)).astype(np.uint8)  # on white, so edges don't go dark
    pad = 8
    flat = cv2.copyMakeBorder(flat, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(255, 255, 255))
    alp = cv2.copyMakeBorder(img[:, :, 3], pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=0)
    H, W = alp.shape
    big = sr.upsample(flat[:, :, ::-1])[:, :, ::-1] if sr else cv2.resize(flat, (W * 4, H * 4), interpolation=cv2.INTER_LANCZOS4)
    A = cv2.resize(alp, (W * 4, H * 4), interpolation=cv2.INTER_CUBIC)
    A = np.clip((A.astype(np.float32) - 128) * 2.2 + 128, 0, 255).astype(np.uint8)  # crisper cut edge
    return Image.fromarray(np.dstack([big, A]))


def fit(img, side):
    bb = img.getbbox(); img = img.crop(bb)
    k = side / max(img.size)
    return img.resize((max(1, round(img.width * k)), max(1, round(img.height * k))), Image.LANCZOS)


def pages(items):
    W, H, M, G = cm(21), cm(29.7), cm(0.8), cm(0.4)
    out, page, x, y, row = [], None, M, M, 0
    def new():
        p = Image.new('RGB', (W, H), 'white'); out.append(p); return p
    page = new()
    for im in items:
        if x + im.width > W - M:
            x, y, row = M, y + row + G, 0
        if y + im.height > H - M:
            page = new(); x, y, row = M, M, 0
        page.paste(im, (x, y), im)
        x += im.width + G; row = max(row, im.height)
    return out


def main():
    sr = None
    if len(sys.argv) > 1:
        sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel(sys.argv[1]); sr.setModel('edsr', 4)
    sheet = Image.open(os.path.join(OUT, 'الصفحة-الأصلية.webp')).convert('RGBA')
    big, small = [], []
    for k, (img, name) in enumerate(zip(cut(sheet), NAMES)):
        size = SMALL if k in SMALL_IDX else BIG
        st = fit(upscale(img, sr), size)
        sub = '3سم' if k in SMALL_IDX else '4.5سم'
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
        st.save(os.path.join(OUT, sub, f'{k + 1:02d}-{name}.png'), dpi=(DPI, DPI))
        (small if k in SMALL_IDX else big).append(st)
        print(k + 1, name, sub, st.size)
    ps = pages(sorted(big, key=lambda i: -i.height) + sorted(small, key=lambda i: -i.height))
    for n, p in enumerate(ps, 1):
        p.save(os.path.join(OUT, f'A4-صفحة-{n}.png'), dpi=(DPI, DPI))
    ps[0].save(os.path.join(OUT, 'ستيكرات-شتوية-A4.pdf'), save_all=True, append_images=ps[1:], resolution=DPI)
    pv = Image.new('RGB', (sum(p.width // 4 for p in ps) + 20 * (len(ps) + 1), ps[0].height // 4 + 40), '#ddd')
    for n, p in enumerate(ps):
        pv.paste(p.resize((p.width // 4, p.height // 4), Image.LANCZOS), (20 + n * (p.width // 4 + 20), 20))
    pv.save(os.path.join(OUT, 'معاينة.jpg'), quality=90)
    print(len(ps), 'pages')

main()
