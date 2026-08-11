/**
 * Oliviks SOP audit: submission collector.
 *
 * Standalone Apps Script web app. Receives a submission from the audit forms
 * and appends one row to the responses spreadsheet. Nothing else. No email,
 * no notification, no third party.
 *
 * The spreadsheet is created by this script on first run and its id is kept in
 * script properties, so the script always owns the file it writes to.
 *
 * Privacy rules the staff form depends on:
 *   - The Staff tab stores a DATE only, never a time. A timestamp plus a shift
 *     rota identifies a person, which would break the promise made on the form.
 *   - This spreadsheet must never be shared with the client. The staff form
 *     tells people only BridgeWorks can open it. Keep that true.
 */

var TAB_OWNERS = 'Owners';
var TAB_STAFF = 'Staff';
var PROP_KEY = 'SHEET_ID';
var BOOK_NAME = 'Oliviks SOP audit responses';

function getBook() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty(PROP_KEY);
  if (id) {
    try {
      return SpreadsheetApp.openById(id);
    } catch (err) {
      // Fall through and make a fresh one.
    }
  }
  var ss = SpreadsheetApp.create(BOOK_NAME);
  props.setProperty(PROP_KEY, ss.getId());
  return ss;
}

function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return reply(false, 'No data received.');
    }

    var data = JSON.parse(e.postData.contents);
    var isStaff = (data.formType === 'staff');
    var fields = data.fields || [];
    if (!fields.length) {
      return reply(false, 'No answers in the submission.');
    }

    var ss = getBook();
    var name = isStaff ? TAB_STAFF : TAB_OWNERS;
    var sheet = ss.getSheetByName(name) || ss.insertSheet(name);

    var tz = ss.getSpreadsheetTimeZone() || 'Europe/Budapest';
    var stamp = Utilities.formatDate(
      new Date(), tz, isStaff ? 'yyyy-MM-dd' : 'yyyy-MM-dd HH:mm'
    );

    var labels = fields.map(function (f) { return f.l; });
    var values = fields.map(function (f) { return f.v; });

    if (sheet.getLastRow() === 0) {
      var header = ['Submitted'].concat(labels);
      sheet.appendRow(header);
      sheet.getRange(1, 1, 1, header.length)
        .setFontWeight('bold')
        .setBackground('#761212')
        .setFontColor('#F7F9F4');
      sheet.setFrozenRows(1);
    }

    sheet.appendRow([stamp].concat(values));
    return reply(true, 'Saved.');

  } catch (err) {
    return reply(false, String(err));
  }
}

/**
 * Open the deployed web app URL in a browser to check it is alive.
 * Returns the spreadsheet URL, creating the spreadsheet on first call.
 */
function doGet() {
  try {
    var ss = getBook();
    return reply(true, 'Collector running. Sheet: ' + ss.getName() + ' :: ' + ss.getUrl());
  } catch (err) {
    return reply(false, String(err));
  }
}

function reply(ok, message) {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: ok, message: message }))
    .setMimeType(ContentService.MimeType.JSON);
}
