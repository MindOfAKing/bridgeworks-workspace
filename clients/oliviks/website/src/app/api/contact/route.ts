import { NextResponse } from 'next/server';
import { site } from '@/data/site';

// Real contact endpoint. Sends via Resend when RESEND_API_KEY is set.
// If not configured, it returns an honest 503 so the UI can fall back to WhatsApp,
// instead of faking a success like the previous build did.
//
// Required env to go live:
//   RESEND_API_KEY   - from resend.com
//   CONTACT_TO       - inbox to receive enquiries (defaults to site.email)
//   CONTACT_FROM     - verified sender, e.g. "Oliviks Website <hello@oliviks.com>"

export async function POST(req: Request) {
  let body: { name?: string; email?: string; message?: string };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Invalid request.' }, { status: 400 });
  }

  const name = (body.name ?? '').trim();
  const email = (body.email ?? '').trim();
  const message = (body.message ?? '').trim();

  if (!name || !email || !message) {
    return NextResponse.json({ error: 'Please fill in every field.' }, { status: 400 });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return NextResponse.json({ error: 'Please enter a valid email address.' }, { status: 400 });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    // Not configured yet. Be honest so the client never thinks a message was sent.
    return NextResponse.json(
      { error: 'Email is not set up yet. Please message us on WhatsApp for now.' },
      { status: 503 },
    );
  }

  const to = process.env.CONTACT_TO || site.email;
  const from = process.env.CONTACT_FROM || 'Oliviks Website <onboarding@resend.dev>';

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: [to],
        reply_to: email,
        subject: `New website enquiry from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\n\n${message}`,
      }),
    });

    if (!res.ok) {
      return NextResponse.json({ error: 'Could not send right now. Please try WhatsApp.' }, { status: 502 });
    }
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json({ error: 'Could not send right now. Please try WhatsApp.' }, { status: 502 });
  }
}
