'use client';

import { useState, type FormEvent } from 'react';

export function UnlockForm() {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError('');

    try {
      const res = await fetch('/api/unlock', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        window.location.href = '/';
        return;
      }

      const data = (await res.json().catch(() => null)) as { error?: string } | null;
      setError(data?.error || 'That is not the word on the invitation.');
    } catch {
      setError('We could not reach the server. Please try again.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="mt-10 w-full">
      <label htmlFor="password" className="block text-center font-body text-xs uppercase tracking-[0.18em] text-cream/70">
        The word on your invitation
      </label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        autoFocus
        required
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        className="mt-3 w-full rounded-sm border border-cream/30 bg-cream/10 px-4 py-3 text-center font-body text-base tracking-[0.2em] text-cream outline-none transition-colors placeholder:text-cream/40 focus:border-cream focus:ring-2 focus:ring-cream/25"
      />

      {error ? (
        <p role="alert" className="mt-4 font-body text-sm text-cream">
          {error}
        </p>
      ) : null}

      <button type="submit" disabled={busy} className="mt-6 inline-flex w-full items-center justify-center rounded-sm bg-cream px-8 py-3 font-body text-sm uppercase tracking-[0.18em] text-burgundy-dark transition-colors hover:bg-cream-card focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-cream disabled:opacity-60">
        {busy ? 'Checking' : 'Enter'}
      </button>
    </form>
  );
}
