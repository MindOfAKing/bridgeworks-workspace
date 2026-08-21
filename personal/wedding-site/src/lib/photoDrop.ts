import { wedding } from '@/data/wedding';

// The drop opens on the wedding morning and closes thirty days later. Both the
// section and the API check this, so a guest cannot reopen it by changing the
// clock on their phone.

const DAY = 24 * 60 * 60 * 1000;
export const OPEN_FOR_DAYS = 30;

export const MAX_FILE_BYTES = 500 * 1024 * 1024;
export const MAX_FILES_PER_BATCH = 30;

export type DropState = 'before' | 'open' | 'closed';

export function dropState(now: number = Date.now()): DropState {
  const opens = Date.parse(`${wedding.date.iso}T00:00:00Z`);
  const closes = opens + OPEN_FOR_DAYS * DAY;
  if (Number.isNaN(opens)) return 'before';
  if (now < opens) return 'before';
  if (now > closes) return 'closed';
  return 'open';
}

export function isAllowedType(mimeType: string): boolean {
  return mimeType.startsWith('image/') || mimeType.startsWith('video/');
}

// Guest names become part of the filename, so anything that would confuse a
// file listing comes out.
export function safeName(value: string): string {
  return value
    .replace(/[\\/:*?"<>|]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 60);
}

export function driveFileName(guestName: string, originalName: string): string {
  const cleanGuest = safeName(guestName) || 'Guest';
  const cleanFile = safeName(originalName) || 'photo';
  return `${cleanGuest} - ${cleanFile}`;
}
