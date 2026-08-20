import { NextResponse } from 'next/server';
import { isSupabaseConfigured, serverSupabase } from '@/lib/supabase';
import { parseRsvp, rsvpEmailText, type RsvpInput } from '@/lib/rsvp';
import { wedding } from '@/data/wedding';

// An RSVP is written to Supabase and emailed to the family inbox. The two paths
// are independent: if one is not configured or fails, the other still counts.
// If neither works the guest is told the truth rather than shown a fake success.

async function store(value: RsvpInput): Promise<boolean> {
  const supabase = serverSupabase();
  if (!supabase) return false;

  const { error } = await supabase.from('rsvps').insert({
    guest_name: value.guestName,
    email: value.email || null,
    attending: value.attending,
    party_size: value.partySize,
    party_names: value.partyNames || null,
    at_ceremony: value.atCeremony,
    at_reception: value.atReception,
    dietary: value.dietary || null,
    message: value.message || null,
  });

  if (error) {
    console.error('RSVP store failed:', error.message);
    return false;
  }
  return true;
}

async function notify(value: RsvpInput): Promise<boolean> {
  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.RSVP_TO;
  if (!apiKey || !to) return false;

  const from = process.env.RSVP_FROM || 'Wedding Website <onboarding@resend.dev>';
  const verdict = value.attending ? 'is coming' : 'cannot come';

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
        ...(value.email ? { reply_to: value.email } : {}),
        subject: `RSVP: ${value.guestName} ${verdict}`,
        text: rsvpEmailText(value),
      }),
    });
    if (!res.ok) {
      console.error('RSVP email failed:', res.status, await res.text());
      return false;
    }
    return true;
  } catch (error) {
    console.error('RSVP email failed:', error);
    return false;
  }
}

export async function POST(request: Request) {
  const body = await request.json().catch(() => null);
  const parsed = parseRsvp(body);
  if (!parsed.ok) {
    return NextResponse.json({ error: parsed.error }, { status: 400 });
  }

  if (Date.now() > Date.parse(`${wedding.rsvp.deadlineIso}T23:59:59Z`)) {
    return NextResponse.json(
      { error: 'The reply date has passed. Please message us directly.' },
      { status: 410 },
    );
  }

  const [stored, emailed] = await Promise.all([store(parsed.value), notify(parsed.value)]);

  if (!stored && !emailed) {
    const detail = isSupabaseConfigured()
      ? 'We could not record your reply just now. Please try again shortly.'
      : 'The reply form is not connected yet. Please message us directly for now.';
    return NextResponse.json({ error: detail }, { status: 503 });
  }

  return NextResponse.json({ ok: true, stored, emailed, attending: parsed.value.attending });
}
