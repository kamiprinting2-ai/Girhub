"""Remove the confirmed grey speck(s) inside the flag's white band. Positions checked by eye; edges/contours untouched."""
import numpy as np, cv2
from PIL import Image
a = np.array(Image.open('flag-ff0000-unified.png').convert('RGB'))
g = cv2.cvtColor(a, cv2.COLOR_RGB2GRAY).astype(np.int16)
gm = cv2.cvtColor(cv2.medianBlur(a, 9), cv2.COLOR_RGB2GRAY).astype(np.int16)
mask = np.zeros(g.shape, np.uint8)
for (x, y) in [(559, 456)]:                  # speck seen in the white band (not edges)
    box = (slice(y - 6, y + 8), slice(x - 6, x + 8))
    mask[box] = (((gm - g)[box] > 6) * 255).astype(np.uint8)
mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
print('speck px:', int((mask > 0).sum()))
Image.fromarray(cv2.inpaint(a, mask, 4, cv2.INPAINT_TELEA)).save('flag-ff0000-unified.png')
