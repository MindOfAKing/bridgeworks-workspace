"""
BridgeWorks Content Planner — Google Sheets API Builder
Creates the full planner with 5 tabs, formatting, dropdowns, and pre-filled data.
"""

import gspread
from google.oauth2.service_account import Credentials

SERVICE_ACCOUNT_FILE = r"C:\Users\ELITEX21012G2\Downloads\singular-winter-477218-r3-7ee1994b60b7.json"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Brand colors (hex without #)
NAVY = {"red": 15/255, "green": 26/255, "blue": 46/255}
GOLD = {"red": 184/255, "green": 134/255, "blue": 11/255}
IVORY = {"red": 245/255, "green": 240/255, "blue": 232/255}
WHITE = {"red": 1, "green": 1, "blue": 1}

# Authenticate
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

# Open existing spreadsheet shared with the service account
sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1tBstgZzoT9fR1TYA7t1SuSp5pz6vnG0w4mcZHo690Ew/edit")

print(f"Sheet opened: {sh.url}")

# ========== TAB 1: Queue ==========
queue = sh.sheet1
queue.update_title("Queue")
queue_headers = ["Date", "Platform", "Content Type", "Hook", "Copy EN", "Copy HU", "Visual Brief", "Status", "Posted?"]
queue.update("A1:I1", [queue_headers])

# ========== TAB 2: Ideas Bank ==========
ideas = sh.add_worksheet(title="Ideas Bank", rows=100, cols=5)
ideas_headers = ["Date Added", "Topic", "Source", "Priority", "Used?"]
ideas.update("A1:E1", [ideas_headers])

# ========== TAB 3: CEEFM April ==========
ceefm = sh.add_worksheet(title="CEEFM April", rows=100, cols=8)
ceefm_headers = ["Week", "Date", "Hook", "Copy HU", "Copy EN", "Visual Brief", "Post Time", "Posted?"]
ceefm.update("A1:H1", [ceefm_headers])

ceefm_data = [
    ["Week 1", "01/04/2026", "Introducing CEE FM. 12 years. 50+ projects.", "A legtobb ember nem gondol a letesitmenykezelesre. Amig valami el nem romlik...", "Most people never think about facility management. Until something breaks...", "Wide-angle photo of clean Budapest apartment lobby. Morning light. CEEFM logo watermark.", "9:00 AM CEST", "FALSE"],
    ["Week 1", "02/04/2026", "Spring maintenance checklist for Budapest property managers", "Az aprilis Budapesten a letesitmenykezelok szamara egyet jelent: tavaszi karbantartasi szezon...", "April in Budapest means one thing for property managers: spring maintenance season...", "Flat-lay maintenance icons: wrench, thermometer, checklist. Navy/gold/ivory palette.", "9:00 AM CEST", "FALSE"],
    ["Week 1", "03/04/2026", "What 5 AM looks like at a Budapest hotel", "Reggel 5:00. A szalloda aulaja csendes. A csapatunk mar a helyszinen van...", "5:00 AM. The hotel lobby is quiet. Our team is already on-site...", "B&W photo of neatly made hotel bed. Crisp sheets. Early morning light.", "8:30 AM CEST", "FALSE"],
    ["Week 2", "08/04/2026", "Why CEEFM uses eco-friendly cleaning products", "Harom eve hagytuk abba a hagyomanyos tisztitoszerek hasznalatat...", "We stopped using conventional cleaning chemicals three years ago...", "Close-up eco-friendly cleaning products with EU Ecolabel. Natural light.", "9:00 AM CEST", "FALSE"],
    ["Week 2", "09/04/2026", "Energy costs in Budapest buildings and what FM can do", "A budapesti kereskedelmi epuletek energiakoltsegei 40%-kal novekedtek...", "Energy costs for Budapest commercial buildings rose 40% between 2022 and 2025...", "Infographic: energy cost reduction percentages. Bar chart/icons. Navy/gold/ivory.", "12:00 PM CEST", "FALSE"],
    ["Week 2", "10/04/2026", "What makes a good facility supervisor", "12 ev alatt tobb mint 50 letesitmenykezelesi felugyelot vettunk fel...", "We have hired over 50 facility supervisors in 12 years...", "Portrait-style: person in workwear with clipboard in building corridor.", "9:00 AM CEST", "FALSE"],
    ["Week 3", "15/04/2026", "Three hotel housekeeping standards guests actually notice", "A szallodavendegek nem olvassak el a hazvezeteseg muveleti eljarasait...", "Hotel guests do not read your housekeeping SOP...", "Split image: pristine bathroom mirror + perfectly made bed linens.", "9:00 AM CEST", "FALSE"],
    ["Week 3", "16/04/2026", "Student housing FM. Different rules, different challenges.", "A diakszallas nem ugyanaz, mint a szallodakezeles...", "Student housing is not the same as hotel management...", "Photo of modern student housing common area. Clean, functional design.", "9:00 AM CEST", "FALSE"],
    ["Week 3", "17/04/2026", "Smart building tech. What actually delivers ROI.", "Minden 2026-os letesitmenykezelesi konferencia az okos epuletekrol beszel...", "Every facility management conference in 2026 talks about smart buildings...", "Tech graphic: thermostat, water sensor, mobile ticket, lightbulb+wifi icons.", "12:00 PM CEST", "FALSE"],
    ["Week 4", "22/04/2026", "Sustainability at CEEFM. What we actually do.", "A fenntarthatosag a leginkabb tulhasznalt szo a letesitmenykezelesi marketingben...", "Sustainability is the most overused word in FM marketing...", "CEEFM ops: eco products, waste sorting, repair over replace. Earth Day.", "9:00 AM CEST", "FALSE"],
    ["Week 4", "23/04/2026", "Budapest's property boom and what it means for FM", "Budapest irodapiaca 4,25 millio negyzetmeter...", "Budapest's office market is 4.25 million square meters...", "Aerial Budapest skyline with modern buildings. Or data map of districts.", "9:00 AM CEST", "FALSE"],
    ["Week 4", "24/04/2026", "Five reasons to outsource facility management", "Kezelhetik az epuletuk letesitmenyeit haazon belul...", "You can manage your building's facilities in-house. Many property owners do...", "Comparison graphic: In-house complexity vs CEEFM unified. Navy/gold/ivory.", "9:00 AM CEST", "FALSE"],
]
ceefm.update("A2:H13", ceefm_data)

# ========== TAB 4: Analytics ==========
analytics = sh.add_worksheet(title="Analytics", rows=100, cols=8)
analytics_headers = ["Date", "Platform", "Hook Preview", "Impressions", "Comments", "Reposts", "Clicks", "Notes"]
analytics.update("A1:H1", [analytics_headers])

# ========== TAB 5: Clients ==========
clients = sh.add_worksheet(title="Clients", rows=100, cols=7)
clients_headers = ["Client", "Platform", "Posts/Week", "Start Date", "Week Number", "Next Post Due", "Notes"]
clients.update("A1:G1", [clients_headers])
clients.update("A2:G2", [["CEEFM Kft", "LinkedIn", "3", "01/04/2026", "Week 1", "01/04/2026", ""]])

# ========== FORMATTING via Sheets API ==========
spreadsheet_id = sh.id

# Get sheet IDs
sheet_metadata = sh.fetch_sheet_metadata()
sheet_ids = {}
for s in sheet_metadata["sheets"]:
    title = s["properties"]["title"]
    sheet_ids[title] = s["properties"]["sheetId"]

def header_format_request(sheet_id, num_cols):
    """Format header row: navy background, gold text, bold, frozen."""
    return [
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": num_cols},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": NAVY,
                        "textFormat": {"foregroundColor": GOLD, "bold": True, "fontFamily": "Inter", "fontSize": 11},
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
            }
        },
        {
            "updateSheetProperties": {
                "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 1}},
                "fields": "gridProperties.frozenRowCount"
            }
        }
    ]

def bg_format_request(sheet_id, num_cols, start_row=1, end_row=100):
    """Ivory background for data rows."""
    return [{
        "repeatCell": {
            "range": {"sheetId": sheet_id, "startRowIndex": start_row, "endRowIndex": end_row, "startColumnIndex": 0, "endColumnIndex": num_cols},
            "cell": {"userEnteredFormat": {"backgroundColor": IVORY}},
            "fields": "userEnteredFormat.backgroundColor"
        }
    }]

def column_width_request(sheet_id, col_index, width):
    return {
        "updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": col_index, "endIndex": col_index + 1},
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    }

def dropdown_request(sheet_id, col_index, values, end_row=100):
    return {
        "setDataValidation": {
            "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": end_row, "startColumnIndex": col_index, "endColumnIndex": col_index + 1},
            "rule": {
                "condition": {
                    "type": "ONE_OF_LIST",
                    "values": [{"userEnteredValue": v} for v in values]
                },
                "showCustomUi": True,
                "strict": True
            }
        }
    }

def checkbox_request(sheet_id, col_index, end_row=100):
    return {
        "setDataValidation": {
            "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": end_row, "startColumnIndex": col_index, "endColumnIndex": col_index + 1},
            "rule": {"condition": {"type": "BOOLEAN"}, "showCustomUi": True}
        }
    }

# Build all requests
requests = []

# Queue formatting
qid = sheet_ids["Queue"]
requests += header_format_request(qid, 9)
requests += bg_format_request(qid, 9)
queue_widths = [110, 160, 140, 250, 300, 300, 200, 100, 80]
for i, w in enumerate(queue_widths):
    requests.append(column_width_request(qid, i, w))
requests.append(dropdown_request(qid, 1, ["Emmanuel LinkedIn", "BridgeWorks LinkedIn", "CEEFM LinkedIn", "Twitter-X", "Instagram"]))
requests.append(dropdown_request(qid, 2, ["Observation", "Story", "Breakdown", "Industry Insight", "Case Study", "Company Update"]))
requests.append(dropdown_request(qid, 7, ["Draft", "Review", "Approved", "Posted"]))
requests.append(checkbox_request(qid, 8))

# Ideas Bank formatting
iid = sheet_ids["Ideas Bank"]
requests += header_format_request(iid, 5)
requests += bg_format_request(iid, 5)
ideas_widths = [120, 300, 200, 100, 80]
for i, w in enumerate(ideas_widths):
    requests.append(column_width_request(iid, i, w))
requests.append(dropdown_request(iid, 3, ["High", "Medium", "Low"]))
requests.append(checkbox_request(iid, 4))

# CEEFM April formatting
cid = sheet_ids["CEEFM April"]
requests += header_format_request(cid, 8)
requests += bg_format_request(cid, 8)
ceefm_widths = [80, 110, 280, 350, 350, 280, 120, 80]
for i, w in enumerate(ceefm_widths):
    requests.append(column_width_request(cid, i, w))
requests.append(checkbox_request(cid, 7))
# Wrap text for copy columns (C, D, E, F)
requests.append({
    "repeatCell": {
        "range": {"sheetId": cid, "startRowIndex": 1, "endRowIndex": 100, "startColumnIndex": 2, "endColumnIndex": 6},
        "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP"}},
        "fields": "userEnteredFormat.wrapStrategy"
    }
})

# Analytics formatting
aid = sheet_ids["Analytics"]
requests += header_format_request(aid, 8)
requests += bg_format_request(aid, 8)
analytics_widths = [110, 160, 250, 110, 100, 100, 100, 200]
for i, w in enumerate(analytics_widths):
    requests.append(column_width_request(aid, i, w))
requests.append(dropdown_request(aid, 1, ["Emmanuel LinkedIn", "BridgeWorks LinkedIn", "CEEFM LinkedIn", "Twitter-X", "Instagram"]))

# Clients formatting
clid = sheet_ids["Clients"]
requests += header_format_request(clid, 7)
requests += bg_format_request(clid, 7)
clients_widths = [150, 120, 100, 120, 120, 130, 250]
for i, w in enumerate(clients_widths):
    requests.append(column_width_request(clid, i, w))

# Execute all formatting in one batch
sh.batch_update({"requests": requests})

print(f"\nDone! Sheet URL:\n{sh.url}")
print(f"\nShared with: office@bridgeworks.agency")

# Save URL to file
url_file = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\content-planner-url.txt"
with open(url_file, "w") as f:
    f.write(sh.url)
print(f"URL saved to: {url_file}")
