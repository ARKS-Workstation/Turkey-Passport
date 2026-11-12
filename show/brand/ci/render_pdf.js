// Render an HTML file to a 1280x720 PDF (and optional PNG page previews) with the pre-installed Chromium.
// Usage: node render_pdf.js IN.html OUT.pdf [PREVIEW_DIR]
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const [inHtml, outPdf, prevDir] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  await page.goto('file://' + path.resolve(inHtml), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: outPdf, width: '1280px', height: '720px', printBackground: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  if (prevDir) {
    const sections = await page.$$('section.page');
    for (let i = 0; i < sections.length; i++) {
      await sections[i].screenshot({ path: `${prevDir}/p${String(i + 1).padStart(2, '0')}.png` });
    }
  }
  await browser.close();
})();
