"""Crop the flag ribbon from the owner's post (source-2160x2700.png) and shift its reds to pure #FF0000, keeping the folds/shading."""
import numpy as np
from PIL import Image
im = Image.open('source-2160x2700.png').convert('RGB').crop((0, 80, 2160, 1530))
hsv = np.array(im.convert('HSV')).astype(float)
H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
red = (S > 60) & ((H < 18) | (H > 238))
Sm, Vm = np.median(S[red]), np.median(V[red])
print('median S,V', Sm, Vm)
# soft weight so anti-aliased edges blend
w = np.clip((S - 25) / 50, 0, 1) * ((H < 22) | (H > 234))
Sn = np.clip(S * 255 / Sm, 0, 255)
r = V / Vm
Vn = np.clip(V * 255 / Vm, 0, 255)
Sn = Sn * np.clip(1 - 1.4 * np.clip(r - 1, 0, None), 0.55, 1)
out = hsv.copy()
out[..., 0] = np.where(w > 0, 0, H)
out[..., 1] = S * (1 - w) + Sn * w
out[..., 2] = V * (1 - w) + Vn * w
res = Image.fromarray(out.clip(0, 255).astype('uint8'), 'HSV').convert('RGB')
res.save('flag-ff0000.png')
a = np.array(res).reshape(-1, 3)[red.reshape(-1)]
print('new median RGB', np.median(a, axis=0))
