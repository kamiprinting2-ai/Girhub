"""Remove the straight vertical seam in the ribbon tail (from the owner's source art, x~1909) by spreading the step over 40 px."""
import numpy as np
from PIL import Image
im = Image.open('flag-ff0000-final.png').convert('RGB'); a = np.array(im).astype(float)
X, R = 1909, 40
h = a.shape[0]
d = a[:, X+1:X+4].mean(1) - a[:, X-4:X-1].mean(1)          # step per row (3 channels)
mag = np.abs(d).max(1)
rows = np.where(mag > 5)[0]
rows = rows[(rows > 900) & (rows < 1146)]                    # tail area above the crease only
print('rows fixed', rows.min(), rows.max(), len(rows))
for y in rows:
    for x in range(X - R, X + 1):
        t = 1 - (X - x) / R                                   # 0 far left -> 1 at seam
        a[y, x] += d[y] * t * 0.5
    for x in range(X + 1, X + R + 1):
        t = 1 - (x - X - 1) / R
        a[y, x] -= d[y] * t * 0.5
Image.fromarray(np.clip(a, 0, 255).astype('uint8')).save('flag-ff0000-final.png')
b = np.array(Image.open('flag-ff0000-final.png').convert('RGB')).astype(float)
print('max step after', np.abs(b[rows][:, X+1:X+4].mean(1) - b[rows][:, X-4:X-1].mean(1)).max().round(1))

# pass 2: feathered horizontal blur across the seam (x 1905±70, rows 953-1145) to hide the change of shading direction
import cv2
a = np.array(Image.open('flag-ff0000-final.png').convert('RGB')).astype(np.float32)
blur = cv2.GaussianBlur(a, (0, 0), sigmaX=22, sigmaY=1.5)
m = np.zeros(a.shape[:2], np.float32)
m[953:1146, 1905-70:1905+70] = 1
m = cv2.GaussianBlur(m, (0, 0), 18)[..., None]
out = a * (1 - m) + blur * m
Image.fromarray(np.clip(out, 0, 255).astype('uint8')).save('flag-ff0000-final.png')
print('pass 2 done')
