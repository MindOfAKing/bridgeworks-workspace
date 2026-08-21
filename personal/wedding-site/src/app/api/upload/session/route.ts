import { NextResponse } from 'next/server';
import { createUploadSession, isDriveConfigured } from '@/lib/drive';
import {
  MAX_FILE_BYTES,
  driveFileName,
  dropState,
  isAllowedType,
  safeName,
} from '@/lib/photoDrop';

// Opens one resumable Drive session per file. The browser then sends the bytes
// straight to Google, so nothing large passes through this function.

export const runtime = 'nodejs';

type Body = {
  guestName?: string;
  note?: string;
  fileName?: string;
  mimeType?: string;
  size?: number;
};

export async function POST(request: Request) {
  const state = dropState();
  if (state !== 'open') {
    const error =
      state === 'before'
        ? 'The photo drop opens on the wedding day.'
        : 'The photo drop has closed. Thank you, we have them all.';
    return NextResponse.json({ error }, { status: 403 });
  }

  const body = (await request.json().catch(() => null)) as Body | null;
  const guestName = safeName(body?.guestName ?? '');
  const fileName = (body?.fileName ?? '').trim();
  const mimeType = (body?.mimeType ?? '').trim();
  const size = Number(body?.size);

  if (!guestName) {
    return NextResponse.json({ error: 'Please tell us your name first.' }, { status: 400 });
  }
  if (!fileName || !mimeType) {
    return NextResponse.json({ error: 'That file is missing its details.' }, { status: 400 });
  }
  if (!isAllowedType(mimeType)) {
    return NextResponse.json(
      { error: 'Photos and videos only, please.' },
      { status: 415 },
    );
  }
  if (!Number.isFinite(size) || size <= 0 || size > MAX_FILE_BYTES) {
    return NextResponse.json(
      { error: 'That file is too large. Anything up to 500MB is fine.' },
      { status: 413 },
    );
  }

  if (!isDriveConfigured()) {
    return NextResponse.json(
      {
        error:
          'The photo drop is not connected yet. Please hold on to your photos and we will ask again.',
      },
      { status: 503 },
    );
  }

  const note = safeName(body?.note ?? '').slice(0, 200);
  const origin = process.env.NEXT_PUBLIC_SITE_ORIGIN || new URL(request.url).origin;

  const session = await createUploadSession({
    fileName: driveFileName(guestName, fileName),
    mimeType,
    size,
    description: note ? `From ${guestName}: ${note}` : `From ${guestName}`,
    origin,
  });

  if ('error' in session) {
    return NextResponse.json({ error: session.error }, { status: session.status });
  }

  return NextResponse.json({ uploadUrl: session.uploadUrl });
}
