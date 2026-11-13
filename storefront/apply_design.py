"""Map the flat sign artwork onto the curved, angled sign panel of the shopfront
mockup, keeping the photo's light and shade.
out: kami-shopfront-clean.jpg
"""
import cv2, numpy as np

PHOTO = '/root/.claude/uploads/ae8a957c-01bf-5da7-ab5b-f8cd01a9e49b/4543a9b5-image.jpg'
ART = '/root/.claude/uploads/ae8a957c-01bf-5da7-ab5b-f8cd01a9e49b/6038c433-image.jpg'
im = cv2.imread(PHOTO).astype(np.float32)
H, W = im.shape[:2]
art = cv2.imread(ART)
art = art[4:-4, 4:-4]                                   # drop screenshot border
ah, aw = art.shape[:2]
sign = np.load('signmask.npy')

# panel edges measured from the photo
tx, ty = np.array([60, 100, 200, 300, 400, 500, 600, 700]), np.array([404, 373, 304, 237, 182, 129, 82, 44])
bx, by = np.array([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1070]), np.array([810, 772, 738, 708, 682, 658, 636, 615, 596, 581, 573])
top = np.poly1d(np.polyfit(tx, ty, 2)); bot = np.poly1d(np.polyfit(bx, by, 2))
XL_T, XL_B, XR = 57.0, 17.0, 1086.0                     # left edge (top/bottom) and right end
G = 1.10                                                 # far (left) side is slightly compressed

xx, yy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
v = (yy - top(xx)) / (bot(xx) - top(xx))
for _ in range(3):                                       # solve for (u, v) of every photo pixel
    xl = XL_T + (XL_B - XL_T) * np.clip(v, 0, 1)
    f = (xx - xl) / (XR - xl)
    u = np.sign(f) * np.abs(f) ** (1 / G)
    v = (yy - top(xx)) / (bot(xx) - top(xx))
mapx = (u * (aw - 1)).astype(np.float32); mapy = (v * (ah - 1)).astype(np.float32)
warped = cv2.remap(art, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)

# keep the photo's lighting: panel brightness relative to its average
hsv = cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_BGR2HSV)
lum = im.mean(2)
plain = (sign > 0) & (lum < 140) & (hsv[..., 0] < 50)
vf = plain.astype(np.float32)
bg = cv2.GaussianBlur(lum * vf, (0, 0), 25) / np.maximum(cv2.GaussianBlur(vf, (0, 0), 25), 1e-3)
light = np.clip(bg / np.median(lum[plain]), 0.82, 1.12)[..., None]
warped = np.clip(warped * (0.93 * light), 0, 255)
warped = cv2.GaussianBlur(warped, (0, 0), 0.45)
grain = np.random.default_rng(2).normal(0, 1.8, warped.shape).astype(np.float32)
warped += grain

inside = ((u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)).astype(np.float32)
keep = ((xx > 1040) & (lum < 80) & (im[..., 0] > im[..., 1] + 4)).astype(np.uint8)   # dark navy trim only
keep = cv2.dilate(keep, np.ones((3, 3), np.uint8)).astype(np.float32)
m = cv2.GaussianBlur(np.minimum(sign.astype(np.float32), inside) * (1 - keep), (0, 0), 0.8)[..., None]
out = im * (1 - m) + warped * m
cv2.imwrite('kami-shopfront-clean.jpg', np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
print('ok', 'top(900)=', round(top(900)), 'bot(60)=', round(bot(60)))
