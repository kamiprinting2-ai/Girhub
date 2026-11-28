"""Make the flag's white band bright/clean: lift low-saturation pixels toward pure white, keep ~35% of the fold shading."""
import numpy as np
from PIL import Image
im = Image.open('flag-ff0000.png').convert('RGB')
rgb = np.array(im).astype(float); hsv = np.array(im.convert('HSV')).astype(float)
S = hsv[..., 1]
w = np.clip((45 - S) / 25, 0, 1)[..., None]          # 1 = white/grey, 0 = red
lum = rgb.mean(2, keepdims=True)
white = 255 - (255 - lum) * 0.35                      # neutral, brighter, folds kept lightly
out = rgb * (1 - w) + np.repeat(white, 3, 2) * w
Image.fromarray(np.clip(out, 0, 255).astype('uint8')).save('flag-ff0000-white.png')
o = np.array(Image.open('flag-ff0000-white.png').convert('RGB')).astype(int)
h = np.array(Image.open('flag-ff0000.png').convert('HSV')).astype(int)
m = (h[100:1000, 0:500, 1] < 40) & (h[100:1000, 0:500, 2] > 120)
print('white band brightness pctl 5/25/50/75/95:', np.percentile(o[100:1000, 0:500][m].mean(1), [5, 25, 50, 75, 95]).round())
