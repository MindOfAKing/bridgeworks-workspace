import pdf from 'pdf-parse';
import mammoth from 'mammoth';
import * as XLSX from 'xlsx';

export const config = {
  api: { bodyParser: { sizeLimit: '6mb' } },
};

function stripHtml(html) {
  return html
    .replace(/<script[\s\S]*?<\/script>/gi, '')
    .replace(/<style[\s\S]*?<\/style>/gi, '')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  const { type, data, filename, url } = req.body;

  try {
    if (type === 'url') {
      const response = await fetch(url, {
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; BridgeWorks/1.0)' },
        signal: AbortSignal.timeout(10000),
      });
      if (!response.ok) throw new Error(`Failed to fetch URL (${response.status})`);
      const html = await response.text();
      const text = stripHtml(html).slice(0, 20000);
      return res.json({ text, filename: url });
    }

    const buffer = Buffer.from(data.split(',')[1], 'base64');
    const ext = filename.split('.').pop().toLowerCase();
    let text = '';

    if (ext === 'pdf') {
      const result = await pdf(buffer);
      text = result.text;
    } else if (ext === 'docx') {
      const result = await mammoth.extractRawText({ buffer });
      text = result.value;
    } else if (ext === 'xlsx' || ext === 'xls') {
      const wb = XLSX.read(buffer, { type: 'buffer' });
      text = wb.SheetNames.map(name => {
        const ws = wb.Sheets[name];
        return `[Sheet: ${name}]\n` + XLSX.utils.sheet_to_csv(ws);
      }).join('\n\n');
    } else {
      text = buffer.toString('utf-8');
    }

    return res.json({ text: text.slice(0, 20000), filename });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
}
