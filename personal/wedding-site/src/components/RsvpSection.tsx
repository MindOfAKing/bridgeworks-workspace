'use client';

import { useState, type FormEvent } from 'react';
import { wedding } from '@/data/wedding';
import { Pending } from './Pending';

type Status = 'idle' | 'sending' | 'sent' | 'error';

export function RsvpSection({ closed }: { closed: boolean }) {
  const [attending, setAttending] = useState<boolean | null>(null);
  const [status, setStatus] = useState<Status>('idle');
  const [error, setError] = useState('');

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (attending === null) {
      setError('Please choose whether you can make it.');
      setStatus('error');
      return;
    }

    const form = new FormData(event.currentTarget);
    setStatus('sending');
    setError('');

    try {
      const res = await fetch('/api/rsvp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          guestName: form.get('guestName'),
          email: form.get('email'),
          attending,
          partySize: Number(form.get('partySize') || 1),
          partyNames: form.get('partyNames'),
          atCeremony: form.get('atCeremony') === 'on',
          atReception: form.get('atReception') === 'on',
          dietary: form.get('dietary'),
          message: form.get('message'),
        }),
      });

      const data = (await res.json().catch(() => null)) as { error?: string } | null;

      if (!res.ok) {
        setError(data?.error || 'Something went wrong. Please try again.');
        setStatus('error');
        return;
      }

      setStatus('sent');
    } catch {
      setError('We could not reach the server. Please check your connection and try again.');
      setStatus('error');
    }
  }

  return (
    <section id="rsvp" className="scroll-mt-20 bg-cream-deep">
      <div className="section">
        <p className="eyebrow">Reply</p>
        <h2 className="section-title">RSVP</h2>
        <div className="rule" />

        <p className="prose-body mt-8">
          <Pending>{wedding.rsvp.intro}</Pending>
        </p>
        <p className="mt-3 font-body text-sm uppercase tracking-[0.18em] text-burgundy">
          Kindly reply by <Pending>{wedding.rsvp.deadlineDisplay}</Pending>
        </p>

        {closed ? (
          <div className="card mt-10">
            <p className="font-body text-base text-ink/80">
              The reply date has passed, so the form is closed. If your plans have changed, please
              message us directly.
            </p>
          </div>
        ) : status === 'sent' ? (
          <div className="card mt-10" role="status">
            <p className="font-display text-2xl text-burgundy">
              {attending ? wedding.rsvp.thanks : wedding.rsvp.thanksDecline}
            </p>
            <button
              type="button"
              onClick={() => {
                setStatus('idle');
                setAttending(null);
              }}
              className="link-quiet mt-4"
            >
              Send another reply
            </button>
          </div>
        ) : (
          <form onSubmit={onSubmit} className="card mt-10 space-y-6">
            <div>
              <label htmlFor="guestName" className="field-label">
                Your name
              </label>
              <input id="guestName" name="guestName" required maxLength={120} className="field" />
            </div>

            <div>
              <label htmlFor="email" className="field-label">
                Email (optional)
              </label>
              <input id="email" name="email" type="email" maxLength={160} className="field" />
            </div>

            <fieldset>
              <legend className="field-label">Can you join us?</legend>
              <div className="mt-3 flex flex-wrap gap-3">
                {[
                  { value: true, label: 'Joyfully accepts' },
                  { value: false, label: 'Regretfully declines' },
                ].map((choice) => (
                  <button
                    key={String(choice.value)}
                    type="button"
                    aria-pressed={attending === choice.value}
                    onClick={() => setAttending(choice.value)}
                    className={`rounded-sm border px-5 py-3 font-body text-sm transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-burgundy ${
                      attending === choice.value
                        ? 'border-burgundy bg-burgundy text-cream'
                        : 'border-sage/30 bg-cream text-ink hover:border-burgundy/50'
                    }`}
                  >
                    {choice.label}
                  </button>
                ))}
              </div>
            </fieldset>

            {attending ? (
              <>
                <div>
                  <label htmlFor="partySize" className="field-label">
                    How many of you, including yourself
                  </label>
                  <input
                    id="partySize"
                    name="partySize"
                    type="number"
                    min={1}
                    max={20}
                    defaultValue={1}
                    className="field"
                  />
                </div>

                <div>
                  <label htmlFor="partyNames" className="field-label">
                    Names of everyone coming with you
                  </label>
                  <input id="partyNames" name="partyNames" maxLength={300} className="field" />
                </div>

                <fieldset>
                  <legend className="field-label">Which parts will you be at?</legend>
                  <div className="mt-3 space-y-2">
                    <label className="flex items-center gap-3 font-body text-sm text-ink">
                      <input
                        type="checkbox"
                        name="atCeremony"
                        defaultChecked
                        className="h-4 w-4 accent-burgundy"
                      />
                      Ceremony
                    </label>
                    <label className="flex items-center gap-3 font-body text-sm text-ink">
                      <input
                        type="checkbox"
                        name="atReception"
                        defaultChecked
                        className="h-4 w-4 accent-burgundy"
                      />
                      Reception
                    </label>
                  </div>
                </fieldset>

                <div>
                  <label htmlFor="dietary" className="field-label">
                    Anything we should know about food
                  </label>
                  <input id="dietary" name="dietary" maxLength={300} className="field" />
                </div>
              </>
            ) : null}

            <div>
              <label htmlFor="message" className="field-label">
                A message for us (optional)
              </label>
              <textarea id="message" name="message" rows={4} maxLength={1000} className="field" />
            </div>

            {status === 'error' ? (
              <p role="alert" className="font-body text-sm text-burgundy">
                {error}
              </p>
            ) : null}

            <button type="submit" disabled={status === 'sending'} className="btn-primary">
              {status === 'sending' ? 'Sending' : 'Send reply'}
            </button>
          </form>
        )}
      </div>
    </section>
  );
}
