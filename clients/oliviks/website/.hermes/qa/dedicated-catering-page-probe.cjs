const fs = require('fs');
const path = require('path');

const root = process.cwd();
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const assert = (condition, message) => {
  if (!condition) throw new Error(message);
};

const cateringPagePath = path.join(root, 'src/app/catering/page.tsx');
assert(fs.existsSync(cateringPagePath), 'Expected dedicated /catering page at src/app/catering/page.tsx');

const cateringPage = read('src/app/catering/page.tsx');
assert(/export const metadata/.test(cateringPage), 'Catering page should define metadata');
assert(/Nigerian catering in Budapest/.test(cateringPage), 'Catering page should have a strong SEO/title phrase');
assert(/Catering for Nigerian celebrations/.test(cateringPage), 'Catering page should carry the approved hero message');
assert(/Birthdays/.test(cateringPage) && /Weddings/.test(cateringPage) && /Baby showers/.test(cateringPage), 'Catering page should list event types');
assert(/headcount/.test(cateringPage) && /date/.test(cateringPage) && /dishes/.test(cateringPage), 'Catering page should tell customers what details to send');
assert(/Book Catering/.test(cateringPage), 'Catering page should include a Book Catering CTA');
assert(/images\/legacy\//.test(cateringPage), 'Catering page should use legacy food/kitchen imagery');
assert(/ContactForm/.test(cateringPage) || /waLink\(/.test(cateringPage), 'Catering page should provide a concrete enquiry path');

const header = read('src/components/Header.tsx');
assert(/href: '\/catering', label: 'Catering'/.test(header), 'Header Catering nav should link to /catering');

const home = read('src/app/page.tsx');
assert(/href="\/catering"/.test(home), 'Homepage catering CTA should link to /catering');

const contact = read('src/app/contact/page.tsx');
assert(/href="\/catering"/.test(contact), 'Contact catering area should link to /catering');

console.log('Dedicated catering page probe passed');
