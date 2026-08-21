'use client';

import { useRef, useState, type FormEvent } from 'react';
import { wedding } from '@/data/wedding';
import { MAX_FILES_PER_BATCH, MAX_FILE_BYTES } from '@/lib/photoDrop';

type Item = {
  file: File;
  progress: number;
  status: 'waiting' | 'sending' | 'done' | 'failed';
  error?: string;
};

function sizeLabel(bytes: number): string {
  const mb = bytes / (1024 * 1024);
  return mb < 1 ? `${Math.max(1, Math.round(bytes / 1024))} KB` : `${mb.toFixed(1)} MB`;
}

// The bytes go straight from the phone to Google, so upload progress comes from
// XHR rather than fetch, which cannot report it.
function sendToDrive(url: string, file: File, onProgress: (percent: number) => void) {
  return new Promise<void>((resolve, reject) => {
    const request = new XMLHttpRequest();
    request.open('PUT', url, true);
    request.setRequestHeader('Content-Type', file.type || 'application/octet-stream');
    request.upload.onprogress = (event) => {
      if (event.lengthComputable) onProgress(Math.round((event.loaded / event.total) * 100));
    };
    request.onload = () =>
      request.status >= 200 && request.status < 400
        ? resolve()
        : reject(new Error(`Drive returned ${request.status}`));
    request.onerror = () => reject(new Error('The connection dropped'));
    request.send(file);
  });
}

export function PhotoDrop() {
  const [items, setItems] = useState<Item[]>([]);
  const [busy, setBusy] = useState(false);
  const [sentCount, setSentCount] = useState(0);
  const [error, setError] = useState('');
  const nameRef = useRef<HTMLInputElement>(null);
  const noteRef = useRef<HTMLInputElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  function onPick(files: FileList | null) {
    if (!files) return;
    setError('');
    const picked = Array.from(files).slice(0, MAX_FILES_PER_BATCH);
    setItems(picked.map((file) => ({ file, progress: 0, status: 'waiting' })));
  }

  function update(index: number, patch: Partial<Item>) {
    setItems((current) => current.map((item, i) => (i === index ? { ...item, ...patch } : item)));
  }

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const guestName = nameRef.current?.value.trim() ?? '';
    const note = noteRef.current?.value.trim() ?? '';

    if (!guestName) {
      setError('Please tell us your name first.');
      return;
    }
    if (items.length === 0) {
      setError('Choose some photos to send.');
      return;
    }

    setBusy(true);
    setError('');
    let sent = 0;

    for (const [index, item] of items.entries()) {
      if (item.status === 'done') continue;
      update(index, { status: 'sending', progress: 0, error: undefined });

      try {
        const res = await fetch('/api/upload/session', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            guestName,
            note,
            fileName: item.file.name,
            mimeType: item.file.type || 'application/octet-stream',
            size: item.file.size,
          }),
        });

        const data = (await res.json().catch(() => null)) as
          | { uploadUrl?: string; error?: string }
          | null;

        if (!res.ok || !data?.uploadUrl) {
          const message = data?.error || 'We could not start that upload.';
          update(index, { status: 'failed', error: message });
          setError(message);
          continue;
        }

        await sendToDrive(data.uploadUrl, item.file, (progress) => update(index, { progress }));
        update(index, { status: 'done', progress: 100 });
        sent += 1;
      } catch (uploadError) {
        update(index, {
          status: 'failed',
          error: uploadError instanceof Error ? uploadError.message : 'Something went wrong',
        });
      }
    }

    setSentCount((count) => count + sent);
    setBusy(false);
    if (sent > 0 && fileRef.current) fileRef.current.value = '';
  }

  const allDone = items.length > 0 && items.every((item) => item.status === 'done');

  return (
    <form onSubmit={onSubmit} className="card mt-10 space-y-6">
      <div>
        <label htmlFor="uploaderName" className="field-label">
          Your name
        </label>
        <input id="uploaderName" ref={nameRef} required maxLength={60} className="field" />
      </div>

      <div>
        <label htmlFor="uploaderNote" className="field-label">
          A note, if you want one (optional)
        </label>
        <input id="uploaderNote" ref={noteRef} maxLength={200} className="field" />
      </div>

      <div>
        <label htmlFor="uploaderFiles" className="field-label">
          Photos and videos
        </label>
        <input
          id="uploaderFiles"
          ref={fileRef}
          type="file"
          accept="image/*,video/*"
          multiple
          onChange={(event) => onPick(event.target.files)}
          className="field file:mr-4 file:rounded-sm file:border-0 file:bg-burgundy file:px-4 file:py-2 file:font-body file:text-xs file:uppercase file:tracking-[0.14em] file:text-cream"
        />
        <p className="mt-2 font-body text-xs text-muted">
          Up to {MAX_FILES_PER_BATCH} at a time, {Math.round(MAX_FILE_BYTES / (1024 * 1024))}MB each.
          They go straight to our Drive, so a long video is fine on a good connection.
        </p>
      </div>

      {items.length > 0 ? (
        <ul className="space-y-2">
          {items.map((item, index) => (
            <li key={`${item.file.name}-${index}`} className="font-body text-sm">
              <div className="flex items-baseline justify-between gap-3">
                <span className="truncate text-ink">{item.file.name}</span>
                <span className="shrink-0 text-xs text-muted">
                  {item.status === 'done'
                    ? 'Sent'
                    : item.status === 'failed'
                      ? 'Failed'
                      : item.status === 'sending'
                        ? `${item.progress}%`
                        : sizeLabel(item.file.size)}
                </span>
              </div>
              <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-sage/20">
                <div
                  className={`h-full transition-[width] duration-200 ${
                    item.status === 'failed' ? 'bg-burgundy-light' : 'bg-sage'
                  }`}
                  style={{ width: `${item.status === 'done' ? 100 : item.progress}%` }}
                />
              </div>
              {item.error ? <p className="mt-1 text-xs text-burgundy">{item.error}</p> : null}
            </li>
          ))}
        </ul>
      ) : null}

      {error ? (
        <p role="alert" className="font-body text-sm text-burgundy">
          {error}
        </p>
      ) : null}

      {sentCount > 0 ? (
        <p role="status" className="font-body text-sm text-sage-dark">
          {sentCount} {sentCount === 1 ? 'file is' : 'files are'} with us. {wedding.photoDrop.thanks}
        </p>
      ) : null}

      <button type="submit" disabled={busy || allDone} className="btn-primary">
        {busy ? 'Sending' : allDone ? 'All sent' : 'Send them over'}
      </button>
    </form>
  );
}
