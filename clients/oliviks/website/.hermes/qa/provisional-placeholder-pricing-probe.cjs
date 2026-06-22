const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const menu = read('src/data/menu.ts');
const pricing = fs.existsSync(path.join(root, 'src/lib/orderPricing.ts')) ? read('src/lib/orderPricing.ts') : '';
const cart = read('src/components/OrderCartPanel.tsx');
const message = read('src/lib/orderMessage.ts');
const menuList = read('src/components/MenuList.tsx');
const context = read('src/context/OrderContext.tsx');

const requiredMenu = [
  "name: 'Pepper soup'",
  "price: 'Price TBC'",
  'No product price found on oliviks.com or export scan',
  "name: 'Abacha and Fish'",
  "price: '7,500 Ft'",
  'unitPriceFt?: number',
  'unitPriceFt: 2500',
  'unitPriceFt: 4000',
];

for (const snippet of requiredMenu) {
  if (!menu.includes(snippet)) throw new Error(`Missing menu pricing placeholder snippet: ${snippet}`);
}

for (const snippet of ['unitPriceFt?: number;', 'unitPriceFt: selectedOption?.unitPriceFt']) {
  const haystack = snippet.includes('selectedOption') ? menuList : context;
  if (!haystack.includes(snippet)) throw new Error(`Missing selected option unit price propagation: ${snippet}`);
}

const requiredPricing = [
  'export function getOrderPricingSummary',
  'knownSubtotalFt',
  'hasTbcLines',
  'formatHuf',
  'Math.max',
];

for (const snippet of requiredPricing) {
  if (!pricing.includes(snippet)) throw new Error(`Missing order pricing helper snippet: ${snippet}`);
}

for (const snippet of ['Provisional subtotal', 'Known subtotal', 'Price TBC items']) {
  if (!cart.includes(snippet)) throw new Error(`Cart panel missing provisional summary text: ${snippet}`);
}

for (const snippet of ['Provisional known subtotal:', 'Some prices are TBC and will be confirmed by Oliviks.']) {
  if (!message.includes(snippet)) throw new Error(`WhatsApp message missing provisional pricing text: ${snippet}`);
}

console.log('Provisional placeholder pricing probe passed');
