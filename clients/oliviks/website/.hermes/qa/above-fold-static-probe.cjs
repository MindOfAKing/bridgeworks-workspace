const fs = require('fs');
const path = require('path');

const root = process.cwd();
const home = fs.readFileSync(path.join(root, 'src/app/page.tsx'), 'utf8');
const about = fs.readFileSync(path.join(root, 'src/app/about/page.tsx'), 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(`Above-fold static probe failed: ${message}`);
    process.exit(1);
  }
}

const homeHero = home.slice(home.indexOf('<section className="relative overflow-hidden'), home.indexOf('<section className="border-y'));
const aboutHero = about.slice(about.indexOf('<section className="container-x py-16">'), about.indexOf('<section className="border-y'));

assert(homeHero.includes('Real Nigerian Food.'), 'homepage hero text must remain in the first section');
assert(homeHero.includes('/images/legacy/jollof-rice.png'), 'homepage hero image must remain in the first section');
assert(!homeHero.includes('<Reveal'), 'homepage above-the-fold hero must not depend on Reveal/whileInView');

assert(aboutHero.includes('How Oliviks Started'), 'about story heading must remain in the first section');
assert(aboutHero.includes('/images/legacy/chef-prep.jpg'), 'about story image must remain in the first section');
assert(!aboutHero.includes('<Reveal'), 'about above-the-fold story must not depend on Reveal/whileInView');

console.log('Above-fold static probe passed');
