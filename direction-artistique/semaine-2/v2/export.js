// Usage : node export.js <page.html> <dossier_sortie>
// Exporte chaque élément [data-name] de la page en PNG, à sa taille (1080 x 1350 ou 1080 x 1920).
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [, , input, outdir] = process.argv;
  const out = path.resolve(outdir);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  const items = page.locator('[data-name]');
  const n = await items.count();
  for (let i = 0; i < n; i++) {
    const el = items.nth(i);
    const name = await el.getAttribute('data-name');
    await el.screenshot({ path: path.join(out, name + '.png') });
    console.log('PNG :', name + '.png');
  }
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
