// Shared passphrase gate.
//
// The cookie never holds the passphrase. It holds a SHA-256 digest of the
// passphrase plus a server secret, so a stolen cookie does not reveal the word
// printed on the invitations. Hashing uses Web Crypto, which runs in both the
// edge middleware and the node route handlers.

export const ACCESS_COOKIE = 'wedding_access';

// Long enough to cover the run up to the wedding and the days after it.
export const ACCESS_COOKIE_MAX_AGE = 60 * 60 * 24 * 365;

export function isGateConfigured(): boolean {
  return Boolean(process.env.SITE_PASSWORD && process.env.SESSION_SECRET);
}

export async function accessToken(): Promise<string | null> {
  const password = process.env.SITE_PASSWORD;
  const secret = process.env.SESSION_SECRET;
  if (!password || !secret) return null;

  const data = new TextEncoder().encode(`${password}:${secret}`);
  const digest = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

// Constant time comparison, so a wrong cookie cannot be tuned byte by byte.
export function safeEqual(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i += 1) {
    diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return diff === 0;
}

export async function hasValidAccessCookie(cookieValue: string | undefined): Promise<boolean> {
  if (!cookieValue) return false;
  const expected = await accessToken();
  if (!expected) return false;
  return safeEqual(cookieValue, expected);
}
