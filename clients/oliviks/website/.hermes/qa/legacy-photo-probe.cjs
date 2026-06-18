const fs = require('fs');
const path = require('path');

const root = process.cwd();
const requiredAssets = [
  'public/images/legacy/jollof-rice.png',
  'public/images/legacy/fried-rice-shrimps.png',
  'public/images/legacy/afang-soup.png',
  'public/images/legacy/ogbono-soup.png',
  'public/images/legacy/assorted-pepper-soup.png',
  'public/images/legacy/native-rice.png',
  'public/images/legacy/rice-and-beans.png',
  'public/images/legacy/coconut-rice.png',
  'public/images/legacy/abacha-and-fish.png',
  'public/images/legacy/chef-prep.jpg',
];

function assert(condition, message) {
  if (!condition) {
    console.error(`Legacy photo probe failed: ${message}`);
    process.exit(1);
  }
}

for (const asset of requiredAssets) {
  assert(fs.existsSync(path.join(root, asset)), `${asset} must exist`);
}

const home = fs.readFileSync(path.join(root, 'src/app/page.tsx'), 'utf8');
const about = fs.readFileSync(path.join(root, 'src/app/about/page.tsx'), 'utf8');
const menu = fs.readFileSync(path.join(root, 'src/data/menu.ts'), 'utf8');

assert(home.includes('src="/images/legacy/jollof-rice.png"'), 'homepage hero must use the jollof legacy photo');
assert(about.includes('src="/images/legacy/chef-prep.jpg"'), 'about page must use the chef prep legacy photo');

const menuExpectations = [
  ['Jollof rice with protein', '/images/legacy/jollof-rice.png'],
  ['Fried rice with protein', '/images/legacy/fried-rice-shrimps.png'],
  ['Beef Pilau rice', '/images/legacy/native-rice.png'],
  ['Ogbono soup with one swallow', '/images/legacy/ogbono-soup.png'],
  ['Pepper soup', '/images/legacy/assorted-pepper-soup.png'],
  ['Abacha and Fish', '/images/legacy/abacha-and-fish.png'],
];

for (const [name, image] of menuExpectations) {
  assert(menu.includes(`name: '${name}'`), `menu must include ${name}`);
  const nameIndex = menu.indexOf(`name: '${name}'`);
  const afterName = menu.slice(nameIndex, nameIndex + 700);
  assert(afterName.includes(`image: '${image}'`), `${name} must use ${image}`);
}

assert(!menu.includes('image: null,\n        tags: [\'popular\']'), 'popular dishes should not all remain photo-less');

console.log('Legacy photo probe passed');
