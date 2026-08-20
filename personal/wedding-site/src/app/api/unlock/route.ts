import { NextResponse } from 'next/server';
import { ACCESS_COOKIE, ACCESS_COOKIE_MAX_AGE, accessToken, safeEqual } from '@/lib/auth';

// A fixed pause on every attempt. Per IP counters are unreliable on serverless,
// so the real defence is a strong passphrase. This only slows a script down.
const ATTEMPT_DELAY_MS = 600;

export async function POST(request: Request) {
  const body = (await request.json().catch(() => null)) as { password?: string } | null;
  const supplied = (body?.password ?? '').trim();

  const password = process.env.SITE_PASSWORD;
  const token = await accessToken();

  if (!password || !token) {
    return NextResponse.json(
      { error: 'The passphrase is not set up yet. Add SITE_PASSWORD and SESSION_SECRET.' },
      { status: 503 },
    );
  }

  await new Promise((resolve) => setTimeout(resolve, ATTEMPT_DELAY_MS));

  if (!supplied || !safeEqual(supplied, password)) {
    return NextResponse.json({ error: 'That is not the word on the invitation.' }, { status: 401 });
  }

  const response = NextResponse.json({ ok: true });
  response.cookies.set(ACCESS_COOKIE, token, {
    httpOnly: true,
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
    path: '/',
    maxAge: ACCESS_COOKIE_MAX_AGE,
  });
  return response;
}
