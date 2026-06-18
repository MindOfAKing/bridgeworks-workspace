const { chromium } = require('@playwright/test');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto('http://localhost:3000/menu');
  await page.getByRole('button', { name: 'Add to Order' }).first().click();
  await page.getByRole('dialog', { name: 'Your order' }).getByRole('button', { name: /Increase Jollof Rice/i }).click();
  await page.screenshot({ path: '.hermes/qa/cart-viewport.png', fullPage: false });
  await browser.close();
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
