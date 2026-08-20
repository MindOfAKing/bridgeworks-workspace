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
      <label htmlFor="password" className="field-label text-center">
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
        className="field text-center tracking-[0.2em]"
      />

      {error ? (
        <p role="alert" className="mt-4 font-body text-sm text-burgundy">
          {error}
        </p>
      ) : null}

      <button type="submit" disabled={busy} className="btn-primary mt-6 w-full">
        {busy ? 'Checking' : 'Enter'}
      </button>
    </form>
  );
}
