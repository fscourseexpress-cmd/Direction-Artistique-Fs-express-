// Rend index.html image par image (30 i/s, 18 s) et encode le MP4 avec ffmpeg.
// Usage : node render.js
//         REVIEW_DIR=/chemin node render.js   (écrit aussi quelques images de contrôle)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const FPS = 30;
const DURATION = 18.0;
const FRAMES = Math.round(FPS * DURATION);
const OUT = path.join(__dirname, 'qui-sommes-nous.mp4');
const REVIEW = process.env.REVIEW_DIR;
const REVIEW_AT = [1.0, 3.6, 5.0, 8.0, 12.0, 15.6, 17.4];

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.join(__dirname, 'index.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(1500);

  const ff = spawn('ffmpeg', [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium',
    '-movflags', '+faststart', OUT,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });

  const done = new Set();
  for (let i = 0; i < FRAMES; i++) {
    const t = i / FPS;
    await page.evaluate((tt) => window.setT(tt), t);
    const jpg = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (REVIEW) {
      const k = REVIEW_AT.find((r) => Math.abs(r - t) < 0.5 / FPS && !done.has(r));
      if (k !== undefined) {
        done.add(k);
        fs.writeFileSync(path.join(REVIEW, `t${k.toFixed(1)}.jpg`), jpg);
      }
    }
    if (!ff.stdin.write(jpg)) await new Promise((r) => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise((r) => ff.on('close', r));
  await browser.close();
  console.log('MP4 :', OUT, '| images :', FRAMES);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
