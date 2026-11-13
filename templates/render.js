// Render every .post in kami-posts.html to templates/out/<id>.png (1080x1350)
// usage: node templates/render.js [query]   e.g. "p07=photos/work-1.jpg"
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async () => {
  const out = path.join(__dirname, 'out');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 1 });
  const q = process.argv[2] ? '?' + process.argv[2] : '';
  await pg.goto('file://' + path.join(__dirname, 'kami-posts.html') + q, { waitUntil: 'networkidle' });
  await pg.addStyleTag({ content: '.label{display:none}' });
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(800);
  for (const el of await pg.$$('.post')) {
    const id = await el.getAttribute('id');
    await el.screenshot({ path: path.join(out, id + '.png') });
    console.log('saved', id);
  }
  await b.close();
})();
