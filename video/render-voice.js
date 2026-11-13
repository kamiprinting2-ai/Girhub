// Render kami-reel-voice.html (driven by timeline.js) to MP4 with the mixed audio.
// usage: python3 video/build_audio.py && node video/render-voice.js
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const path = require('path');
const FPS = 30;
(async () => {
  const out = path.join(__dirname, 'out', 'kami-reel-voice.mp4');
  const silent = path.join(__dirname, 'out', 'video-only.mp4');
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await pg.goto('file://' + path.join(__dirname, 'kami-reel-voice.html'), { waitUntil: 'networkidle' });
  await pg.evaluate(() => document.fonts.ready);
  const dur = await pg.evaluate(() => window.TL.dur);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(FPS * dur);
  for (let i = 0; i < total; i++) {
    await pg.evaluate(t => window.renderAt(t), i / FPS);
    const buf = await pg.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log('frame', i, '/', total);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', silent, '-i', path.join(__dirname, 'out', 'mix.wav'),
    '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out]);
  console.log('done', out);
})();
