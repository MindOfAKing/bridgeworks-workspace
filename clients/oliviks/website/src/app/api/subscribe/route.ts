import { NextResponse } from 'next/server';
import { serverSupabase } from '@/lib/supabase/server';

// Retention capture endpoint (Foundation A3 — Email & WhatsApp Infrastructure).
// Stores subscribers in the Oliviks Supabase project. The client owns this list;
// it exports to MailerLite/Beehiiv once that account exists. GDPR: consent is
// required and enforced here AND by the row-level security policy on the table.
// Double opt-in confirmation email is sent once an email provider is connected
// (RESEND_API_KEY / MailerLite); until then rows are stored unconfirmed.

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(req: Request) {
  let body: {
    email?: string;
    whatsapp?: string;
    consent?: boolean;
    wantsWhatsapp?: boolean;
    locale?: string;
    source?: string;
    incentive?: string;
  };
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: 'Invalid request.' }, { status: 400 });
  }

  const email = (body.email ?? '').trim().toLowerCase();
  const whatsapp = (body.whatsapp ?? '').trim();
  const consent = body.consent === true;

  if (!consent) {
    return NextResponse.json({ error: 'Please tick the consent box so we can email you.' }, { status: 400 });
  }
  if (!email && !whatsapp) {
    return NextResponse.json({ error: 'Enter an email address or a WhatsApp number.' }, { status: 400 });
  }
  if (email && !EMAIL_RE.test(email)) {
    return NextResponse.json({ error: 'Please enter a valid email address.' }, { status: 400 });
  }

  const supabase = serverSupabase();
  if (!supabase) {
    return NextResponse.json(
      { error: 'Sign-ups are not set up yet. Please message us on WhatsApp.' },
      { status: 503 },
    );
  }

  const { error } = await supabase.from('subscribers').insert({
    email: email || null,
    whatsapp: whatsapp || null,
    wants_email: Boolean(email),
    wants_whatsapp: Boolean(whatsapp) || body.wantsWhatsapp === true,
    consent: true,
    locale: body.locale === 'hu' ? 'hu' : 'en',
    source: (body.source ?? 'website').slice(0, 40),
    incentive: (body.incentive ?? '').slice(0, 120) || null,
  });

  if (error) {
    // Duplicate email = already on the list. Treat as success, don't leak details.
    if (error.code === '23505') {
      return NextResponse.json({ ok: true, already: true });
    }
    return NextResponse.json({ error: 'Could not sign you up right now. Please try WhatsApp.' }, { status: 502 });
  }

  return NextResponse.json({ ok: true });
}
