const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const menuPage = read('src/app/menu/page.tsx');
const menuList = read('src/components/MenuList.tsx');
const cart = read('src/components/OrderCartPanel.tsx');

const checks = [
  ['menu page has a premium visual hero shell', menuPage.includes('menu-hero-panel') && menuPage.includes('Order direct in under a minute')],
  ['menu page has clear ordering helper cards', menuPage.includes('Choose your plate') && menuPage.includes('Customize options') && menuPage.includes('Send to WhatsApp')],
  ['menu filters are sticky category chips', menuList.includes('sticky top-24 z-30') && menuList.includes('Category chips')],
  ['dish cards use premium menu-card styling', menuList.includes('menu-card') && menuList.includes('group-hover:scale-105')],
  ['dish cards have an order-ready footer', menuList.includes('order-card-footer') && menuList.includes('Customize first, then send direct')],
  ['customize panel has premium option styling', menuList.includes('customize-panel') && menuList.includes('Customize your plate')],
  ['option controls have clearer selection styling', menuList.includes('option-control') && menuList.includes('accent-gold')],
  ['cart has premium drawer header summary', cart.includes('order-drawer-header') && cart.includes('Kitchen receives this on WhatsApp')],
  ['cart lines have styled selected option pills', cart.includes('selected-option-pill') && cart.includes('Price guidance')],
  ['cart footer has checkout confidence strip', cart.includes('checkout-confidence-strip') && cart.includes('No platform checkout fee')],
];

const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('Menu/order styling probe failed:\n- ' + failed.join('\n- '));
  process.exit(1);
}
console.log('Menu/order styling probe passed');
