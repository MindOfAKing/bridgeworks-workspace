/*
CEEFM bilingual outreach send-control script

Use this only after office.ceefm@gmail.com is configured to send as office@ceefm.eu
and DNS alignment is corrected. Current DNS check found:
- ceefm.eu SPF: Hostinger only
- _dmarc.ceefm.eu: v=DMARC1; p=none
- google._domainkey.ceefm.eu: missing

Sheet requirements:
- Import the Send Control tab from CEEFM-full-outreach-packet-2026-05-15.xlsx into Google Sheets.
- Keep the tab name as "Send Control".
- Set "Send Approved" to Yes only for rows reviewed by a human.
- This script sends only rows where Automation Stage is "Auto-email eligible".
*/

const SHEET_NAME = "Send Control";
const DAILY_LIMIT = 20;

function sendApprovedCeefmOutreach() {
  const sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  if (!sheet) throw new Error(`Missing sheet: ${SHEET_NAME}`);

  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return;

  const headers = values[0].map(String);
  const idx = Object.fromEntries(headers.map((header, index) => [header, index]));
  const required = [
    "Email",
    "Send Approved",
    "Automation Stage",
    "Subject EN",
    "Subject HU",
    "First Message",
    "Sent At",
    "Thread ID",
    "Follow-up Due",
    "Reply Status",
  ];

  for (const header of required) {
    if (!(header in idx)) throw new Error(`Missing required column: ${header}`);
  }

  let sent = 0;
  for (let rowNumber = 2; rowNumber <= values.length && sent < DAILY_LIMIT; rowNumber++) {
    const row = values[rowNumber - 1];
    const approved = String(row[idx["Send Approved"]]).trim().toLowerCase();
    const stage = String(row[idx["Automation Stage"]]).trim();
    const alreadySent = String(row[idx["Sent At"]]).trim();
    const email = String(row[idx["Email"]]).trim();

    if (approved !== "yes") continue;
    if (stage !== "Auto-email eligible") continue;
    if (alreadySent) continue;
    if (!email || email.toLowerCase().includes("not found")) continue;

    const subject = `${row[idx["Subject EN"]]} / ${row[idx["Subject HU"]]}`;
    const body = String(row[idx["First Message"]]).trim();
    const draft = GmailApp.createDraft(email, subject, body, {
      from: "office@ceefm.eu",
      name: "CEEFM",
    });

    // Safety: create drafts first. After one clean run, replace createDraft with sendEmail.
    const threadId = draft.getMessage().getThread().getId();
    const now = new Date();
    sheet.getRange(rowNumber, idx["Sent At"] + 1).setValue(now);
    sheet.getRange(rowNumber, idx["Thread ID"] + 1).setValue(threadId);
    sheet.getRange(rowNumber, idx["Follow-up Due"] + 1).setValue(addBusinessDays(now, 3));
    sheet.getRange(rowNumber, idx["Reply Status"] + 1).setValue("Drafted");
    sent++;
  }
}

function addBusinessDays(startDate, days) {
  const result = new Date(startDate);
  let added = 0;
  while (added < days) {
    result.setDate(result.getDate() + 1);
    const day = result.getDay();
    if (day !== 0 && day !== 6) added++;
  }
  return result;
}

function markRepliesByThreadId() {
  const sheet = SpreadsheetApp.getActive().getSheetByName(SHEET_NAME);
  if (!sheet) throw new Error(`Missing sheet: ${SHEET_NAME}`);

  const values = sheet.getDataRange().getValues();
  if (values.length < 2) return;

  const headers = values[0].map(String);
  const idx = Object.fromEntries(headers.map((header, index) => [header, index]));

  for (let rowNumber = 2; rowNumber <= values.length; rowNumber++) {
    const row = values[rowNumber - 1];
    const threadId = String(row[idx["Thread ID"]]).trim();
    if (!threadId) continue;

    const thread = GmailApp.getThreadById(threadId);
    if (!thread) continue;

    const messages = thread.getMessages();
    if (messages.length > 1) {
      sheet.getRange(rowNumber, idx["Reply Status"] + 1).setValue("Replied");
    }
  }
}
