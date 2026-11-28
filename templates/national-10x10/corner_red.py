"""Make the flag's back panel (top-right corner area) pure #FF0000; keep a thin soft shadow where it meets the ribbon."""
import numpy as np, cv2
from PIL import Image
im = Image.open('flag-ff0000-white.png').convert('RGB')
rgb = np.array(im).astype(float); hsv = np.array(im.convert('HSV')).astype(float)
H, S, V = hsv[...,0], hsv[...,1], hsv[...,2]
red = (S > 150) & ((H < 15) | (H > 240))
dark = (red & (V < 250)).astype(np.uint8)
n, lab = cv2.connectedComponents(dark, connectivity=8)
h, w = dark.shape
# the back panel = the dark-red component touching the top-right corner
ids = set(np.unique(lab[0:5, w-200:w])) | set(np.unique(lab[0:300, w-5:w]))
ids.discard(0)
panel = np.isin(lab, list(ids)).astype(np.uint8)
print('panel components', ids, 'panel px', panel.sum())
# distance (px) from the panel edge facing the ribbon: keep shadow only within ~45 px of non-panel red
inside = cv2.distanceTransform(panel, cv2.DIST_L2, 5)
keep = np.clip(1 - inside / 45.0, 0, 1) * 0.6          # 60% of the original shadow at the edge, fading to 0
keep = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 6)
Vn = np.where(panel > 0, 255 - (255 - V) * keep, V)
soft = cv2.GaussianBlur(panel.astype(np.float32), (0, 0), 1.5)  # smooth the transition at panel border
out = hsv.copy(); out[...,2] = V * (1 - soft) + Vn * soft
out[...,0] = np.where(soft > 0, 0, H); out[...,1] = np.where(soft > 0, np.maximum(S, 254) * soft + S * (1 - soft), S)
res = Image.fromarray(np.clip(out, 0, 255).astype('uint8'), 'HSV').convert('RGB')
res.save('flag-ff0000-final.png')
a = np.array(res).astype(int)
for (x, y) in [(w-20, 20), (w-200, 150), (w-400, 300), (w-300, 600), (w-100, 900), (1500, 100), (1200, 250)]:
    print((x, y), a[y, x])
