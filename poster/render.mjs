// Render poster.html to a print PDF (A0) and a PNG preview.
// usage: node render.mjs   (needs playwright-core; Chromium at /opt/pw-browsers)
import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const dir = path.dirname(fileURLToPath(import.meta.url));
const exe = fs.readdirSync('/opt/pw-browsers').filter(d => d.startsWith('chromium-'))
  .map(d => `/opt/pw-browsers/${d}/chrome-linux/chrome`).find(fs.existsSync);
const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 3179, height: 4494 } }); // 841x1189mm @96dpi
await page.goto('file://' + path.join(dir, 'poster.html'));
await page.evaluate(() => document.fonts.ready);
const overflow = await page.evaluate(() => {
  const p = document.querySelector('.page');
  return { scroll: p.scrollHeight, client: p.clientHeight };
});
console.log('page height px', overflow);
await page.pdf({ path: path.join(dir, 'emem-poster-A0.pdf'), width: '841mm', height: '1189mm', printBackground: true });
await page.screenshot({ path: path.join(dir, 'emem-poster-preview.png'), scale: 'css' });
await browser.close();
