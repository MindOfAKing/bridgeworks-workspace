const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const outDir = path.join(process.cwd(), '.hermes/qa/menu-order-styling-live');
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  await page.goto('http://127.0.0.1:3004/menu', { waitUntil: 'networkidle' });

  await page.waitForSelector('.menu-hero-panel');
  await page.waitForSelector('.menu-card');
  await page.waitForSelector('.customize-panel');
  await page.waitForSelector('text=Order direct in under a minute');
  await page.waitForSelector('text=Customize your plate');
  await page.screenshot({ path: path.join(outDir, 'menu-styled-desktop.png'), fullPage: true });

  const firstProtein = page.locator('select').first();
  await firstProtein.selectOption({ label: 'Turkey — Base rice plate: 2,500 Ft.' }).catch(async () => {
    await firstProtein.selectOption({ index: 1 });
  });

  const extraHot = page.getByText('Extra hot pepper stew?').first();
  await extraHot.click();
  await page.getByRole('button', { name: /Add customized order/i }).first().click();
  await page.waitForSelector('[role="dialog"]');
  await page.waitForSelector('text=Kitchen receives this on WhatsApp');
  await page.waitForSelector('text=No platform checkout fee');
  await page.waitForSelector('text=Price guidance');
  await page.screenshot({ path: path.join(outDir, 'cart-styled-desktop.png'), fullPage: true });

  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto('http://127.0.0.1:3004/menu', { waitUntil: 'networkidle' });
  await page.waitForSelector('.menu-hero-panel');
  await page.waitForSelector('.menu-card');
  await page.screenshot({ path: path.join(outDir, 'menu-styled-mobile.png'), fullPage: true });

  await browser.close();
  console.log('Menu/order browser styling QA passed');
  console.log(outDir);
})().catch(async (error) => {
  console.error(error);
  process.exit(1);
});
