// Exporte les trois créas validées (LU-FB1, ME-FB1, JE-FB2) depuis sources/creas-photo.html vers png-v2/.
// Les visuels sont dans ../assets : une balise <base> les rattache à ce dossier pendant l'export.
// Usage : node sources/export-creas-photo.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const semaine = path.resolve(__dirname, '..');
  const assets = 'file://' + path.join(semaine, 'assets') + '/';
  const html = fs.readFileSync(path.join(__dirname, 'creas-photo.html'), 'utf8')
    .replace('<head>', '<head><base href="' + assets + '">');
  const tmp = path.join(__dirname, '.creas-photo-export.html');
  fs.writeFileSync(tmp, html);
  const b = await chromium.launch();
  try {
    const p = await b.newPage({ viewport: { width: 1200, height: 1400 }, deviceScaleFactor: 1 });
    await p.goto('file://' + tmp, { waitUntil: 'load' });
    await p.waitForTimeout(800);
    const polices = await p.evaluate(async () => {
      await document.fonts.ready;
      return [...document.fonts].map(f => f.family + ' ' + f.weight + ' : ' + f.status);
    });
    console.log('polices :', polices.length ? polices.join(' | ') : 'aucune police chargée');
    const names = { b: 'LU-FB1', a: 'ME-FB1', c: 'JE-FB2' };
    for (const [id, name] of Object.entries(names)) {
      await (await p.$('#' + id)).screenshot({ path: path.join(semaine, 'png-v2', name + '.png') });
    }
    console.log('exportés :', Object.values(names).join(', '));
  } finally {
    fs.unlinkSync(tmp);
    await b.close();
  }
})();
