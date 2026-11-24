"""Turn the Instagram posts into TikTok-ready media.
- 4:5 slides (1080x1350) -> 9:16 (1080x1920): background extended from the slide's own top/bottom edges
  (smooth sage gradient), slide placed high (top 170 px) so the bottom TikTok UI (caption, buttons) sits on empty space.
- Single-image posts -> 8 s silent video with a slow zoom (video gets more reach than a one-photo post; add a sound in the app).
  python3 tiktok/make_tiktok.py <in_dir> <out_dir>
"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter

W, H, TOP = 1080, 1920, 170


def to_916(src, dst):
    im = Image.open(src).convert('RGB')
    if im.size == (W, H):
        im.save(dst, quality=95); return
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)
    a = np.array(im)
    top = np.repeat(a[:1], TOP, axis=0)
    bot = np.repeat(a[-1:], H - TOP - a.shape[0], axis=0)
    canvas = Image.fromarray(np.vstack([top, a, bot]))
    blur = canvas.filter(ImageFilter.GaussianBlur(30))
    m = Image.new('L', (W, H), 255); m.paste(0, (0, TOP + 40, W, TOP + a.shape[0] - 40))
    m = m.filter(ImageFilter.GaussianBlur(25))
    Image.composite(blur, canvas, m).save(dst, quality=95)


def to_video(img, dst, secs=8):
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-i', img, '-t', str(secs),
                    '-vf', f"scale=2160:-1,zoompan=z='1+0.06*on/({secs}*30)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,format=yuv420p",
                    '-c:v', 'libx264', '-preset', 'slow', '-crf', '20', '-movflags', '+faststart', dst], check=True)


if __name__ == '__main__':
    src, out = sys.argv[1], sys.argv[2]
    for d in sorted(glob.glob(f'{src}/*/')):
        name = os.path.basename(d.rstrip('/')); o = f'{out}/{name}'; os.makedirs(o, exist_ok=True)
        imgs = sorted(glob.glob(d + '0*.png') + glob.glob(d + '0*.jpg'))
        for v in glob.glob(d + '*.mp4'):
            subprocess.run(['cp', v, o])
        for i, f in enumerate(imgs, 1):
            to_916(f, f'{o}/{i:02d}.jpg')
        if len(imgs) == 1:
            to_video(f'{o}/01.jpg', f'{o}/فيديو.mp4'); os.remove(f'{o}/01.jpg')
        print(name, len(imgs))
