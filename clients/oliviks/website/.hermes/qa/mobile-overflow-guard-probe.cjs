const fs = require('fs');
const path = require('path');

const css = fs.readFileSync(path.join(process.cwd(), 'src/app/globals.css'), 'utf8');

function assert(condition, message) {
  if (!condition) {
    console.error(`Mobile overflow guard probe failed: ${message}`);
    process.exit(1);
  }
}

assert(/html\s*{[^}]*overflow-x:\s*hidden;/s.test(css), 'html must hide horizontal overflow');
assert(/body\s*{[^}]*overflow-x:\s*hidden;/s.test(css), 'body must hide horizontal overflow');
assert(/body\s*{[^}]*max-width:\s*100vw;/s.test(css), 'body must be capped to viewport width');
assert(/\.container-x\s*{[^}]*box-sizing:\s*border-box;/s.test(css), 'container-x must use border-box sizing');
assert(/\.container-x\s*{[^}]*max-width:\s*min\(72rem,\s*100vw\);/s.test(css), 'container-x must not exceed viewport width');

console.log('Mobile overflow guard probe passed');
