const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const outDir = path.join(process.cwd(), '.hermes', 'qa');
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const results = [];

  for (const viewport of [
    { name: 'desktop', width: 1440, height: 900 },
    { name: 'mobile', width: 390, height: 844 },
  ]) {
    const page = await browser.newPage({ viewport });
    const consoleErrors = [];
    page.on('console', (msg) => {
      if (msg.type() === 'error') consoleErrors.push(msg.text());
    });
    await page.goto('https://oliviks-kitchen.vercel.app', { waitUntil: 'networkidle' });
    const header = page.locator('header');
    const logo = page.locator('img[alt="Oliviks Kitchen & Catering logo"]');
    await header.screenshot({ path: path.join(outDir, `logo-header-${viewport.name}.png`) });
    const metrics = await page.evaluate(() => {
      const header = document.querySelector('header');
      const logo = document.querySelector('img[alt="Oliviks Kitchen & Catering logo"]');
      const link = document.querySelector('a[aria-label="Oliviks Kitchen home"]');
      const headerBox = header?.getBoundingClientRect();
      const logoBox = logo?.getBoundingClientRect();
      const linkBox = link?.getBoundingClientRect();
      return {
        header: headerBox && { width: headerBox.width, height: headerBox.height },
        logo: logoBox && { width: logoBox.width, height: logoBox.height },
        link: linkBox && { width: linkBox.width, height: linkBox.height },
      };
    });
    const visible = await logo.isVisible();
    results.push({ viewport, visible, metrics, consoleErrors });
    await page.close();
  }

  await browser.close();
  fs.writeFileSync(path.join(outDir, 'logo-live-review.json'), JSON.stringify(results, null, 2));
  console.log(JSON.stringify(results, null, 2));
})();
