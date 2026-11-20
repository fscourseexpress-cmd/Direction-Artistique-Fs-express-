// Exporte chaque créa de creas.html en PNG (taille réelle) et signale les débordements.
const { chromium } = require('playwright');
(async () => {
  const only = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/creas.html', { waitUntil: 'load' });
  await p.evaluate(() => document.body.classList.add('export'));
  await p.waitForTimeout(1200);
  const issues = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.crea').forEach(c => {
      const cr = c.getBoundingClientRect();
      c.querySelectorAll('.hdr,.mid,.ftr,.mid *,.ftr *').forEach(e => {
        const r = e.getBoundingClientRect();
        if (!r.width) return;
        if (r.right > cr.right - 20 || r.bottom > cr.bottom - 20 || r.left < cr.left + 20 || r.top < cr.top + 20)
          out.push(c.id + ': ' + (e.className.baseVal ?? e.className) + ' hors marge');
      });
      const m = c.querySelector('.mid');
      if (m && m.scrollHeight > m.clientHeight + 2) out.push(c.id + ': contenu trop haut (' + (m.scrollHeight - m.clientHeight) + 'px)');
    });
    return [...new Set(out)];
  });
  console.log(issues.length ? issues.join('\n') : 'aucun débordement');
  const els = await p.$$('.crea');
  let n = 0;
  for (const el of els) {
    const id = await el.getAttribute('id');
    if (only && !id.startsWith(only)) continue;
    await el.screenshot({ path: 'png/' + id + '.png' }); n++;
  }
  console.log('exportées :', n);
  await b.close();
})();
