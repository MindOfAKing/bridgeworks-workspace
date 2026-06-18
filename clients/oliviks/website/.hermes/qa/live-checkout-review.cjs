const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const outDir = path.join(process.cwd(), '.hermes', 'qa', 'live-checkout-review');
fs.mkdirSync(outDir, { recursive: true });

async function getCartMessage(cart) {
  const href = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  if (!href) throw new Error('WhatsApp link missing');
  return decodeURIComponent(href);
}

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Users/User/AppData/Local/ms-playwright/chromium-1228/chrome-win64/chrome.exe',
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const consoleErrors = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });

  await page.goto('https://oliviks-kitchen.vercel.app/menu', { waitUntil: 'networkidle' });

  // Scenario 1: known legacy price path, Turkey Jollof + extra hot stew.
  await page.getByRole('heading', { name: 'Jollof rice with protein' }).scrollIntoViewIfNeeded();
  const jollof = page.locator('article').filter({ has: page.getByRole('heading', { name: 'Jollof rice with protein' }) }).first();
  await jollof.getByLabel('Protein').selectOption('Turkey');
  await jollof.getByLabel('Extra hot pepper stew?').check();
  await jollof.getByRole('button', { name: /Add customized order/i }).click();
  let cart = page.getByRole('dialog', { name: /Your order/i });
  await cart.getByText(/Protein:\s*Turkey/).waitFor();
  await cart.getByText(/Extra hot pepper stew\?:\s*Yes/).waitFor();
  await cart.getByText('Provisional subtotal').waitFor();
  await cart.getByText('Known subtotal: 4,000 Ft').waitFor();
  const turkeyMessage = await getCartMessage(cart);
  for (const expected of [
    'Protein: Turkey',
    'Extra hot pepper stew?: Yes',
    'Provisional known subtotal: 4,000 Ft',
  ]) {
    if (!turkeyMessage.includes(expected)) throw new Error(`Turkey scenario missing ${expected}`);
  }
  await page.screenshot({ path: path.join(outDir, 'turkey-jollof-known-price.png'), fullPage: false });
  await cart.getByRole('button', { name: /Clear order/i }).click();
  await cart.getByRole('button', { name: /Close cart/i }).click();

  // Scenario 2: placeholder path, Chicken Jollof without confirmed price.
  await jollof.getByLabel('Protein').selectOption('Chicken');
  await jollof.getByRole('button', { name: /Add customized order/i }).click();
  cart = page.getByRole('dialog', { name: /Your order/i });
  await cart.getByText(/Protein:\s*Chicken/).waitFor();
  await cart.getByText('Price TBC', { exact: true }).waitFor();
  await cart.getByText('Known subtotal: Price TBC').waitFor();
  const chickenMessage = await getCartMessage(cart);
  for (const expected of [
    'Protein: Chicken',
    'Price guidance: Price TBC — owner confirmation needed.',
    'Provisional known subtotal: Price TBC',
    'Some prices are TBC and will be confirmed by Oliviks.',
  ]) {
    if (!chickenMessage.includes(expected)) throw new Error(`Chicken scenario missing ${expected}`);
  }
  await page.screenshot({ path: path.join(outDir, 'chicken-jollof-tbc-price.png'), fullPage: false });

  if (consoleErrors.length) throw new Error(`Console errors found: ${consoleErrors.join('\n')}`);

  await browser.close();
  console.log(JSON.stringify({
    status: 'passed',
    screenshots: [
      path.join(outDir, 'turkey-jollof-known-price.png'),
      path.join(outDir, 'chicken-jollof-tbc-price.png'),
    ],
    turkeyMessageIncludes: ['Protein: Turkey', 'Extra hot pepper stew?: Yes', 'Provisional known subtotal: 4,000 Ft'],
    chickenMessageIncludes: ['Protein: Chicken', 'Price TBC', 'Provisional known subtotal: Price TBC'],
  }, null, 2));
})();
