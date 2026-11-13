"""Shopfront mockup: recolor the sign to the brand sage and replace the AI-made
logo with the real Kami logo, warped to the sign's angle.
input: mockup-fixed.jpg (sign text already corrected) -> kami-shopfront-clean.jpg
"""
import cv2, numpy as np

im = cv2.imread('mockup-fixed.jpg').astype(np.float32)
H, W = im.shape[:2]
lum = im.mean(2)

# ---------- sign region (olive panel incl. its text) ----------
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV)
olive = ((hsv[..., 0] > 18) & (hsv[..., 0] < 50) & (hsv[..., 1] > 45) & (hsv[..., 2] > 60) & (hsv[..., 2] < 175)).astype(np.uint8)
olive[870:] = 0
n, lab, st, _ = cv2.connectedComponentsWithStats(olive)
big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
olive = (lab == big).astype(np.uint8)
cnts, _ = cv2.findContours(cv2.morphologyEx(olive, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8)), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
sign = np.zeros_like(olive); cv2.drawContours(sign, [max(cnts, key=cv2.contourArea)], -1, 1, -1)
sign = cv2.erode(sign, np.ones((3, 3), np.uint8))

# ---------- local background colour of the panel (ignoring text/logo) ----------
def bg_estimate(img, valid, k=61):
    v = valid.astype(np.float32)
    num = cv2.GaussianBlur(img * v[..., None], (0, 0), k / 3)
    den = cv2.GaussianBlur(v, (0, 0), k / 3)[..., None]
    return num / np.maximum(den, 1e-3)

bright = (lum > 140) | ((hsv[..., 1] < 60) & (lum > 110))           # white text / lilac
lilac = (hsv[..., 0] > 120) & (hsv[..., 1] > 25) & (lum > 120)
fgmask = cv2.dilate((bright | lilac).astype(np.uint8), np.ones((7, 7), np.uint8))
bg_old = bg_estimate(im, (olive > 0) & (fgmask == 0))

# ---------- 1) erase the old logo area ----------
yy, xx = np.mgrid[0:H, 0:W]
arabic_top = 612 - (xx - 190) * 0.29              # stay above the Arabic services line
logo_zone = (xx > 195) & (xx < 790) & (yy > 100) & (yy < arabic_top) & (sign > 0)
erase = (fgmask > 0) & logo_zone
erase = cv2.dilate(erase.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
grain = cv2.GaussianBlur(np.random.default_rng(1).normal(0, 2.2, (H, W)).astype(np.float32), (0, 0), 0.7)[..., None]
im = np.where(erase[..., None], bg_old + grain, im)

# ---------- 2) recolour olive -> brand sage, keeping light & shade ----------
target = np.array([145, 181, 167], np.float32) * 0.86              # BGR of #A7B591, in the awning's shade
ref = np.median(bg_old[sign > 0], 0)
bg_new = bg_old * (target / ref)
lum_bg = bg_old.mean(2, keepdims=True)
t = np.clip((im.mean(2, keepdims=True) - lum_bg) / np.maximum(225 - lum_bg, 1), 0, 1)   # 1 = text
rec = im + (1 - t) * (bg_new - bg_old)
soft = cv2.GaussianBlur(sign.astype(np.float32), (0, 0), 1.2)[..., None]
im = im * (1 - soft) + rec * soft

# crisper small text on the lighter panel
cream = np.array([224, 233, 237], np.float32)
tt = np.clip((t - 0.15) / 0.6, 0, 1) * soft
im = im + tt * (cream - im) * 0.75

# ---------- 3) place the real logo ----------
logo = cv2.imread('../brand/logo-en-cream.png', cv2.IMREAD_UNCHANGED).astype(np.float32)
lh, lw = logo.shape[:2]
ang = np.deg2rad(-21)
u = np.array([np.cos(ang), np.sin(ang)]); v = np.array([0.05, 0.9987])
C = np.array([478, 392]); s = 0.61
hw, hh = lw * s / 2, lh * s / 2
TL = C - u * hw - v * hh * 0.92; TR = C + u * hw - v * hh * 1.08
BR = C + u * hw + v * hh * 1.08; BL = C - u * hw + v * hh * 0.92
M = cv2.getPerspectiveTransform(np.float32([[0, 0], [lw, 0], [lw, lh], [0, lh]]), np.float32([TL, TR, BR, BL]))
warp = cv2.warpPerspective(logo, M, (W, H), flags=cv2.INTER_AREA)
a = cv2.GaussianBlur(warp[..., 3] / 255, (0, 0), 0.45)[..., None]
col = warp[..., :3]
shade = np.clip(bg_new.mean(2, keepdims=True) / target.mean(), 0.85, 1.12)   # follow panel lighting
col = np.clip(col * shade, 0, 255)
im = im * (1 - a) + col * a

out = np.clip(im, 0, 255).astype(np.uint8)
cv2.imwrite('kami-shopfront-clean.jpg', out, [cv2.IMWRITE_JPEG_QUALITY, 95])
print('done', ref.round(1))
