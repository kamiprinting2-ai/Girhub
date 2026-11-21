"""Cricut Print Then Cut pages (A4) for the winter cozy stickers.
Cricut's A4 Print Then Cut max is 18.3 x 26.98 cm; pages here are 18 x 26.5 cm, transparent PNG, 300 DPI.
Every sticker gets one solid white die-cut border (gaps closed, holes filled, ~1.5 mm offset) so Cricut cuts
one smooth outline per sticker. Sizes stay 4.5 cm (big) / 3 cm (small) on the longest side, border included.
Input: brand/stickers/winter-cozy/{4.5سم,3سم}/*.png (from templates/winter_cozy_stickers.py)
  python3 templates/winter_cozy_cricut.py
Out: brand/stickers/winter-cozy/كريكت-A4/{صفحة-N.png, منفصلة/, معاينة.jpg}
"""
import glob, os
import numpy as np, cv2
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'brand/stickers/winter-cozy')
OUT = os.path.join(SRC, 'كريكت-A4')
DPI = 300
cm = lambda v: round(v / 2.54 * DPI)
PAGE_W, PAGE_H, GAP = cm(18.0), cm(26.5), cm(0.4)
CLOSE, OFFSET = cm(0.30), cm(0.15)


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def die_cut(img, target):
    a = np.array(img.convert('RGBA'))
    pad = CLOSE + OFFSET + 10
    a = cv2.copyMakeBorder(a, pad, pad, pad, pad, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))
    m = (a[:, :, 3] > 40).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, disk(CLOSE))           # join letters / floating hearts
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    m = np.zeros_like(m); cv2.drawContours(m, cs, -1, 255, -1)        # fill holes, keep outer shape
    m = cv2.dilate(m, disk(OFFSET))                                   # white border
    m = cv2.GaussianBlur(m, (0, 0), 4); m = ((m > 127) * 255).astype(np.uint8)  # smooth cut line
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max(cs, key=cv2.contourArea)                                # one island only
    m = np.zeros_like(m); cv2.drawContours(m, [big], -1, 255, -1)
    m = cv2.GaussianBlur(m, (0, 0), 1)                                # anti-aliased edge
    base = np.zeros_like(a); base[:, :, :3] = 255; base[:, :, 3] = m
    out = np.array(Image.alpha_composite(Image.fromarray(base), Image.fromarray(a)))
    out[:, :, 3] = m                                                  # nothing outside the cut line
    out = Image.fromarray(out)
    out = out.crop(out.getbbox())
    k = target / max(out.size)
    return out.resize((round(out.width * k), round(out.height * k)), Image.LANCZOS)


class MaxRects:
    """Minimal MaxRects bin packer (best short side fit, no rotation)."""
    def __init__(self, w, h):
        self.free = [(0, 0, w, h)]

    def insert(self, w, h):
        best = None
        for fx, fy, fw, fh in self.free:
            if w <= fw and h <= fh:
                score = (min(fw - w, fh - h), max(fw - w, fh - h))
                if best is None or score < best[0]:
                    best = (score, fx, fy)
        if not best:
            return None
        _, x, y = best
        new = []
        for fx, fy, fw, fh in self.free:
            if x >= fx + fw or x + w <= fx or y >= fy + fh or y + h <= fy:
                new.append((fx, fy, fw, fh)); continue
            if x > fx: new.append((fx, fy, x - fx, fh))
            if x + w < fx + fw: new.append((x + w, fy, fx + fw - x - w, fh))
            if y > fy: new.append((fx, fy, fw, y - fy))
            if y + h < fy + fh: new.append((fx, y + h, fw, fy + fh - y - h))
        self.free = [r for r in new if not any(
            r != o and r[0] >= o[0] and r[1] >= o[1] and r[0] + r[2] <= o[0] + o[2] and r[1] + r[3] <= o[1] + o[3]
            for o in new)]
        return x, y


def pack(items):
    """Fill pages with MaxRects; biggest stickers first. GAP is kept around each sticker."""
    order = sorted(range(len(items)), key=lambda k: -(items[k][1].width * items[k][1].height))
    bins, pages = [], []
    for k in order:
        name, im = items[k]
        for b, pg in zip(bins, pages):
            pos = b.insert(im.width + GAP, im.height + GAP)
            if pos:
                pg.append((name, im, *pos)); break
        else:
            b = MaxRects(PAGE_W + GAP, PAGE_H + GAP); bins.append(b); pages.append([])
            pages[-1].append((name, im, *b.insert(im.width + GAP, im.height + GAP)))
    return pages


def main():
    os.makedirs(os.path.join(OUT, 'منفصلة'), exist_ok=True)
    items = []
    for sub, size in (('4.5سم', cm(4.5)), ('3سم', cm(3.0))):
        for f in sorted(glob.glob(os.path.join(SRC, sub, '*.png'))):
            name = os.path.basename(f)
            st = die_cut(Image.open(f), size)
            st.save(os.path.join(OUT, 'منفصلة', f'{sub}-{name}'), dpi=(DPI, DPI))
            items.append((name, st))
    big = sorted([i for i in items if max(i[1].size) > cm(3.5)], key=lambda i: -i[1].height)
    small = sorted([i for i in items if max(i[1].size) <= cm(3.5)], key=lambda i: -i[1].height)
    pages = pack(big + small)
    for old in glob.glob(os.path.join(OUT, 'صفحة-*.png')):
        os.remove(old)
    pv = []
    for n, pg in enumerate(pages, 1):
        page = Image.new('RGBA', (PAGE_W, PAGE_H), (0, 0, 0, 0))
        for _, im, x, y in pg:
            page.paste(im, (x, y), im)
        page.save(os.path.join(OUT, f'صفحة-{n}.png'), dpi=(DPI, DPI), optimize=True)
        bg = Image.new('RGBA', page.size, (200, 210, 190, 255)); bg.alpha_composite(page)
        pv.append(bg.convert('RGB').resize((PAGE_W // 4, PAGE_H // 4), Image.LANCZOS))
        print('page', n, len(pg), 'stickers')
    W = sum(p.width for p in pv) + 20 * (len(pv) + 1)
    sheet = Image.new('RGB', (W, pv[0].height + 40), '#888')
    for n, p in enumerate(pv):
        sheet.paste(p, (20 + n * (p.width + 20), 20))
    sheet.save(os.path.join(OUT, 'معاينة.jpg'), quality=90)

main()
