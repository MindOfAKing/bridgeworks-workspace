export type RsvpInput = {
  guestName: string;
  email: string;
  attending: boolean;
  partySize: number;
  partyNames: string;
  atCeremony: boolean;
  atReception: boolean;
  dietary: string;
  message: string;
};

export type RsvpParseResult =
  | { ok: true; value: RsvpInput }
  | { ok: false; error: string };

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MAX_TEXT = 2000;

function str(value: unknown): string {
  return typeof value === 'string' ? value.trim().slice(0, MAX_TEXT) : '';
}

export function parseRsvp(body: unknown): RsvpParseResult {
  if (!body || typeof body !== 'object') {
    return { ok: false, error: 'Something went wrong. Please try again.' };
  }
  const raw = body as Record<string, unknown>;

  const guestName = str(raw.guestName);
  if (!guestName) return { ok: false, error: 'Please tell us your name.' };

  const email = str(raw.email);
  if (email && !EMAIL.test(email)) {
    return { ok: false, error: 'That email address does not look right.' };
  }

  if (typeof raw.attending !== 'boolean') {
    return { ok: false, error: 'Please let us know whether you can make it.' };
  }
  const attending = raw.attending;

  let partySize = Number(raw.partySize);
  if (!Number.isFinite(partySize)) partySize = 1;
  partySize = Math.min(20, Math.max(1, Math.round(partySize)));
  if (!attending) partySize = 0;

  return {
    ok: true,
    value: {
      guestName,
      email,
      attending,
      partySize,
      partyNames: attending ? str(raw.partyNames) : '',
      atCeremony: attending && raw.atCeremony === true,
      atReception: attending && raw.atReception === true,
      dietary: attending ? str(raw.dietary) : '',
      message: str(raw.message),
    },
  };
}

export function rsvpEmailText(value: RsvpInput): string {
  const lines = [
    `Name: ${value.guestName}`,
    `Attending: ${value.attending ? 'Yes' : 'No'}`,
  ];
  if (value.attending) {
    lines.push(`Party size: ${value.partySize}`);
    if (value.partyNames) lines.push(`Coming with: ${value.partyNames}`);
    lines.push(`Ceremony: ${value.atCeremony ? 'Yes' : 'No'}`);
    lines.push(`Reception: ${value.atReception ? 'Yes' : 'No'}`);
    if (value.dietary) lines.push(`Dietary notes: ${value.dietary}`);
  }
  if (value.email) lines.push(`Email: ${value.email}`);
  if (value.message) lines.push('', 'Message:', value.message);
  return lines.join('\n');
}
