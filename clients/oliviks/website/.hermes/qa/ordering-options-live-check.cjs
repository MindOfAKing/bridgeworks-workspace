const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const outDir = path.join(process.cwd(), '.hermes', 'qa');
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Users/User/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  await page.goto(process.env.OLIVIKS_QA_URL ?? 'http://127.0.0.1:3000/menu', { waitUntil: 'networkidle' });
  await page.getByRole('heading', { name: 'Jollof rice with protein' }).scrollIntoViewIfNeeded();
  const card = page.locator('article').filter({ has: page.getByRole('heading', { name: 'Jollof rice with protein' }) }).first();

  await card.getByLabel('Protein').selectOption('Turkey');
  await card.getByLabel('Extra hot pepper stew?').check();
  await card.getByRole('button', { name: /Add customized order/i }).click();

  const cart = page.getByRole('dialog', { name: /Your order/i });
  await cart.getByText('Protein:').waitFor();
  await cart.getByText('Turkey').waitFor();
  await cart.getByText('Extra hot pepper stew?:').waitFor();
  await cart.getByText('Yes').waitFor();

  const whatsappHref = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  if (!whatsappHref) throw new Error('WhatsApp link missing');
  const decoded = decodeURIComponent(whatsappHref);
  for (const expected of ['Jollof rice with protein', 'Protein: Turkey', 'Extra hot pepper stew?: Yes']) {
    if (!decoded.includes(expected)) throw new Error(`WhatsApp message missing ${expected}`);
  }

  await page.screenshot({ path: path.join(outDir, 'ordering-options-cart.png'), fullPage: false });

  if (consoleErrors.length) {
    throw new Error(`Console errors found: ${consoleErrors.join('\n')}`);
  }

  await browser.close();
  console.log('Ordering options browser QA passed');
})();
