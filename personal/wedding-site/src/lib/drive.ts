// Google Drive uploads, server side.
//
// Guests never sign in and never send their files through this app. The server
// holds a refresh token for the couple's own Google account, mints a short
// lived access token, and asks Drive to open a resumable upload session. Only
// that session URL goes back to the browser, which then sends the bytes
// straight to Google.
//
// Files therefore land in the couple's Drive, owned by them, and nothing large
// passes through the site. That matters: a serverless request body is capped at
// a few megabytes, and a guest's video is not.

const TOKEN_URL = 'https://oauth2.googleapis.com/token';
const UPLOAD_URL =
  'https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true&fields=id,name';

export function isDriveConfigured(): boolean {
  return Boolean(
    process.env.GOOGLE_CLIENT_ID &&
      process.env.GOOGLE_CLIENT_SECRET &&
      process.env.GOOGLE_REFRESH_TOKEN &&
      process.env.DRIVE_UPLOAD_FOLDER_ID,
  );
}

async function accessToken(): Promise<string | null> {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;
  if (!clientId || !clientSecret || !refreshToken) return null;

  const res = await fetch(TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: clientId,
      client_secret: clientSecret,
      refresh_token: refreshToken,
      grant_type: 'refresh_token',
    }),
    cache: 'no-store',
  });

  if (!res.ok) {
    console.error('Drive token refresh failed:', res.status, await res.text());
    return null;
  }

  const data = (await res.json()) as { access_token?: string };
  return data.access_token ?? null;
}

export type UploadSession = { uploadUrl: string } | { error: string; status: number };

export async function createUploadSession({
  fileName,
  mimeType,
  size,
  description,
  origin,
}: {
  fileName: string;
  mimeType: string;
  size: number;
  description?: string;
  origin: string;
}): Promise<UploadSession> {
  const folderId = process.env.DRIVE_UPLOAD_FOLDER_ID;
  const token = await accessToken();

  if (!token || !folderId) {
    return {
      error: 'The photo drop is not connected yet. Please send your photos to us directly for now.',
      status: 503,
    };
  }

  const res = await fetch(UPLOAD_URL, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=UTF-8',
      'X-Upload-Content-Type': mimeType,
      'X-Upload-Content-Length': String(size),
      // Drive only returns a CORS enabled session URL when the origin is
      // declared here, and the browser sends the bytes cross origin.
      Origin: origin,
    },
    body: JSON.stringify({
      name: fileName,
      parents: [folderId],
      ...(description ? { description } : {}),
    }),
    cache: 'no-store',
  });

  const uploadUrl = res.headers.get('location');

  if (!res.ok || !uploadUrl) {
    console.error('Drive session failed:', res.status, await res.text());
    return { error: 'We could not start the upload. Please try again in a moment.', status: 502 };
  }

  return { uploadUrl };
}
