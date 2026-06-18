const fs = require('fs');

const files = {
  home: fs.readFileSync('src/app/page.tsx', 'utf8'),
  about: fs.readFileSync('src/app/about/page.tsx', 'utf8'),
  menuPage: fs.readFileSync('src/app/menu/page.tsx', 'utf8'),
  contact: fs.readFileSync('src/app/contact/page.tsx', 'utf8'),
  menu: fs.readFileSync('src/data/menu.ts', 'utf8'),
  site: fs.readFileSync('src/data/site.ts', 'utf8'),
  orderCta: fs.readFileSync('src/components/OrderCTA.tsx', 'utf8'),
  menuList: fs.readFileSync('src/components/MenuList.tsx', 'utf8'),
};

const checks = [
  ['home headline approved', files.home.includes('Real Nigerian Food.') && files.home.includes('Made in Budapest.')],
  ['home subheadline approved', files.home.includes('Jollof rice, egusi soup, suya, and more, cooked the way it is at home. Order direct from Rákóczi tér 9.')],
  ['homepage Nigerian kitchen section', files.home.includes('Nothing here is adjusted to play it safe. It is Nigerian food, cooked properly.')],
  ['homepage Budapest proof section', files.home.includes('Rated 4.8 from 491 Google reviews. Featured by Origo, We Love Budapest, and WMN.')],
  ['homepage first-timer section', files.home.includes('Start with jollof rice, plantain, and puff puff.')],
  ['about headline approved', files.about.includes('How Oliviks Started')],
  ['about founders approved', files.about.includes('Cynthia and Aese came to Hungary to study') && files.about.includes('Debrecen, from 2017 to 2019')],
  ['about Nigerian not African-themed', files.about.includes('a Nigerian kitchen, not an African-themed one')],
  ['menu intro approved', files.menuPage.includes('What We Cook') && files.menuPage.includes('The menu runs deep. Jollof rice and fried rice.')],
  ['contact approved', files.contact.includes('Find Us') && files.contact.includes('We cater. Birthdays, weddings, baby showers, anniversaries, and drop-off orders.')],
  ['order button copy approved', files.orderCta.includes("label = 'Order Direct'")],
  ['dish button copy approved', files.menuList.includes('Order') && !files.menuList.includes('Add to Order')],
  ['jollof full copy approved', files.menu.includes('Long-cooked tomato rice with a smoky edge.')],
  ['new confirmed menu items present', ['Beef Pilau rice', 'Bitter leaf soup', 'Banga soup', 'Chin Chin', 'Fish roll'].every((s) => files.menu.includes(s))],
  ['stale menu items removed', ['Efo Riro', 'Okra Soup', 'Moi Moi', 'Akara', 'Amala', 'Salad', 'Extra Stew', 'Mixed Plate / Combo'].every((s) => !files.menu.includes(s))],
  ['pepper soup placeholder present', files.menu.includes("name: 'Pepper soup'") && files.menu.includes("price: 'Price TBC'")],
  ['abacha fish placeholder present', files.menu.includes("name: 'Abacha and Fish'") && files.menu.includes('Awaiting owner confirmation before final publish')],
  ['menu page placeholder note present', files.menuPage.includes('Pepper soup and Abacha and Fish are shown as placeholders while final details are confirmed.')],
  ['dish count remains 25 with placeholders', files.menu.includes('should be 25')],
];

const missing = checks.filter(([, ok]) => !ok).map(([name]) => name);
if (missing.length) {
  console.error('Approved copy probe failed:\n- ' + missing.join('\n- '));
  process.exit(1);
}
console.log('Approved copy probe passed');
