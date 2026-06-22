const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const menu = read('src/data/menu.ts');
const home = read('src/app/page.tsx');
const header = read('src/components/Header.tsx');
const layout = read('src/app/layout.tsx');

const checks = [
  ['rice protein options have confirmed 2,500 Ft unit price', menu.includes('const riceProteinOptions') && (menu.match(/unitPriceFt: 2500/g) || []).length >= 4],
  ['unconfirmed protein Price TBC placeholders removed', !menu.includes("{ label: 'Chicken', priceNote: 'Price TBC") && !menu.includes("{ label: 'Fish', priceNote: 'Price TBC")],
  ['jollof and fried rice both include extra hot stew option', (menu.match(/optionGroups: \[riceProteinOptions, extraHotStewOption\]/g) || []).length >= 2],
  ['extra hot stew confirms 4,000 Ft with clean customer wording', menu.includes("unitPriceFt: 4000") && menu.includes('With extra hot stew: 4,000 Ft.')],
  ['Abacha and Fish price recovered from export order evidence', menu.includes("name: 'Abacha and Fish'") && menu.includes("price: '7,500 Ft'")],
  ['Pepper soup remains explicit no-source confirmation item', menu.includes("name: 'Pepper soup'") && menu.includes("price: 'Price TBC'") && menu.includes('No product price found on oliviks.com or export scan')],
  ['homepage has prominent rating pill with exact approved review count', home.includes('rating-pill') && home.includes('{site.reviews.rating} out of 5') && home.includes('{site.reviews.count} Google reviews')],
  ['homepage uses full-bleed hero background aesthetic', home.includes('hero-reference-shell') && home.includes('absolute inset-0') && home.includes('bg-cocoa/65')],
  ['homepage includes reference-style hero fact row', home.includes('Rákóczi tér 9, Budapest') && home.includes('Mon–Sat 11:00–20:00') && home.includes('Pickup & private delivery')],
  ['header has reference-style contact strip', header.includes('site.phone.display') && header.includes('site.email') && header.includes('Order Now')],
  ['metadata review count corrected from old 160+ to 491', !layout.includes('160+ reviews') && layout.includes('491 reviews')],
];

const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('Pricing/rating/aesthetic probe failed:\n- ' + failed.join('\n- '));
  process.exit(1);
}
console.log('Pricing/rating/aesthetic probe passed');
