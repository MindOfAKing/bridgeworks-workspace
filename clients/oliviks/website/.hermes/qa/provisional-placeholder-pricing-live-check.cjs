const { chromium } = require('@playwright/test');

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
  await page.getByRole('heading', { name: 'Jollof rice with protein' }).scrollIntoViewIfNeeded();
  const card = page.locator('article').filter({ has: page.getByRole('heading', { name: 'Jollof rice with protein' }) }).first();
  await card.getByLabel('Protein').selectOption('Chicken');
  await card.getByRole('button', { name: /Add customized order/i }).click();

  const cart = page.getByRole('dialog', { name: /Your order/i });
  await cart.getByText('Price TBC', { exact: true }).waitFor();
  for (const expected of [
    'Provisional subtotal',
    'Known subtotal: Price TBC',
    'Price TBC items are included in the order but not counted in this known subtotal.',
  ]) {
    await cart.getByText(expected).waitFor();
  }

  const href = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  if (!href) throw new Error('WhatsApp link missing');
  const decoded = decodeURIComponent(href);
  for (const expected of [
    'Protein: Chicken',
    'Price guidance: Price TBC — owner confirmation needed.',
    'Provisional known subtotal: Price TBC',
    'Some prices are TBC and will be confirmed by Oliviks.',
  ]) {
    if (!decoded.includes(expected)) throw new Error(`WhatsApp message missing: ${expected}`);
  }

  if (consoleErrors.length) throw new Error(`Console errors found: ${consoleErrors.join('\n')}`);
  await browser.close();
  console.log('Live provisional placeholder pricing browser QA passed');
})();
