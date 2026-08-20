// Turns a running preview of the site into one self contained HTML file.
//
//   NEXT_PUBLIC_PREVIEW_SAMPLE=1 SITE_PASSWORD=... SESSION_SECRET=... npm run build && npx next start -p 3112
//   node scripts/make-preview.mjs --base http://127.0.0.1:3112 --password ...
//
// The output is body content only, with the stylesheet inlined, the photos
// inlined as data URIs, and the fonts pulled from Google Fonts instead of the
// self hosted copies. No scripts survive, so the page is a look at the design
// rather than a working site.

import { readFile, readdir, writeFile, mkdir } from 'node:fs/promises';
import { join, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

function arg(name, fallback) {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? fallback : process.argv[index + 1];
}

const base = arg('base', 'http://127.0.0.1:3112');
const password = arg('password', process.env.SITE_PASSWORD);
const out = join(root, arg('out', 'preview/index.html'));

if (!password) {
  console.error('Need the site passphrase: --password <word> or SITE_PASSWORD in the environment.');
  process.exit(1);
}

// 1. Unlock, then pull the rendered page.
const unlock = await fetch(`${base}/api/unlock`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ password }),
});
if (!unlock.ok) {
  console.error(`Unlock failed with ${unlock.status}. Is the passphrase right?`);
  process.exit(1);
}
const cookie = (unlock.headers.get('set-cookie') || '').split(';')[0];

const pageRes = await fetch(base, { headers: { cookie } });
if (!pageRes.ok) {
  console.error(`Could not fetch the page: ${pageRes.status}`);
  process.exit(1);
}
let html = await pageRes.text();

// 2. Keep the body content only. The artifact host supplies the document shell.
const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
if (!bodyMatch) {
  console.error('No body found in the rendered page.');
  process.exit(1);
}
let content = bodyMatch[1];

// 3. Drop every script, including the hydration payload.
content = content.replace(/<script[\s\S]*?<\/script>/gi, '');
content = content.replace(/<template[\s\S]*?<\/template>/gi, '');

// 4. Inline the compiled stylesheet, fonts and all, so the page needs nothing
// from the network.
const cssDir = join(root, '.next/static/css');
const cssFiles = (await readdir(cssDir)).filter((file) => file.endsWith('.css'));
let css = '';
for (const file of cssFiles) css += await readFile(join(cssDir, file), 'utf8');

const fontUrls = [...new Set([...css.matchAll(/\/_next\/static\/media\/([\w.-]+\.woff2?)/g)].map((m) => m[1]))];
for (const file of fontUrls) {
  const bytes = await readFile(join(root, '.next/static/media', file));
  const type = file.endsWith('.woff2') ? 'font/woff2' : 'font/woff';
  css = css.split(`/_next/static/media/${file}`).join(`data:${type};base64,${bytes.toString('base64')}`);
}

// The font variables normally live on <html>, which the artifact host owns.
// Lift whatever the build assigned them onto :root instead.
const displayFont = (css.match(/--font-display:\s*([^;}]+)/) || [, "Georgia, serif"])[1];
const bodyFont = (css.match(/--font-body:\s*([^;}]+)/) || [, "system-ui, sans-serif"])[1];

// 5. Inline the photos as data URIs so nothing is fetched from a server.
const photoDir = join(root, 'public/photos');
const photos = (await readdir(photoDir)).filter((file) => /\.(jpe?g|png|webp)$/i.test(file));
const mime = { '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp' };
for (const file of photos) {
  const bytes = await readFile(join(photoDir, file));
  const uri = `data:${mime[extname(file).toLowerCase()]};base64,${bytes.toString('base64')}`;
  content = content.split(`/photos/${file}`).join(uri);
}

// 6. Load every photo straight away. Lazy loading is right on the real site,
// but a snapshot gets screenshotted and scrolled through, so blank tiles read
// as broken.
content = content.replace(/loading="lazy"/g, 'loading="eager"');

// 7. A note under the form, so nobody waits for a reply that cannot arrive.
content = content.replace(
  /(<button[^>]*type="submit"[\s\S]*?<\/button>)/,
  `$1<p class="mt-4 font-body text-sm leading-relaxed text-muted">Preview only, so this form does not send. On the live site, choosing "Joyfully accepts" opens fields for how many are coming, their names, which parts of the day they will be at, and anything we should know about food.</p>`,
);

const title = (html.match(/<title[^>]*>([^<]*)<\/title>/i) || [, 'Wedding preview'])[1]
  .replace(' | Wedding', '');

const page = `<title>${title}</title>
<style>
${css}
:root {
  --font-display: ${displayFont};
  --font-body: ${bodyFont};
}
body { background-color: #F7F4EF; color: #2A2422; }
input, textarea, button { pointer-events: none; }
</style>
${content}
`;

await mkdir(dirname(out), { recursive: true });
await writeFile(out, page);
console.log(`Wrote ${out} (${(Buffer.byteLength(page) / 1024 / 1024).toFixed(2)} MB)`);
