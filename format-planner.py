"""Format the already-populated BridgeWorks Content Planner sheet."""

import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = r"C:\Users\ELITEX21012G2\Downloads\singular-winter-477218-r3-7ee1994b60b7.json"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

NAVY = {"red": 15/255, "green": 26/255, "blue": 46/255}
GOLD = {"red": 184/255, "green": 134/255, "blue": 11/255}
IVORY = {"red": 245/255, "green": 240/255, "blue": 232/255}

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew/edit")

# Get sheet IDs
sheet_metadata = sh.fetch_sheet_metadata()
sheet_ids = {}
for s in sheet_metadata["sheets"]:
    title = s["properties"]["title"]
    sheet_ids[title] = s["properties"]["sheetId"]

print(f"Found tabs: {list(sheet_ids.keys())}")

def header_fmt(sid, cols):
    return [
        {"repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": cols},
            "cell": {"userEnteredFormat": {
                "backgroundColor": NAVY,
                "textFormat": {"foregroundColor": GOLD, "bold": True, "fontFamily": "Inter", "fontSize": 11},
                "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE"
            }},
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }},
        {"updateSheetProperties": {
            "properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 1}},
            "fields": "gridProperties.frozenRowCount"
        }}
    ]

def bg_fmt(sid, cols):
    return [{"repeatCell": {
        "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 0, "endColumnIndex": cols},
        "cell": {"userEnteredFormat": {"backgroundColor": IVORY}},
        "fields": "userEnteredFormat.backgroundColor"
    }}]

def col_w(sid, ci, w):
    return {"updateDimensionProperties": {
        "range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": ci, "endIndex": ci + 1},
        "properties": {"pixelSize": w}, "fields": "pixelSize"
    }}

def dropdown(sid, ci, vals):
    return {"setDataValidation": {
        "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": ci, "endColumnIndex": ci + 1},
        "rule": {"condition": {"type": "ONE_OF_LIST", "values": [{"userEnteredValue": v} for v in vals]}, "showCustomUi": True, "strict": True}
    }}

def checkbox(sid, ci):
    return {"setDataValidation": {
        "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": ci, "endColumnIndex": ci + 1},
        "rule": {"condition": {"type": "BOOLEAN"}, "showCustomUi": True}
    }}

reqs = []

# Queue
qid = sheet_ids["Queue"]
reqs += header_fmt(qid, 9)
reqs += bg_fmt(qid, 9)
for i, w in enumerate([110, 160, 140, 250, 300, 300, 200, 100, 80]):
    reqs.append(col_w(qid, i, w))
reqs.append(dropdown(qid, 1, ["Emmanuel LinkedIn", "BridgeWorks LinkedIn", "CEEFM LinkedIn", "Twitter-X", "Instagram"]))
reqs.append(dropdown(qid, 2, ["Observation", "Story", "Breakdown", "Industry Insight", "Case Study", "Company Update"]))
reqs.append(dropdown(qid, 7, ["Draft", "Review", "Approved", "Posted"]))
reqs.append(checkbox(qid, 8))

# Ideas Bank
iid = sheet_ids["Ideas Bank"]
reqs += header_fmt(iid, 5)
reqs += bg_fmt(iid, 5)
for i, w in enumerate([120, 300, 200, 100, 80]):
    reqs.append(col_w(iid, i, w))
reqs.append(dropdown(iid, 3, ["High", "Medium", "Low"]))
reqs.append(checkbox(iid, 4))

# CEEFM April
cid = sheet_ids["CEEFM April"]
reqs += header_fmt(cid, 8)
reqs += bg_fmt(cid, 8)
for i, w in enumerate([80, 110, 280, 350, 350, 280, 120, 80]):
    reqs.append(col_w(cid, i, w))
reqs.append(checkbox(cid, 7))
reqs.append({"repeatCell": {
    "range": {"sheetId": cid, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 6},
    "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP"}},
    "fields": "userEnteredFormat.wrapStrategy"
}})

# Analytics
aid = sheet_ids["Analytics"]
reqs += header_fmt(aid, 8)
reqs += bg_fmt(aid, 8)
for i, w in enumerate([110, 160, 250, 110, 100, 100, 100, 200]):
    reqs.append(col_w(aid, i, w))
reqs.append(dropdown(aid, 1, ["Emmanuel LinkedIn", "BridgeWorks LinkedIn", "CEEFM LinkedIn", "Twitter-X", "Instagram"]))

# Clients
clid = sheet_ids["Clients"]
reqs += header_fmt(clid, 7)
reqs += bg_fmt(clid, 7)
for i, w in enumerate([150, 120, 100, 120, 120, 130, 250]):
    reqs.append(col_w(clid, i, w))

sh.batch_update({"requests": reqs})

# Save URL
url = sh.url
with open(r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\content-planner-url.txt", "w") as f:
    f.write(url)

print(f"\nFormatting complete!")
print(f"URL: {url}")
print(f"URL saved to content-planner-url.txt")
