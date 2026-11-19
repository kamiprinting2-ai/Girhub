"""Print a text PNG along the front rim of the saucer in g1-clean.png (graduation carousel, slide 2).
  python3 templates/saucer_text.py <text.png>   -> templates/photos/graduation/g1-ar.png
The rim is an ellipse centred (1245, 900), a=465, b=210 (inside the outer edge); text runs from 165° to 100°.
"""
import math, os, sys
import numpy as np
from PIL import Image, ImageFilter

PH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos/graduation')
CX, CY, A, B = 1245, 900, 465, 210
T0, T1, HEIGHT = 168, 97, 92  # degrees; glyph height in px

base = Image.open(os.path.join(PH, 'g1-clean.png')).convert('RGB')
t = Image.open(sys.argv[1]).convert('RGBA'); t = t.crop(t.getbbox())
th = np.radians(np.linspace(T0, T1, 2000))
pts = np.c_[CX + A * np.cos(th), CY + B * np.sin(th)]
seg = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
k = HEIGHT / t.height; t = t.resize((round(t.width * k), HEIGHT), Image.LANCZOS)
scale = min(1, seg[-1] / t.width)
if scale < 1:
    t = t.resize((round(t.width * scale), round(t.height * scale)), Image.LANCZOS)
start = (seg[-1] - t.width) / 2
alpha = np.array(t)[:, :, 3]
layer = np.zeros((base.height, base.width), np.float32)
N = max(40, t.width // 4)
for i in range(N):
    xs, xe = int(i * t.width / N), int(min(t.width, (i + 1) * t.width / N + 2))
    s = start + (xs + xe) / 2
    j = int(np.clip(np.searchsorted(seg, s), 1, len(seg) - 1))
    p = pts[j]; d = pts[j] - pts[j - 1]
    ang = math.degrees(math.atan2(d[1], d[0]))
    sl = Image.fromarray(alpha[:, xs:xe]).rotate(-ang, resample=Image.BICUBIC, expand=True)
    x, y = int(p[0] - sl.width / 2), int(p[1] - sl.height / 2)
    a = np.array(sl, np.float32)
    layer[y:y + a.shape[0], x:x + a.shape[1]] = np.maximum(layer[y:y + a.shape[0], x:x + a.shape[1]], a)
lay = Image.fromarray(layer.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
al = np.array(lay, np.float32)[..., None] / 255 * 0.9
img = np.array(base, np.float32); ink = np.array([44, 74, 51], np.float32)
Image.fromarray((img * (1 - al) + ink * al).astype(np.uint8)).save(os.path.join(PH, 'g1-ar.png'))
print('ok', t.size, round(seg[-1]))
