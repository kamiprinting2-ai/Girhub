// Render reel.html to MP4 frames (1080x1920, 30fps). usage: node video/cups-reel/render.js out.mp4 [stills]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = 30, DUR = 12;
(async () => {
  const out = process.argv[2];
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, 'reel.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  if (process.argv[3] === 'stills') {
    for (const t of [0.4, 1.5, 4.5, 6.8, 8.6, 11.0]) {
      await pg.evaluate(t => window.renderAt(t), t);
      await pg.screenshot({ path: path.join(out, `still-${t}.jpg`), type: 'jpeg', quality: 80 });
    }
    await b.close(); return;
  }
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'slow', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < FPS * DUR; i++) {
    await pg.evaluate(t => window.renderAt(t), i / FPS);
    const buf = await pg.screenshot({ type: 'jpeg', quality: 93 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close();
  console.log('done', out);
})();
