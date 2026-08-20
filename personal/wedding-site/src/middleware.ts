import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { ACCESS_COOKIE, hasValidAccessCookie, isGateConfigured } from '@/lib/auth';

export async function middleware(request: NextRequest) {
  // Without a configured passphrase the site would silently be public.
  // Send everyone to the unlock screen, which explains what is missing.
  if (!isGateConfigured()) {
    if (request.nextUrl.pathname === '/unlock') return NextResponse.next();
    return NextResponse.redirect(new URL('/unlock', request.url));
  }

  const unlocked = await hasValidAccessCookie(request.cookies.get(ACCESS_COOKIE)?.value);

  if (request.nextUrl.pathname === '/unlock') {
    if (unlocked) return NextResponse.redirect(new URL('/', request.url));
    return NextResponse.next();
  }

  if (unlocked) return NextResponse.next();

  // API calls get a status, not a redirect, so the form can report honestly.
  if (request.nextUrl.pathname.startsWith('/api/')) {
    return NextResponse.json({ error: 'This link is locked.' }, { status: 401 });
  }

  return NextResponse.redirect(new URL('/unlock', request.url));
}

export const config = {
  // Everything except the unlock endpoint, Next internals and static files.
  matcher: ['/((?!api/unlock|_next/static|_next/image|favicon.ico|robots.txt).*)'],
};
