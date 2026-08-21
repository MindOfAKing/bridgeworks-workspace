// One-time setup for the guest photo drop.
//
//   node scripts/google-drive-setup.mjs --client-id XXX --client-secret YYY
//
// Opens a local callback server, walks you through the Google consent screen,
// exchanges the code for a refresh token, creates the Drive folder the uploads
// land in, and prints the two values to put in the environment.
//
// Scope is drive.file, which only ever touches files this app creates. It
// cannot see the rest of your Drive, and it is a non sensitive scope, so the
// OAuth app can be published without Google review. That matters: an app left
// in testing mode has its refresh token expire after seven days, which would
// break the drop mid wedding.

import { createServer } from 'node:http';
import { randomBytes } from 'node:crypto';

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

const clientId = arg('client-id') || process.env.GOOGLE_CLIENT_ID;
const clientSecret = arg('client-secret') || process.env.GOOGLE_CLIENT_SECRET;
const port = Number(arg('port') || 5411);
const folderName = arg('folder') || 'Wedding photos from guests';
const redirectUri = `http://localhost:${port}/callback`;

if (!clientId || !clientSecret) {
  console.error('Need --client-id and --client-secret from your Google Cloud OAuth client.');
  process.exit(1);
}

const state = randomBytes(16).toString('hex');
const authUrl = new URL('https://accounts.google.com/o/oauth2/v2/auth');
authUrl.searchParams.set('client_id', clientId);
authUrl.searchParams.set('redirect_uri', redirectUri);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', 'https://www.googleapis.com/auth/drive.file');
authUrl.searchParams.set('access_type', 'offline');
authUrl.searchParams.set('prompt', 'consent');
authUrl.searchParams.set('state', state);

console.log('\nOpen this in the browser you are signed into as the couple:\n');
console.log(authUrl.toString());
console.log('\nWaiting for the redirect back...\n');

const code = await new Promise((resolve, reject) => {
  const server = createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${port}`);
    if (url.pathname !== '/callback') {
      res.writeHead(404).end();
      return;
    }
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<p style="font:16px system-ui">Done. You can close this tab and go back to the terminal.</p>');
    server.close();
    if (url.searchParams.get('state') !== state) return reject(new Error('State mismatch'));
    const returned = url.searchParams.get('code');
    if (returned) {
      resolve(returned);
    } else {
      reject(new Error(url.searchParams.get('error') || 'No code'));
    }
  });
  server.listen(port);
});

const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    code,
    client_id: clientId,
    client_secret: clientSecret,
    redirect_uri: redirectUri,
    grant_type: 'authorization_code',
  }),
});

if (!tokenRes.ok) {
  console.error('Token exchange failed:', tokenRes.status, await tokenRes.text());
  process.exit(1);
}

const { refresh_token: refreshToken, access_token: accessToken } = await tokenRes.json();

if (!refreshToken) {
  console.error('Google did not return a refresh token. Re-run it, the consent screen must be accepted fresh.');
  process.exit(1);
}

const folderRes = await fetch('https://www.googleapis.com/drive/v3/files?fields=id,name', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ name: folderName, mimeType: 'application/vnd.google-apps.folder' }),
});

if (!folderRes.ok) {
  console.error('Could not create the folder:', folderRes.status, await folderRes.text());
  process.exit(1);
}

const folder = await folderRes.json();

console.log('Folder created in your Drive:', folder.name);
console.log('\nPut these in .env.local and in the Vercel project settings:\n');
console.log(`GOOGLE_CLIENT_ID=${clientId}`);
console.log(`GOOGLE_CLIENT_SECRET=${clientSecret}`);
console.log(`GOOGLE_REFRESH_TOKEN=${refreshToken}`);
console.log(`DRIVE_UPLOAD_FOLDER_ID=${folder.id}`);
console.log('');
