'use client';

import { useState } from 'react';
import { Check, Mail } from 'lucide-react';
import { waLink } from '@/data/site';

type Status = 'idle' | 'sending' | 'ok' | 'error';

// Retention capture form (Foundation A3). Email + optional WhatsApp, GDPR consent,
// No first-order incentive (removed at client request, 2026-07-15).
// Posts to /api/subscribe (stored in Supabase, client-owned).
export function NewsletterSignup({ source = 'website' }: { source?: string }) {
  const [status, setStatus] = useState<Status>('idle');
  const [error, setError] = useState('');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('sending');
    setError('');

    const form = e.currentTarget;
    const email = (form.elements.namedItem('email') as HTMLInputElement).value;
    const whatsapp = (form.elements.namedItem('whatsapp') as HTMLInputElement).value;
    const consent = (form.elements.namedItem('consent') as HTMLInputElement).checked;

    try {
      const res = await fetch('/api/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email,
          whatsapp,
          consent,
          source,
          incentive: null,
        }),
      });
      if (!res.ok) {
        const j = await res.json().catch(() => ({}));
        setError(j.error || 'Something went wrong. Please try WhatsApp.');
        setStatus('error');
        return;
      }
      setStatus('ok');
      form.reset();
    } catch {
      setError('Network error. Please try WhatsApp.');
      setStatus('error');
    }
  }

  if (status === 'ok') {
    return (
      <div className="flex items-center gap-3 rounded-2xl border-2 border-gold/40 bg-gold-50 px-6 py-5">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-palm text-cream">
          <Check size={18} aria-hidden="true" />
        </span>
        <div>
          <p className="font-display text-[16px] font-extrabold text-cocoa">You&apos;re on the list.</p>
          <p className="text-[13.5px] text-cocoa/65">
            Weekly specials and the occasional treat, straight to your inbox. See you soon.
          </p>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-3">
      <div className="flex flex-col gap-3 sm:flex-row">
        <div className="relative flex-1">
          <Mail
            size={17}
            className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-cocoa/40"
            aria-hidden="true"
          />
          <label htmlFor="nl-email" className="sr-only">
            Email address
          </label>
          <input
            id="nl-email"
            name="email"
            type="email"
            inputMode="email"
            placeholder="you@example.com"
            className="w-full rounded-full border-2 border-ink/10 bg-white py-3 pl-11 pr-4 text-[15px] outline-none transition-colors focus:border-palm"
          />
        </div>
        <button
          type="submit"
          disabled={status === 'sending'}
          className="btn-appetite shrink-0 text-[15px] disabled:opacity-60"
        >
          {status === 'sending' ? 'Signing up...' : 'Join the list'}
        </button>
      </div>

      <div>
        <label htmlFor="nl-whatsapp" className="sr-only">
          WhatsApp number (optional)
        </label>
        <input
          id="nl-whatsapp"
          name="whatsapp"
          type="tel"
          inputMode="tel"
          placeholder="WhatsApp number (optional, for specials)"
          className="w-full rounded-full border-2 border-ink/10 bg-white px-4 py-2.5 text-[14px] outline-none transition-colors focus:border-palm"
        />
      </div>

      <label className="flex items-start gap-2.5 text-[12.5px] leading-snug text-cocoa/60">
        <input
          name="consent"
          type="checkbox"
          required
          className="mt-0.5 h-4 w-4 shrink-0 accent-palm"
        />
        <span>
          Yes, email me Oliviks specials and offers. I can unsubscribe anytime. See how we handle your
          data in our{' '}
          <a href="/privacy" className="font-semibold text-palm underline">
            privacy policy
          </a>
          .
        </span>
      </label>

      {status === 'error' && (
        <div className="rounded-xl border border-palm/30 bg-palm-50 p-3 text-[13px] text-palm">
          {error}{' '}
          <a
            href={waLink('Hi Oliviks, I want to join your specials list:')}
            target="_blank"
            rel="noopener noreferrer"
            className="font-semibold underline"
          >
            Message us on WhatsApp
          </a>
        </div>
      )}
    </form>
  );
}
