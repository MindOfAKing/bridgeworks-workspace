const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');

const menu = read('src/data/menu.ts');
const home = read('src/app/page.tsx');
const contact = read('src/app/contact/page.tsx');
const catering = read('src/app/catering/page.tsx');
const header = read('src/components/Header.tsx');
const menuList = read('src/components/MenuList.tsx');

const checks = [
  ['no customer-facing legacy checkout wording in menu option notes', !/legacy checkout/i.test(menu)],
  ['no customer-facing current store variants wording in menu option notes', !/current Oliviks store variants/i.test(menu)],
  ['swallow selector uses clean included wording', menu.includes("priceNote: 'Included with the soup.'")],
  ['rice selectors use clean price wording', menu.includes("priceNote: 'Base rice plate: 2,500 Ft.'") && menu.includes("priceNote: 'With extra hot stew: 4,000 Ft.'")],
  ['menu UI still displays option notes through formatOptionLabel', menuList.includes('formatOptionLabel(option)')],
  ['header exposes Catering as a top-level nav item', header.includes("{ href: '/catering', label: 'Catering' }")],
  ['homepage has a prominent catering section', home.includes('catering-showcase') && home.includes('Catering for Nigerian celebrations')],
  ['homepage catering section links to dedicated catering page', home.includes('href="/catering"')],
  ['dedicated catering page exists with strong catering copy', catering.includes('Nigerian catering in Budapest') && catering.includes('Catering for Nigerian celebrations')],
  ['contact catering form/card has an anchor', contact.includes('id="catering"')],
  ['contact page includes prominent catering package bullets', contact.includes('Birthdays') && contact.includes('Weddings') && contact.includes('Drop-off catering')],
];

const failed = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (failed.length) {
  console.error('Catering/prominence clean-options probe failed:\n- ' + failed.join('\n- '));
  process.exit(1);
}
console.log('Catering/prominence clean-options probe passed');
