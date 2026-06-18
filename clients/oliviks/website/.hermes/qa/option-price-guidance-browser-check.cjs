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

  await page.goto(process.env.OLIVIKS_QA_URL ?? 'http://127.0.0.1:3002/menu', { waitUntil: 'networkidle' });
  await page.getByRole('heading', { name: 'Jollof rice with protein' }).scrollIntoViewIfNeeded();
  const card = page.locator('article').filter({ has: page.getByRole('heading', { name: 'Jollof rice with protein' }) }).first();

  await card.getByLabel('Protein').selectOption('Turkey');
  await card.getByLabel('Extra hot pepper stew?').check();
  await card.getByRole('button', { name: /Add customized order/i }).click();

  const cart = page.getByRole('dialog', { name: /Your order/i });
  const expectedNotes = [
    'Price guidance: Legacy checkout evidence: Turkey Jollof without extra hot stew was 2,500 Ft.',
    'Price guidance: Legacy checkout evidence: Turkey Jollof with extra hot stew was 4,000 Ft.',
  ];

  for (const expected of expectedNotes) {
    await cart.getByText(expected).waitFor();
  }

  const whatsappHref = await cart.getByRole('link', { name: /Send order on WhatsApp/i }).getAttribute('href');
  if (!whatsappHref) throw new Error('WhatsApp link missing');
  const decoded = decodeURIComponent(whatsappHref);
  for (const expected of expectedNotes) {
    if (!decoded.includes(expected)) throw new Error(`WhatsApp message missing ${expected}`);
  }

  if (consoleErrors.length) {
    throw new Error(`Console errors found: ${consoleErrors.join('\n')}`);
  }

  await browser.close();
  console.log('Option price guidance browser QA passed');
})();
