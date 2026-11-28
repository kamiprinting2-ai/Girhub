"""Make the flag's red consistent: every red pixel close to #FF0000 (hue 0), pink highlights and dark folds reduced
to a light trace (sat keeps 25% of its drop, value keeps 40%). Anti-aliased edges against white are left alone."""
import numpy as np, cv2
from PIL import Image
im = Image.open('flag-ff0000-final.png').convert('RGB')
hsv = np.array(im.convert('HSV')).astype(np.float32)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
red = ((S > 80) & ((H < 18) | (H > 236))).astype(np.uint8)
white = ((S < 45) & (V > 190)).astype(np.uint8)
near_white = cv2.dilate(white, np.ones((7, 7), np.uint8))          # ~3 px band at red/white borders
w = red.astype(np.float32) * (1 - near_white)
w = cv2.GaussianBlur(w, (0, 0), 1.2)                                 # soft transition into the edge band
S2 = 255 - (255 - S) * 0.25
V2 = 255 - (255 - V) * 0.40
out = hsv.copy()
out[..., 0] = np.where(w > 0.01, 0, H)
out[..., 1] = S * (1 - w) + S2 * w
out[..., 2] = V * (1 - w) + V2 * w
res = Image.fromarray(np.clip(out, 0, 255).astype('uint8'), 'HSV').convert('RGB')
res.save('flag-ff0000-unified.png')
a = np.array(res).astype(int); h2 = np.array(res.convert('HSV')).astype(int)
m = red.astype(bool) & ~near_white.astype(bool)
print('inner red V pctl 1/5/50:', np.percentile(h2[..., 2][m], [1, 5, 50]), ' S pctl 1/5/25/50:', np.percentile(h2[..., 1][m], [1, 5, 25, 50]))
r = a[m]; print('within 25 levels of FF0000: %.1f%%' % ((np.abs(r - [255, 0, 0]).max(1) <= 25).mean() * 100))
