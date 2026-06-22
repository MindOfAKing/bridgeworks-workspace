const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const menu = read('src/data/menu.ts');
const context = read('src/context/OrderContext.tsx');
const menuList = read('src/components/MenuList.tsx');
const cartPanel = read('src/components/OrderCartPanel.tsx');
const orderMessage = read('src/lib/orderMessage.ts');

const requiredMenuSnippets = [
  'priceNote?: string',
  "priceNote: 'Base rice plate: 2,500 Ft.'",
  "priceNote: 'With extra hot stew: 4,000 Ft.'",
  "priceNote: 'Included with the soup.'",
];

for (const snippet of requiredMenuSnippets) {
  if (!menu.includes(snippet)) {
    throw new Error(`Missing menu price guidance snippet: ${snippet}`);
  }
}

if (!context.includes('priceNote?: string;')) {
  throw new Error('OrderItemOption must store an optional priceNote.');
}

if (!menuList.includes('priceNote: selectedOption?.priceNote') || !menuList.includes('formatOptionLabel(option)')) {
  throw new Error('MenuList must preserve option price notes and display option guidance to shoppers.');
}

if (!cartPanel.includes('option.priceNote') || !cartPanel.includes('Price guidance')) {
  throw new Error('Cart panel must display selected option price guidance.');
}

if (!orderMessage.includes('option.priceNote') || !orderMessage.includes('Price guidance:')) {
  throw new Error('WhatsApp order message must include selected option price guidance.');
}

console.log('Option price guidance probe passed');
