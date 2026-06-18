const fs = require('fs');
const path = require('path');

const root = process.cwd();
const header = fs.readFileSync(path.join(root, 'src/components/Header.tsx'), 'utf8');
const layout = fs.readFileSync(path.join(root, 'src/app/layout.tsx'), 'utf8');
const logoPath = path.join(root, 'public/images/oliviks-logo.png');

function assert(condition, message) {
  if (!condition) {
    console.error(`Logo probe failed: ${message}`);
    process.exit(1);
  }
}

assert(fs.existsSync(logoPath), 'public/images/oliviks-logo.png must exist');
assert(header.includes("import Image from 'next/image'"), 'Header must use next/image for the logo');
assert(header.includes('src="/images/oliviks-logo.png"'), 'Header must render the Oliviks logo image');
assert(header.includes('alt="Oliviks Kitchen & Catering logo"'), 'Header logo must have accessible alt text');
assert(header.includes('Oliviks Kitchen home'), 'Header brand link must remain accessible');
assert(layout.includes('/images/oliviks-logo.png'), 'Metadata should reference the logo asset');

console.log('Logo probe passed');
