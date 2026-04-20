/**
 * BridgeWorks Content Planner — Google Apps Script
 *
 * HOW TO USE:
 * 1. Open https://sheets.new
 * 2. Go to Extensions > Apps Script
 * 3. Delete the default code and paste this entire file
 * 4. Click Run (play button)
 * 5. Authorize when prompted
 * 6. The script builds all 5 tabs with headers, dropdowns, formatting, and data
 */

function setupContentPlanner() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.rename("BridgeWorks Content Planner");

  // Brand colors
  var navy = "#0F1A2E";
  var gold = "#B8860B";
  var ivory = "#F5F0E8";
  var charcoal = "#1C2B3A";
  var warmGray = "#6B6560";

  // ========== TAB 1: Queue ==========
  var queue = ss.getSheets()[0];
  queue.setName("Queue");
  var queueHeaders = ["Date", "Platform", "Content Type", "Hook", "Copy EN", "Copy HU", "Visual Brief", "Status", "Posted?"];
  queue.getRange(1, 1, 1, queueHeaders.length).setValues([queueHeaders]);

  // Header formatting
  formatHeader(queue, queueHeaders.length, navy, gold);

  // Platform dropdown (B2:B100)
  var platformRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["Emmanuel LinkedIn", "BridgeWorks LinkedIn", "CEEFM LinkedIn", "Twitter-X", "Instagram"])
    .setAllowInvalid(false)
    .build();
  queue.getRange("B2:B100").setDataValidation(platformRule);

  // Content Type dropdown (C2:C100)
  var contentTypeRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["Observation", "Story", "Breakdown", "Industry Insight", "Case Study", "Company Update"])
    .setAllowInvalid(false)
    .build();
  queue.getRange("C2:C100").setDataValidation(contentTypeRule);

  // Status dropdown (H2:H100)
  var statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["Draft", "Review", "Approved", "Posted"])
    .setAllowInvalid(false)
    .build();
  queue.getRange("H2:H100").setDataValidation(statusRule);

  // Posted? checkbox (I2:I100)
  queue.getRange("I2:I100").insertCheckboxes();

  // Column widths
  queue.setColumnWidth(1, 110); // Date
  queue.setColumnWidth(2, 160); // Platform
  queue.setColumnWidth(3, 140); // Content Type
  queue.setColumnWidth(4, 250); // Hook
  queue.setColumnWidth(5, 300); // Copy EN
  queue.setColumnWidth(6, 300); // Copy HU
  queue.setColumnWidth(7, 200); // Visual Brief
  queue.setColumnWidth(8, 100); // Status
  queue.setColumnWidth(9, 80);  // Posted?

  // Background
  queue.getRange("A2:I100").setBackground(ivory);

  // ========== TAB 2: Ideas Bank ==========
  var ideas = ss.insertSheet("Ideas Bank");
  var ideasHeaders = ["Date Added", "Topic", "Source", "Priority", "Used?"];
  ideas.getRange(1, 1, 1, ideasHeaders.length).setValues([ideasHeaders]);
  formatHeader(ideas, ideasHeaders.length, navy, gold);

  var priorityRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(["High", "Medium", "Low"])
    .setAllowInvalid(false)
    .build();
  ideas.getRange("D2:D100").setDataValidation(priorityRule);
  ideas.getRange("E2:E100").insertCheckboxes();

  ideas.setColumnWidth(1, 120);
  ideas.setColumnWidth(2, 300);
  ideas.setColumnWidth(3, 200);
  ideas.setColumnWidth(4, 100);
  ideas.setColumnWidth(5, 80);
  ideas.getRange("A2:E100").setBackground(ivory);

  // ========== TAB 3: CEEFM April ==========
  var ceefm = ss.insertSheet("CEEFM April");
  var ceefmHeaders = ["Week", "Date", "Hook", "Copy HU", "Copy EN", "Visual Brief", "Post Time", "Posted?"];
  ceefm.getRange(1, 1, 1, ceefmHeaders.length).setValues([ceefmHeaders]);
  formatHeader(ceefm, ceefmHeaders.length, navy, gold);

  // Pre-fill CEEFM April data from april-calendar.md
  var ceefmData = [
    ["Week 1", "01/04/2026", "Introducing CEE FM. 12 years. 50+ projects. Budapest and Hungary.", "A legtobb ember nem gondol a letesitmenykezelesre. Amig valami el nem romlik...", "Most people never think about facility management. Until something breaks...", "Wide-angle photo of clean Budapest apartment lobby. Morning light. CEEFM logo watermark.", "9:00 AM CEST", false],
    ["Week 1", "02/04/2026", "Spring maintenance checklist for Budapest property managers", "Az aprilis Budapesten a letesitmenykezelok szamara egyet jelent: tavaszi karbantartasi szezon...", "April in Budapest means one thing for property managers: spring maintenance season...", "Flat-lay maintenance icons: wrench, thermometer, checklist. Navy/gold/ivory palette.", "9:00 AM CEST", false],
    ["Week 1", "03/04/2026", "What 5 AM looks like at a Budapest hotel", "Reggel 5:00. A szalloda aulaja csendes. A csapatunk mar a helyszinen van...", "5:00 AM. The hotel lobby is quiet. Our team is already on-site...", "B&W photo of neatly made hotel bed. Crisp sheets. Early morning light.", "8:30 AM CEST", false],
    ["Week 2", "08/04/2026", "Why CEEFM uses eco-friendly cleaning products", "Harom eve hagytuk abba a hagyomanyos tisztitoszerek hasznalatat...", "We stopped using conventional cleaning chemicals three years ago...", "Close-up eco-friendly cleaning products with EU Ecolabel. Natural light.", "9:00 AM CEST", false],
    ["Week 2", "09/04/2026", "Energy costs in Budapest buildings and what FM can do", "A budapesti kereskedelmi epuletek energiakoltsegei 2022 es 2025 kozott 40%-kal novekedtek...", "Energy costs for Budapest commercial buildings rose 40% between 2022 and 2025...", "Infographic: energy cost reduction percentages. Bar chart/icons. Navy and gold on ivory.", "12:00 PM CEST", false],
    ["Week 2", "10/04/2026", "What makes a good facility supervisor", "12 ev alatt tobb mint 50 letesitmenykezelesi felugyelot vettunk fel...", "We have hired over 50 facility supervisors in 12 years...", "Portrait-style photo: person in professional workwear with clipboard in building corridor.", "9:00 AM CEST", false],
    ["Week 3", "15/04/2026", "Three hotel housekeeping standards guests actually notice", "A szallodavendegek nem olvassak el a hazvezeteseg muveleti eljarasait...", "Hotel guests do not read your housekeeping SOP...", "Split image: pristine bathroom mirror + perfectly made bed linens.", "9:00 AM CEST", false],
    ["Week 3", "16/04/2026", "Student housing FM. Different rules, different challenges.", "A diakszallas nem ugyanaz, mint a szallodakezeles...", "Student housing is not the same as hotel management...", "Photo of modern student housing common area. Clean, functional design.", "9:00 AM CEST", false],
    ["Week 3", "17/04/2026", "Smart building technology. What actually delivers ROI.", "Minden 2026-os letesitmenykezelesi konferencia az okos epuletekrol beszel...", "Every facility management conference in 2026 talks about smart buildings...", "Clean tech graphic: thermostat, water sensor, mobile ticket, lightbulb+wifi. ROI numbers.", "12:00 PM CEST", false],
    ["Week 4", "22/04/2026", "Sustainability at CEEFM. What we actually do, not what we say.", "A fenntarthatosag a leginkabb tulhasznalt szo a letesitmenykezelesi marketingben...", "Sustainability is the most overused word in facility management marketing...", "CEEFM operations: eco products, waste sorting, repair over replace. Earth Day tie-in.", "9:00 AM CEST", false],
    ["Week 4", "23/04/2026", "Budapest's property boom and what it means for FM", "Budapest irodapiaca 4,25 millio negyzetmeter. Kozep-Europa masodik legnagyobb piaca...", "Budapest's office market is 4.25 million square meters. Second largest in Central Europe...", "Aerial Budapest skyline with modern buildings. Or data map of districts with growth indicators.", "9:00 AM CEST", false],
    ["Week 4", "24/04/2026", "Five reasons to outsource facility management", "Kezelhetik az epuletuk letesitmenyeit haazon belul. Sok ingatlantulajdonos igy tesz...", "You can manage your building's facilities in-house. Many property owners do...", "Comparison graphic: In-house complexity vs CEEFM unified interface. Navy/gold/ivory.", "9:00 AM CEST", false]
  ];

  ceefm.getRange(2, 1, ceefmData.length, ceefmData[0].length).setValues(ceefmData);
  ceefm.getRange("H2:H100").insertCheckboxes();

  ceefm.setColumnWidth(1, 80);  // Week
  ceefm.setColumnWidth(2, 110); // Date
  ceefm.setColumnWidth(3, 280); // Hook
  ceefm.setColumnWidth(4, 350); // Copy HU
  ceefm.setColumnWidth(5, 350); // Copy EN
  ceefm.setColumnWidth(6, 280); // Visual Brief
  ceefm.setColumnWidth(7, 120); // Post Time
  ceefm.setColumnWidth(8, 80);  // Posted?
  ceefm.getRange("A2:H100").setBackground(ivory);

  // Wrap text for copy columns
  ceefm.getRange("C2:F100").setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);

  // ========== TAB 4: Analytics ==========
  var analytics = ss.insertSheet("Analytics");
  var analyticsHeaders = ["Date", "Platform", "Hook Preview", "Impressions", "Comments", "Reposts", "Clicks", "Notes"];
  analytics.getRange(1, 1, 1, analyticsHeaders.length).setValues([analyticsHeaders]);
  formatHeader(analytics, analyticsHeaders.length, navy, gold);

  analytics.getRange("B2:B100").setDataValidation(platformRule);

  analytics.setColumnWidth(1, 110);
  analytics.setColumnWidth(2, 160);
  analytics.setColumnWidth(3, 250);
  analytics.setColumnWidth(4, 110);
  analytics.setColumnWidth(5, 100);
  analytics.setColumnWidth(6, 100);
  analytics.setColumnWidth(7, 100);
  analytics.setColumnWidth(8, 200);
  analytics.getRange("A2:H100").setBackground(ivory);

  // Number formatting for metrics
  analytics.getRange("D2:G100").setNumberFormat("#,##0");

  // ========== TAB 5: Clients ==========
  var clients = ss.insertSheet("Clients");
  var clientsHeaders = ["Client", "Platform", "Posts/Week", "Start Date", "Week Number", "Next Post Due", "Notes"];
  clients.getRange(1, 1, 1, clientsHeaders.length).setValues([clientsHeaders]);
  formatHeader(clients, clientsHeaders.length, navy, gold);

  // Pre-fill CEEFM row
  var clientData = [["CEEFM Kft", "LinkedIn", 3, "01/04/2026", "Week 1", "01/04/2026", ""]];
  clients.getRange(2, 1, 1, clientData[0].length).setValues(clientData);

  clients.setColumnWidth(1, 150);
  clients.setColumnWidth(2, 120);
  clients.setColumnWidth(3, 100);
  clients.setColumnWidth(4, 120);
  clients.setColumnWidth(5, 120);
  clients.setColumnWidth(6, 130);
  clients.setColumnWidth(7, 250);
  clients.getRange("A2:G100").setBackground(ivory);

  // Final touches
  ss.setActiveSheet(queue);
  SpreadsheetApp.flush();

  // Show completion message
  SpreadsheetApp.getUi().alert(
    "BridgeWorks Content Planner is ready!\n\n" +
    "5 tabs created:\n" +
    "1. Queue — content pipeline with dropdowns\n" +
    "2. Ideas Bank — topic storage\n" +
    "3. CEEFM April — 12 posts pre-filled\n" +
    "4. Analytics — performance tracking\n" +
    "5. Clients — client overview\n\n" +
    "Copy the sheet URL and save it."
  );
}

function formatHeader(sheet, numCols, bgColor, textColor) {
  var headerRange = sheet.getRange(1, 1, 1, numCols);
  headerRange.setBackground(bgColor);
  headerRange.setFontColor(textColor);
  headerRange.setFontWeight("bold");
  headerRange.setFontFamily("Inter");
  headerRange.setFontSize(11);
  headerRange.setHorizontalAlignment("center");
  headerRange.setVerticalAlignment("middle");
  sheet.setRowHeight(1, 36);
  sheet.setFrozenRows(1);
}
