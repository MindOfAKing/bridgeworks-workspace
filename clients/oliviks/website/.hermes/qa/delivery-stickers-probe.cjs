const fs = require('fs');
const path = require('path');
const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const exists = (file) => fs.existsSync(path.join(root, file));

const site = read('src/data/site.ts');
const home = read('src/app/page.tsx');
const menu = read('src/app/menu/page.tsx');
const contact = read('src/app/contact/page.tsx');

const checks = [
  ['platform delivery enabled in config', site.includes('showPlatforms: true')],
  ['Wolt URL present', site.includes('wolt.com/en/hun/budapest/restaurant/oliviks-nigerian-kitchen')],
  ['Foodora URL present', site.includes('foodora.hu/en/restaurant/lclg/oliviks-kitchen')],
  ['DeliveryStickers component exists', exists('src/components/DeliveryStickers.tsx')],
  ['DeliveryStickers component has Wolt sticker', exists('src/components/DeliveryStickers.tsx') && read('src/components/DeliveryStickers.tsx').includes('Wolt')],
  ['DeliveryStickers component has Foodora sticker', exists('src/components/DeliveryStickers.tsx') && read('src/components/DeliveryStickers.tsx').includes('Foodora')],
  ['Homepage renders delivery stickers', home.includes('<DeliveryStickers')],
  ['Menu page renders delivery stickers', menu.includes('<DeliveryStickers')],
  ['Contact page renders delivery stickers', contact.includes('<DeliveryStickers')],
];

const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('Delivery stickers probe failed:\n- ' + failed.join('\n- '));
  process.exit(1);
}
console.log('Delivery stickers probe passed');
