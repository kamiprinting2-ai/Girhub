"""Add the girl from girl.jpg as a 4th child on the left of scene.jpg (behind the left girl).
Layers: scene -> shadow -> new girl (colour/grain matched) -> occlusion shade -> scene girls (front).
"""
import numpy as np
from PIL import Image, ImageFilter, ImageChops
SC = Image.open('scene.jpg').convert('RGB'); W, H = SC.size
cut = Image.open('cut-birefnet-portrait.png').convert('RGBA')
front = Image.open('scene-girls-mask.png').convert('L')

def lab(img): return np.array(img.convert('LAB')).astype(float)
# ---- colour match: same child's face in both photos (skin boxes)
src_boxes = [(650, 700, 790, 880), (430, 1290, 540, 1480)]   # girl.jpg: face, satin centre of dress
dst_boxes = [(590, 740, 720, 890), (600, 1040, 700, 1160)]   # scene left girl (same child, same dress)
s = np.concatenate([lab(cut.convert('RGB').crop(b)).reshape(-1,3) for b in src_boxes])
d = np.concatenate([lab(SC.crop(b)).reshape(-1,3) for b in dst_boxes])
ms, ss = s.reshape(-1,3).mean(0), s.reshape(-1,3).std(0)
md, sd = d.reshape(-1,3).mean(0), d.reshape(-1,3).std(0)
k = np.clip(sd/ss, 0.8, 1.15)
L = lab(cut.convert('RGB'))
L = (L - ms) * k * 0.6 + (L - ms) * 0.4 + md  # partial std match, full mean match
L[...,0] = L[...,0]*0.97 + 2               # tiny contrast drop like the scene
rgb = Image.fromarray(np.clip(L,0,255).astype('uint8'), 'LAB').convert('RGB')

# ---- edge decontamination: pull edge colours from inside (kills white-wall halo)
a = cut.split()[3]
inner = a.point(lambda v: 255 if v > 250 else 0).filter(ImageFilter.MinFilter(5))
filled = rgb.copy()
for r in (6, 12, 24):
    blur = Image.composite(rgb, Image.new('RGB', rgb.size), inner).filter(ImageFilter.GaussianBlur(r))
    wts = inner.filter(ImageFilter.GaussianBlur(r))
    b = np.array(blur).astype(float); w = np.array(wts).astype(float)[...,None]/255
    est = np.where(w > 0.02, b / np.maximum(w, 1e-3), 0)
    f = np.array(filled).astype(float)
    edge = ((np.array(a) < 250) & (np.array(a) > 0))[...,None]
    f = np.where(edge & (w > 0.02), est, f); filled = Image.fromarray(np.clip(f,0,255).astype('uint8'))
girl = filled.convert('RGBA'); girl.putalpha(a)

# ---- scale & place (same child: match head height to her in the scene, slightly smaller = a step behind)
scale = 0.70
gw, gh = int(cut.width*scale), int(cut.height*scale)
girl = girl.resize((gw, gh), Image.LANCZOS)
face_src = (702, 773)                      # face centre in girl.jpg
fx, fy = 262, 772                           # face centre target in scene
ox, oy = int(fx - face_src[0]*scale), int(fy - face_src[1]*scale)

# ---- match sharpness + grain of the scene (phone photo, light noise)
g_rgb = girl.convert('RGB').filter(ImageFilter.GaussianBlur(0.85))
rng = np.random.default_rng(7)
n = rng.normal(0, 2.6, (gh, gw, 1)) + rng.normal(0, 1.2, (gh, gw, 3))
g_rgb = Image.fromarray(np.clip(np.array(g_rgb).astype(float) + n, 0, 255).astype('uint8'))
girl = g_rgb.convert('RGBA'); girl.putalpha(girl_a := Image.open('cut-birefnet-portrait.png').split()[3].resize((gw, gh), Image.LANCZOS))

layer = Image.new('RGBA', (W, H)); layer.paste(girl, (ox, oy))
# ---- shadow on the sofa/bolster behind her (light from front-top-left -> shadow to back-right)
sh_a = layer.split()[3].filter(ImageFilter.GaussianBlur(28))
sh_a = ImageChops.offset(sh_a, 26, 14).point(lambda v: int(v*0.38))
shadow = Image.new('RGBA', (W, H), (40, 18, 14, 0)); shadow.putalpha(sh_a)
# ---- ambient occlusion: front girl darkens the new girl where they meet
fr_blur = front.filter(ImageFilter.GaussianBlur(22))
occ = ImageChops.multiply(fr_blur, layer.split()[3]).point(lambda v: int(v*0.45))
occ_l = Image.new('RGBA', (W, H), (25, 10, 8, 0)); occ_l.putalpha(occ)
# ---- front layer: scene girls (only the left one matters, but keep mask as is)
front_l = SC.convert('RGBA'); front_l.putalpha(front)

out = SC.convert('RGBA')
for l in (shadow, layer, occ_l, front_l): out = Image.alpha_composite(out, l)
# ---- light final grade shared by everything (ties layers together)
o = np.array(out.convert('RGB')).astype(float)
o = o*1.0; o[...,0]*=1.01; o[...,2]*=0.99
final = Image.fromarray(np.clip(o,0,255).astype('uint8'))
final.save('composite.png'); final.save('composite.jpg', quality=95, dpi=(300,300))
for n_, l in [('L1-scene', SC.convert('RGBA')), ('L2-shadow', shadow), ('L3-girl', layer), ('L4-occlusion', occ_l), ('L5-front-girls', front_l)]:
    l.save(f'layer-{n_}.png')
print('placed at', ox, oy, gw, gh)
