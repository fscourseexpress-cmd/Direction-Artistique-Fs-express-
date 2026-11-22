// Exporte chaque visuel de creas-v2.html en PNG (png-v2/) et signale ce qui sort du cadre.
const { chromium } = require('playwright');
(async () => {
  const only = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/creas-v2.html', { waitUntil: 'load' });
  await p.evaluate(() => document.body.classList.add('export'));
  await p.waitForTimeout(1500);
  const issues = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('.crea').forEach(c => {
      const cr = c.getBoundingClientRect();
      c.querySelectorAll('.tb, .tb *, .cta, .notif, .bbl, .stk, .logo, .pg, .k, .cap').forEach(e => {
        const r = e.getBoundingClientRect();
        if (!r.width) return;
        if (r.right > cr.right - 12 || r.bottom > cr.bottom - 12 || r.left < cr.left + 12 || r.top < cr.top + 12)
          out.push(c.id + ': ' + (e.className.baseVal ?? e.className) + ' hors cadre');
      });
    });
    return [...new Set(out)];
  });
  console.log(issues.length ? issues.join('\n') : 'aucun débordement');
  let n = 0;
  for (const el of await p.$$('.crea')) {
    const id = await el.getAttribute('id');
    if (only && !id.startsWith(only)) continue;
    await el.screenshot({ path: 'png-v2/' + id + '.png' }); n++;
  }
  console.log('exportés :', n);
  await b.close();
})();
