'use client';

import { useState } from 'react';
import { waLink } from '@/data/site';

type Status = 'idle' | 'sending' | 'ok' | 'error';

export function ContactForm() {
  const [status, setStatus] = useState<Status>('idle');
  const [error, setError] = useState('');

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus('sending');
    setError('');

    const form = e.currentTarget;
    const data = {
      name: (form.elements.namedItem('name') as HTMLInputElement).value,
      email: (form.elements.namedItem('email') as HTMLInputElement).value,
      message: (form.elements.namedItem('message') as HTMLTextAreaElement).value,
    };

    try {
      const res = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
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
      <div className="rounded-2xl border border-leaf/30 bg-leaf/10 p-6 text-center">
        <p className="font-display text-xl font-semibold text-leaf">Thank you</p>
        <p className="mt-2 text-cocoa/70">Your message has been sent. We will get back to you soon.</p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      <div>
        <label htmlFor="name" className="mb-1 block text-sm font-medium text-cocoa">Your name</label>
        <input
          id="name"
          name="name"
          required
          className="w-full rounded-xl border border-cocoa/15 bg-white px-4 py-3 outline-none focus:border-palm"
          placeholder="Enter your name"
        />
      </div>
      <div>
        <label htmlFor="email" className="mb-1 block text-sm font-medium text-cocoa">Email address</label>
        <input
          id="email"
          name="email"
          type="email"
          required
          className="w-full rounded-xl border border-cocoa/15 bg-white px-4 py-3 outline-none focus:border-palm"
          placeholder="you@example.com"
        />
      </div>
      <div>
        <label htmlFor="message" className="mb-1 block text-sm font-medium text-cocoa">How can we help?</label>
        <textarea
          id="message"
          name="message"
          required
          rows={4}
          className="w-full rounded-xl border border-cocoa/15 bg-white px-4 py-3 outline-none focus:border-palm"
          placeholder="Pickup order, catering, or help choosing a dish..."
        />
      </div>

      {status === 'error' && (
        <div className="rounded-xl border border-palm/30 bg-palm/5 p-3 text-sm text-palm">
          {error}{' '}
          <a href={waLink('Hi Oliviks, I have a question:')} target="_blank" rel="noopener noreferrer" className="font-semibold underline">
            Message us on WhatsApp
          </a>
        </div>
      )}

      <button type="submit" disabled={status === 'sending'} className="btn-primary w-full disabled:opacity-60">
        {status === 'sending' ? 'Sending...' : 'Send message'}
      </button>
    </form>
  );
}
