const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const outDir = path.join(process.cwd(), '.hermes', 'qa', 'pricing-rating-aesthetic-review');
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Users/User/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  const errors = [];
  page.on('console', (msg) => { if (msg.type() === 'error') errors.push(msg.text()); });

  await page.goto(process.env.OLIVIKS_QA_URL || 'http://127.0.0.1:3003/', { waitUntil: 'networkidle' });
  await page.getByText('4.8 out of 5').waitFor();
  await page.getByText('491 Google reviews').first().waitFor();
  await page.getByText('Rákóczi tér 9, Budapest').waitFor();
  await page.screenshot({ path: path.join(outDir, 'home-reference-inspired.png'), fullPage: false });

  await page.goto((process.env.OLIVIKS_QA_URL || 'http://127.0.0.1:3003') + '/menu', { waitUntil: 'networkidle' });
  await page.getByRole('heading', { name: 'Fried rice with protein' }).scrollIntoViewIfNeeded();
  const fried = page.locator('article').filter({ has: page.getByRole('heading', { name: 'Fried rice with protein' }) }).first();
  await fried.locator('select').first().selectOption('Chicken');
  await fried.locator('input[type="checkbox"]').check();
  await fried.getByRole('button', { name: /Add customized order/i }).click();
  const cart = page.getByRole('dialog', { name: /Your order/i });
  await cart.getByText('Known subtotal: 4,000 Ft').waitFor();
  const href = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  if (!href) throw new Error('WhatsApp link missing');
  const decoded = decodeURIComponent(href);
  for (const expected of ['Fried rice with protein', 'Protein: Chicken', 'Extra hot pepper stew?: Yes', 'Provisional known subtotal: 4,000 Ft']) {
    if (!decoded.includes(expected)) throw new Error(`Missing WhatsApp text: ${expected}`);
  }

  if (errors.length) throw new Error(`Console errors found: ${errors.join('\n')}`);
  await browser.close();
  console.log('Pricing/rating/aesthetic browser QA passed');
})();
