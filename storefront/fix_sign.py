"""Replace phone, CR and last services phrase on the storefront mockup sign."""
import cv2, numpy as np
SRC = '/root/.claude/uploads/ae8a957c-01bf-5da7-ab5b-f8cd01a9e49b/4543a9b5-image.jpg'
im = cv2.imread(SRC)
out = im.copy()

def ink(path):
    a = cv2.imread(path, cv2.IMREAD_UNCHANGED)[..., 3]
    ys, xs = np.where(a > 20)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

# name: (search box, new text png, reference png, anchor 'start-left'|'start-right')
JOBS = {
    'phone': ((58, 335, 184, 442), 'tp-phone.png', 'tp-refph.png', 'left'),
    'cr':    ((25, 762, 138, 832), 'tp-cr.png', 'tp-refcr.png', 'left'),
    'seg':   ((118, 622, 316, 722), 'tp-seg.png', 'tp-ref.png', 'right'),
}
TEXT_BGR = np.array([216, 229, 228], np.float32)

for name, ((x0, y0, x1, y1), new, ref, anchor) in JOBS.items():
    g = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
    ys, xs = np.where(g > 150)
    pts = np.stack([xs + x0, ys + y0], 1).astype(np.float32)
    (cx, cy), (L, H), ang = cv2.minAreaRect(pts)
    if H > L: L, H, ang = H, L, ang + 90
    th = np.deg2rad(ang); u = np.array([np.cos(th), np.sin(th)]); v = np.array([-np.sin(th), np.cos(th)])
    c = np.array([cx, cy])
    # 1) erase old text: mask of bright pixels inside a padded rotated box, then inpaint
    box = cv2.boxPoints(((cx, cy), (L + 6, H + 10), ang)).astype(np.int32)
    region = np.zeros(im.shape[:2], np.uint8); cv2.fillPoly(region, [box], 255)
    gray = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
    mask = ((gray > 120) & (region > 0)).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    out = cv2.inpaint(out, mask, 6, cv2.INPAINT_TELEA)
    # 2) draw new text with the same scale/angle
    ref_ink = ink(ref); new_ink = ink(new)
    s = L / ref_ink.shape[1] if name != 'seg' else 222 / new_ink.shape[1]
    W, Hn = new_ink.shape[1] * s, new_ink.shape[0] * s
    ref_h = ref_ink.shape[0] * s
    if anchor == 'left':
        start = c - u * L / 2
        tl = start - v * Hn / 2
    else:
        end = c + u * L / 2 - u * 5
        tl = end - u * W - v * Hn / 2
    h0, w0 = new_ink.shape
    srcp = np.float32([[0, 0], [w0, 0], [0, h0]])
    dstp = np.float32([tl, tl + u * W, tl + v * Hn])
    M = cv2.getAffineTransform(srcp, dstp)
    alpha = cv2.warpAffine(new_ink, M, (im.shape[1], im.shape[0]), flags=cv2.INTER_AREA).astype(np.float32) / 255
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.5)[..., None] * 0.97
    out = (out.astype(np.float32) * (1 - alpha) + TEXT_BGR * alpha).astype(np.uint8)
    print(name, 'angle', round(ang, 1), 'len', round(L), '->', round(W))

# restore the WhatsApp icon and the bullet dot exactly as in the original
for (px, py, r) in [(192, 347, 15), (318, 629, 7)]:
    m = np.zeros(im.shape[:2], np.uint8); cv2.circle(m, (px, py), r, 255, -1)
    out[m > 0] = im[m > 0]
cv2.imwrite('mockup-fixed.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 95])
