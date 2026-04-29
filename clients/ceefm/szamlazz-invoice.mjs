#!/usr/bin/env node
// Issue CEEFM invoices through the szamlazz.hu Agent API.
//
// HOW TO USE
//   1. Make sure SZAMLAZZ_API_KEY is set in C:/Users/ELITEX21012G2/Projects/.env
//   2. From this folder run:  node szamlazz-invoice.mjs
//   3. The script fetches today's MNB EUR/HUF rate, prints a preview, and asks to confirm.
//   4. On 'y' it issues the invoices and saves PDFs to ./invoices/
//
// The script issues TWO invoices: the setup fee and the April retainer.
// Edit the INVOICES array below for future months.

import { readFileSync, existsSync } from 'node:fs';
import { writeFile } from 'node:fs/promises';
import { createInterface } from 'node:readline';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// ----- Configuration -----

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const INVOICES_DIR = join(SCRIPT_DIR, 'invoices');
const ENV_PATH = 'C:/Users/ELITEX21012G2/Projects/.env';
const SZAMLAZZ_URL = 'https://www.szamlazz.hu/szamla/';
const ECB_URL = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml';

const TODAY = new Date().toISOString().slice(0, 10);
const DUE_DATE = '2026-05-01';

// Optional: paste today's MNB EUR/HUF rate here (e.g. 363.84) to override the ECB fallback.
// Source: https://www.mnb.hu/arfolyamok
// Leave as null to auto-fetch from ECB (typically within 0.1% of MNB).
const MANUAL_RATE = null;

const SELLER_BANK = ''; // leave blank to use the default bank saved in szamlazz.hu

const BUYER = {
  nev: 'CEEFM Kft',
  orszag: 'Magyarország',
  irsz: '2724',
  telepules: 'Újlengyel',
  cim: 'Petőfi Sándor utca 48',
  adoszam: '22734015-2-13',
  email: '',
};

const INVOICES = [
  {
    label: 'Setup fee',
    description_en: 'Digital foundation setup — initial onboarding',
    description_hu: 'Digitális alaprendszer kiépítése — kezdeti beállítás',
    amount_eur: 1050,
    unit: 'db',
    note_en: '16-week digital growth engagement. One-time setup fee.',
  },
  {
    label: 'April retainer (Month 1)',
    description_en: 'Monthly retainer — Digital growth services (April 2026)',
    description_hu: 'Havi átalánydíj — Digitális növekedés szolgáltatások (2026 április)',
    amount_eur: 400,
    unit: 'hó',
    note_en: '16-week digital growth engagement. Month 1 of 4 retainer (April 2026).',
  },
];

// ----- Helpers -----

function loadEnvVar(path, key) {
  const text = readFileSync(path, 'utf-8');
  const match = text.match(new RegExp(`^\\s*${key}\\s*=\\s*(.+)\\s*$`, 'm'));
  if (!match) throw new Error(`${key} not found in ${path}`);
  return match[1].replace(/^['"]|['"]$/g, '').trim();
}

async function fetchEurHufRate() {
  if (MANUAL_RATE !== null) {
    return { date: TODAY, rate: MANUAL_RATE, source: 'manual MNB override' };
  }
  const res = await fetch(ECB_URL);
  if (!res.ok) throw new Error(`ECB request failed: ${res.status}`);
  const text = await res.text();
  const dateMatch = text.match(/<Cube\s+time=['"]([^'"]+)['"]>/);
  const hufMatch = text.match(/<Cube\s+currency=['"]HUF['"]\s+rate=['"]([\d.]+)['"]\s*\/?>/);
  if (!dateMatch || !hufMatch) throw new Error('Could not parse ECB response');
  return {
    date: dateMatch[1],
    rate: parseFloat(hufMatch[1]),
    source: 'ECB',
  };
}

function eurToHuf(eur, rate) {
  return Math.round(eur * rate);
}

function formatHuf(n) {
  return n.toLocaleString('hu-HU') + ' Ft';
}

function buildInvoiceXml({ apiKey, invoice, mnb }) {
  const huf = eurToHuf(invoice.amount_eur, mnb.rate);
  const itemName =
    `${invoice.description_en} / ${invoice.description_hu}`;
  const headerComment =
    `${invoice.note_en} | Original: ${invoice.amount_eur} EUR. ` +
    `EUR/HUF rate on ${mnb.date}: 1 EUR = ${mnb.rate.toFixed(4)} HUF (source: ${mnb.source}).`;

  // Escape XML special chars in user-supplied strings
  const esc = (s) =>
    String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

  return `<?xml version="1.0" encoding="UTF-8"?>
<xmlszamla xmlns="http://www.szamlazz.hu/xmlszamla" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.szamlazz.hu/xmlszamla https://www.szamlazz.hu/szamla/docs/xsds/agent/xmlszamla.xsd">
  <beallitasok>
    <szamlaagentkulcs>${esc(apiKey)}</szamlaagentkulcs>
    <eszamla>true</eszamla>
    <szamlaLetoltes>true</szamlaLetoltes>
    <szamlaLetoltesPld>1</szamlaLetoltesPld>
    <valaszVerzio>2</valaszVerzio>
  </beallitasok>
  <fejlec>
    <keltDatum>${TODAY}</keltDatum>
    <teljesitesDatum>${TODAY}</teljesitesDatum>
    <fizetesiHataridoDatum>${DUE_DATE}</fizetesiHataridoDatum>
    <fizmod>Átutalás</fizmod>
    <penznem>HUF</penznem>
    <szamlaNyelve>en</szamlaNyelve>
    <megjegyzes>${esc(headerComment)}</megjegyzes>
  </fejlec>
  <elado>
    ${SELLER_BANK ? `<bank>${esc(SELLER_BANK)}</bank>` : ''}
  </elado>
  <vevo>
    <nev>${esc(BUYER.nev)}</nev>
    <orszag>${esc(BUYER.orszag)}</orszag>
    <irsz>${esc(BUYER.irsz)}</irsz>
    <telepules>${esc(BUYER.telepules)}</telepules>
    <cim>${esc(BUYER.cim)}</cim>
    ${BUYER.email ? `<email>${esc(BUYER.email)}</email>` : ''}
    <adoszam>${esc(BUYER.adoszam)}</adoszam>
  </vevo>
  <tetelek>
    <tetel>
      <megnevezes>${esc(itemName)}</megnevezes>
      <mennyiseg>1</mennyiseg>
      <mennyisegiEgyseg>${esc(invoice.unit)}</mennyisegiEgyseg>
      <nettoEgysegar>${huf}</nettoEgysegar>
      <afakulcs>AAM</afakulcs>
      <nettoErtek>${huf}</nettoErtek>
      <afaErtek>0</afaErtek>
      <bruttoErtek>${huf}</bruttoErtek>
    </tetel>
  </tetelek>
</xmlszamla>`;
}

async function postInvoice(xml) {
  const fd = new FormData();
  const blob = new Blob([xml], { type: 'text/xml' });
  fd.append('action-xmlagentxmlfile', blob, 'invoice.xml');

  const res = await fetch(SZAMLAZZ_URL, {
    method: 'POST',
    body: fd,
  });

  const text = await res.text();
  return parseSzamlazzResponse(text);
}

function parseSzamlazzResponse(text) {
  const successMatch = text.match(/<sikeres>(true|false)<\/sikeres>/);
  if (!successMatch) {
    return { ok: false, errorCode: 'NO_RESPONSE', errorMsg: 'Could not parse response', body: text.slice(0, 2000) };
  }
  if (successMatch[1] !== 'true') {
    const errCode = (text.match(/<hibakod>(?:<!\[CDATA\[)?([^<\]]+)/) || [])[1] || '';
    const errMsg = (text.match(/<hibauzenet>(?:<!\[CDATA\[)?([^<\]]+)/) || [])[1] || '';
    return { ok: false, errorCode: errCode, errorMsg: decodeURIComponent(errMsg), body: text.slice(0, 2000) };
  }

  const invoiceNumber = (text.match(/<szamlaszam>([^<]+)<\/szamlaszam>/) || [])[1];
  const netTotal = (text.match(/<szamlanetto>([^<]+)<\/szamlanetto>/) || [])[1];
  const grossTotal = (text.match(/<szamlabrutto>([^<]+)<\/szamlabrutto>/) || [])[1];
  const buyerAcct = (text.match(/<vevoifiokurl><!\[CDATA\[([^\]]+)\]\]><\/vevoifiokurl>/) || [])[1];

  const pdfMatch = text.match(/<pdf>([\s\S]*?)<\/pdf>/);
  let pdf = null;
  if (pdfMatch) {
    pdf = Buffer.from(pdfMatch[1].replace(/\s/g, ''), 'base64');
  }
  return { ok: true, invoiceNumber, netTotal, grossTotal, buyerAcct, pdf };
}

function ask(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise((resolve) => rl.question(question, (a) => { rl.close(); resolve(a); }));
}

// ----- Main -----

async function main() {
  if (!existsSync(ENV_PATH)) throw new Error(`.env not found at ${ENV_PATH}`);
  const apiKey = loadEnvVar(ENV_PATH, 'SZAMLAZZ_API_KEY');

  console.log('\n=== CEEFM Invoice Run ===');
  console.log(`Issue date:  ${TODAY}`);
  console.log(`Due date:    ${DUE_DATE}`);
  console.log(`Buyer:       ${BUYER.nev} (must match saved customer in szamlazz.hu)`);
  console.log(`Language:    English (item descriptions bilingual EN/HU)`);
  console.log(`VAT:         AAM (Alanyi adómentes — subjective VAT exemption)`);
  console.log(`Payment:     Bank transfer\n`);

  console.log('Fetching today\'s EUR/HUF rate...');
  const mnb = await fetchEurHufRate();
  console.log(`Rate (${mnb.date}, ${mnb.source}): 1 EUR = ${mnb.rate.toFixed(4)} HUF\n`);

  console.log('--- Invoices to issue ---');
  for (const inv of INVOICES) {
    const huf = eurToHuf(inv.amount_eur, mnb.rate);
    console.log(`\n[${inv.label}]`);
    console.log(`  Item: ${inv.description_en}`);
    console.log(`        ${inv.description_hu}`);
    console.log(`  Amount: ${inv.amount_eur} EUR  ->  ${formatHuf(huf)} (1 ${inv.unit}, AAM no VAT)`);
    console.log(`  Note: ${inv.note_en}`);
  }

  console.log('\n');
  const answer = (await ask('Issue both invoices now? [y/N] ')).trim().toLowerCase();
  if (answer !== 'y' && answer !== 'yes') {
    console.log('Cancelled. No invoices issued.');
    return;
  }

  for (const inv of INVOICES) {
    console.log(`\nIssuing: ${inv.label}...`);
    const xml = buildInvoiceXml({ apiKey, invoice: inv, mnb });
    const result = await postInvoice(xml);

    if (!result.ok) {
      console.error(`  FAILED. error_code=${result.errorCode} error=${result.errorMsg}`);
      console.error(`  body: ${result.body}`);
      console.error('  Stopping. Already-issued invoices are not rolled back.');
      process.exit(1);
    }

    const safeNum = result.invoiceNumber.replace(/[^A-Za-z0-9_-]/g, '_');
    const pdfPath = join(INVOICES_DIR, `${safeNum}_${inv.label.replace(/\s+/g, '-')}.pdf`);
    await writeFile(pdfPath, result.pdf);
    console.log(`  OK. Invoice number: ${result.invoiceNumber}`);
    console.log(`  Net: ${result.netTotal} HUF | Gross: ${result.grossTotal} HUF`);
    console.log(`  PDF saved: ${pdfPath}`);
  }

  console.log('\nAll invoices issued. PDFs are in ./invoices/.');
}

main().catch((e) => { console.error('\nERROR:', e.message); process.exit(1); });
