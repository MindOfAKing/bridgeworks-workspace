import fs from "node:fs/promises";
import path from "node:path";
import { Presentation, PresentationFile } from "@oai/artifact-tool";

const buildDir = "C:\\Users\\User\\Projects\\bridgeworks-workspace\\clients\\oliviks\\delivery\\.pptx-build-2026-08-01";
const outputDir = path.join(buildDir, "rendered");
const finalPptx = "C:\\Users\\User\\Projects\\bridgeworks-workspace\\clients\\oliviks\\delivery\\OLIVIKS-PROJECT-DELIVERY-WALKTHROUGH-2026-08-01.pptx";
const clientRoot = "C:\\Users\\User\\Projects\\bridgeworks-workspace\\clients\\oliviks";

const assets = {
  logo: path.join(clientRoot, "website", "public", "images", "oliviks-logo-horizontal.png"),
  legacy: path.join(clientRoot, "evidence", "before", "legacy-home-desktop-2026-07-14.png"),
  homepage: path.join(clientRoot, "evidence", "after", "preview-home-desktop-2026-07-14.png"),
  menuMobile: path.join(clientRoot, "evidence", "after", "preview-menu-mobile-2026-07-14.png"),
  admin: path.join(clientRoot, "evidence", "after", "preview-admin-desktop-2026-07-14.png"),
  qrCard: path.join(clientRoot, "execution", "email-whatsapp", "print-assets", "oliviks-whatsapp-counter-card.png"),
};

const C = {
  canvas: "#FFFFFF",
  ink: "#111111",
  muted: "#5E6268",
  panel: "#F0F0EE",
  rule: "#BBBDBF",
  accent: "#D99B2B",
  accentSoft: "#F8EBD2",
  green: "#365E43",
  danger: "#9E4A3B",
};
const FONT = "Arial";
const W = 1280;
const H = 720;

function addText(slide, text, position, style = {}) {
  const box = slide.shapes.add({
    geometry: "textbox",
    position,
    fill: "none",
    line: { style: "solid", fill: "none", width: 0 },
  });
  box.text = text;
  box.text.style = {
    fontSize: style.fontSize ?? 24,
    typeface: FONT,
    color: style.color ?? C.ink,
    bold: style.bold ?? false,
    alignment: style.alignment ?? "left",
    verticalAlignment: style.verticalAlignment ?? "top",
    autoFit: style.autoFit ?? "shrinkText",
    ...style,
  };
  return box;
}

function addPanel(slide, position, fill = C.panel) {
  return slide.shapes.add({
    geometry: "rect",
    position,
    fill,
    line: { style: "solid", fill: fill, width: 0 },
  });
}

function addRule(slide, left, top, width, fill = C.rule, weight = 1) {
  return slide.shapes.add({
    geometry: "straightConnector1",
    position: { left, top, width, height: 0 },
    fill: "none",
    line: { style: "solid", fill, width: weight },
  });
}

async function addImage(slide, imagePath, position, alt, fit = "cover", crop) {
  const blob = await fs.readFile(imagePath);
  return slide.images.add({
    blob,
    contentType: "image/png",
    alt,
    fit,
    position,
    ...(crop ? { crop } : {}),
  });
}

function addHeader(slide, title, number, kicker = "OLIVIKS KITCHEN · FOUNDATION HANDOVER") {
  addText(slide, kicker, { left: 42, top: 32, width: 700, height: 28 }, {
    fontSize: 16, bold: true, color: C.green,
  });
  addText(slide, title, { left: 42, top: 72, width: 1160, height: 72 }, {
    fontSize: 48, bold: true, autoFit: "none",
  });
  addRule(slide, 42, 655, 1196);
  addText(slide, String(number).padStart(2, "0"), { left: 1170, top: 667, width: 68, height: 24 }, {
    fontSize: 14, color: C.muted, alignment: "right",
  });
}

function addNotes(slide, presenterNotes, sources) {
  const src = sources.map((s) => `- ${s}`).join("\n");
  slide.speakerNotes.textFrame.setText(`${presenterNotes}\n\n[Sources]\n${src}\n[/Sources]`);
  slide.speakerNotes.setVisible(true);
}

function addBulletList(slide, items, position, options = {}) {
  const lines = items.map((item) => `• ${item}`).join("\n");
  return addText(slide, lines, position, {
    fontSize: options.fontSize ?? 25,
    color: options.color ?? C.ink,
    autoFit: "shrinkText",
  });
}

const deck = Presentation.create({ slideSize: { width: W, height: H } });

// 1. Cover, based on Codex Grid slide 02.
{
  const slide = deck.slides.add();
  slide.background.fill = C.canvas;
  await addImage(slide, assets.logo, { left: 42, top: 36, width: 305, height: 88 }, "Oliviks Kitchen logo", "contain");
  addText(slide, "Project delivery\nwalkthrough", { left: 42, top: 250, width: 900, height: 250 }, {
    fontSize: 76, bold: true, verticalAlignment: "bottom", autoFit: "none",
  });
  addText(slide, "Website · ordering · visibility · retention", { left: 42, top: 548, width: 790, height: 44 }, {
    fontSize: 28, color: C.green, bold: true,
  });
  addText(slide, "Prepared by BridgeWorks · August 2026", { left: 882, top: 44, width: 356, height: 30 }, {
    fontSize: 18, color: C.muted, alignment: "right",
  });
  addRule(slide, 42, 635, 1196, C.accent, 4);
  addNotes(slide,
    "Open by saying this is a practical walkthrough, not a technical presentation. The goal is to show what was built, how the parts connect, and agree the final owner actions.",
    ["OLIVIKS-HANDOVER-2026-07-14.md", "Oliviks Foundation contract and verified delivery records"]);
}

// 2. Connected journey, based on Codex Grid slide 17.
{
  const slide = deck.slides.add();
  addHeader(slide, "The system connects discovery and repeat orders", 2);
  addRule(slide, 82, 260, 1110, C.ink, 2);
  const xs = [112, 472, 832];
  const labels = ["01 · DISCOVER", "02 · ORDER", "03 · RETURN"];
  const heads = ["Find and trust", "Choose a clear route", "Stay connected"];
  const bodies = [
    "A faster website explains the food, story, location, reviews, and award.",
    "Customers browse the menu, then continue to the existing shop, WhatsApp, Wolt, or Marwa.",
    "Email and WhatsApp tools turn one visit into a relationship and a reason to come back.",
  ];
  for (let i = 0; i < 3; i += 1) {
    slide.shapes.add({ geometry: "ellipse", position: { left: xs[i], top: 250, width: 22, height: 22 }, fill: C.accent, line: { style: "solid", fill: C.accent, width: 0 } });
    addText(slide, labels[i], { left: xs[i], top: 194, width: 300, height: 30 }, { fontSize: 18, color: C.green, bold: true });
    addText(slide, heads[i], { left: xs[i], top: 312, width: 310, height: 76 }, { fontSize: 29, bold: true });
    addText(slide, bodies[i], { left: xs[i], top: 402, width: 310, height: 158 }, { fontSize: 21, color: C.muted });
  }
  addNotes(slide,
    "Explain the system as one customer journey. BridgeWorks did not replace the existing checkout. It made the path into that checkout clearer and added the retention layer around it.",
    ["OLIVIKS-HANDOVER-2026-07-14.md §1", "OLIVIKS-ORDERING-JOURNEY-COMPARISON-2026-07-14.md"]);
}

// 3. Before/after visual comparison, based on Codex Grid slide 11.
{
  const slide = deck.slides.add();
  addHeader(slide, "The new website makes the next step obvious", 3);
  addText(slide, "BEFORE · LEGACY SITE", { left: 42, top: 160, width: 560, height: 28 }, { fontSize: 18, color: C.danger, bold: true });
  addText(slide, "AFTER · NEW PREVIEW", { left: 657, top: 160, width: 580, height: 28 }, { fontSize: 18, color: C.green, bold: true });
  addPanel(slide, { left: 42, top: 198, width: 580, height: 340 }, "#E6E6E6");
  addPanel(slide, { left: 657, top: 198, width: 580, height: 340 }, C.accentSoft);
  await addImage(slide, assets.legacy, { left: 54, top: 210, width: 556, height: 316 }, "Legacy Oliviks homepage", "cover", { left: 0, top: 0, right: 0, bottom: 0.25 });
  await addImage(slide, assets.homepage, { left: 669, top: 210, width: 556, height: 316 }, "New Oliviks homepage preview", "cover", { left: 0, top: 0, right: 0, bottom: 0.25 });
  addText(slide, "Many overlapping routes and a heavier storefront.", { left: 42, top: 560, width: 570, height: 54 }, { fontSize: 22, color: C.muted });
  addText(slide, "Clear story, proof, menu, and intent-specific order routes.", { left: 657, top: 560, width: 580, height: 54 }, { fontSize: 22, color: C.muted });
  addNotes(slide,
    "Use the screenshots to show the shift from a shop-first surface to a clearer marketing and ordering journey. The new preview keeps the existing shop behind focused calls to action.",
    ["evidence/before/legacy-home-desktop-2026-07-14.png", "evidence/after/preview-home-desktop-2026-07-14.png", "OLIVIKS-ORDERING-JOURNEY-COMPARISON-2026-07-14.md"]);
}

// 4. Performance evidence, sparse metric composition.
{
  const slide = deck.slides.add();
  addHeader(slide, "A faster mobile experience", 4);
  addText(slide, "2.84 s", { left: 64, top: 206, width: 330, height: 110 }, { fontSize: 78, bold: true, color: C.green, autoFit: "none" });
  addText(slide, "new preview mobile LCP", { left: 68, top: 318, width: 360, height: 40 }, { fontSize: 24, color: C.muted });
  addText(slide, "390 KB", { left: 470, top: 206, width: 330, height: 110 }, { fontSize: 78, bold: true, color: C.green, autoFit: "none" });
  addText(slide, "mobile transfer size", { left: 474, top: 318, width: 360, height: 40 }, { fontSize: 24, color: C.muted });
  addText(slide, "21", { left: 888, top: 206, width: 250, height: 110 }, { fontSize: 78, bold: true, color: C.green, autoFit: "none" });
  addText(slide, "mobile resources", { left: 892, top: 318, width: 300, height: 40 }, { fontSize: 24, color: C.muted });
  addRule(slide, 64, 397, 1128, C.accent, 4);
  addText(slide, "Compared with the legacy mobile trace: 23.28 s LCP, 5,556 KB transferred, and 102 resources.", { left: 64, top: 440, width: 1050, height: 72 }, { fontSize: 28, bold: true });
  addText(slide, "Controlled one-run comparison on the public legacy site and Vercel preview. Repeat after domain cutover.", { left: 64, top: 538, width: 1050, height: 52 }, { fontSize: 20, color: C.muted });
  addNotes(slide,
    "Present the direction of change, not a guarantee. These are controlled comparative traces, not official PageSpeed scores. The production-domain check comes after cutover.",
    ["OLIVIKS-FUNCTIONAL-PERFORMANCE-AUDIT-2026-07-14.md §Before-and-After Performance"]);
}

// 5. Delivery inventory, based on half-text/half-image.
{
  const slide = deck.slides.add();
  addHeader(slide, "What BridgeWorks built and verified", 5);
  addBulletList(slide, [
    "A responsive Next.js website with Home, Menu, About, Contact, Catering, Privacy, and Admin routes",
    "A 33-item menu mapped to the existing WooCommerce shop, plus WhatsApp and delivery-platform routes",
    "Restaurant schema, AI-readable business information, and local robots/sitemap routes",
    "Google profile improvements, review handling, and Restaurant Guru award proof",
    "MailerLite welcome automation, weekly-special templates, WhatsApp copy, and a printable counter QR card",
  ], { left: 42, top: 176, width: 665, height: 426 }, { fontSize: 23 });
  addPanel(slide, { left: 755, top: 158, width: 483, height: 472 }, C.accentSoft);
  await addImage(slide, assets.menuMobile, { left: 835, top: 174, width: 250, height: 442 }, "Oliviks menu on mobile", "contain");
  addText(slide, "33-item menu", { left: 1080, top: 532, width: 145, height: 58 }, { fontSize: 24, bold: true, color: C.green, alignment: "right" });
  addNotes(slide,
    "Move from the visible website into the wider system. Emphasize that the valuable delivery is the connected infrastructure, not only the visual redesign.",
    ["OLIVIKS-DELIVERY-VERIFICATION-2026-07-14.md", "OLIVIKS-FUNCTIONAL-PERFORMANCE-AUDIT-2026-07-14.md", "OLIVIKS-HANDOVER-2026-07-14.md"]);
}

// 6. Weekly operating rhythm, based on Codex Grid slide 18.
{
  const slide = deck.slides.add();
  addHeader(slide, "A weekly rhythm keeps the system useful", 6);
  const lefts = [42, 452, 862];
  const headings = ["Keep the menu current", "Send one weekly special", "Protect trust"];
  const texts = [
    "Update availability, photos, descriptions, and website prices. Keep WooCommerce prices aligned separately.",
    "Use the MailerLite template, then reuse the same offer in the WhatsApp broadcast list.",
    "Reply to new Google reviews, check ordering links, and flag any incorrect public information.",
  ];
  const labels = ["WHEN NEEDED", "THU OR FRI", "EVERY WEEK"];
  for (let i = 0; i < 3; i += 1) {
    addPanel(slide, { left: lefts[i], top: 176, width: 370, height: 362 }, i === 1 ? C.accentSoft : C.panel);
    addText(slide, headings[i], { left: lefts[i] + 28, top: 214, width: 314, height: 76 }, { fontSize: 31, bold: true });
    addText(slide, texts[i], { left: lefts[i] + 28, top: 310, width: 314, height: 164 }, { fontSize: 22, color: C.muted });
    addText(slide, labels[i], { left: lefts[i], top: 574, width: 370, height: 32 }, { fontSize: 18, color: C.green, bold: true, alignment: "center" });
  }
  addNotes(slide,
    "Use this slide as the live operating guide. Menu edits need the database reactivated first. WhatsApp broadcast-list creation happens on the owners' phone.",
    ["OLIVIKS-HANDOVER-2026-07-14.md §3", "execution/email-whatsapp/HANDOVER.md"]);
}

// 7. Current gates, with admin and QR visual evidence.
{
  const slide = deck.slides.add();
  addHeader(slide, "The walkthrough closes the owner gates", 7);
  addText(slide, "READY TO REVIEW", { left: 42, top: 180, width: 390, height: 30 }, { fontSize: 18, color: C.green, bold: true });
  addBulletList(slide, [
    "Approve the new site content, menu, photos, address, and ordering wording",
    "Confirm the domain move from the legacy root to the new site",
    "Choose the final timing for one controlled signup and welcome-email test",
  ], { left: 42, top: 228, width: 580, height: 242 }, { fontSize: 24 });
  addText(slide, "OWNER SETUP", { left: 42, top: 488, width: 390, height: 30 }, { fontSize: 18, color: C.accent, bold: true });
  addText(slide, "Reactivate the paused menu database, create the WhatsApp broadcast list, and place the counter QR card.", { left: 42, top: 530, width: 590, height: 86 }, { fontSize: 23, bold: true });
  addPanel(slide, { left: 684, top: 158, width: 554, height: 474 }, C.panel);
  await addImage(slide, assets.admin, { left: 700, top: 174, width: 522, height: 260 }, "Oliviks admin interface", "cover", { left: 0, top: 0, right: 0, bottom: 0.15 });
  await addImage(slide, assets.qrCard, { left: 886, top: 456, width: 150, height: 150 }, "Oliviks WhatsApp counter QR card", "contain");
  addText(slide, "Current note: the free-tier database paused on 31 July and must be reactivated before live menu editing.", { left: 712, top: 456, width: 162, height: 148 }, { fontSize: 18, color: C.danger, bold: true });
  addNotes(slide,
    "Be transparent about current state. The site remains demonstrable through its static menu fallback, but live owner editing requires reactivating Supabase. Ask for content approval before any domain change.",
    ["Gmail message 19fb8898252987bc, 2026-07-31", "OLIVIKS-COMPLETION-CHECKLIST-2026-07-14.md", "evidence/after/preview-admin-desktop-2026-07-14.png"]);
}

// 8. Close, based on Codex Grid slide 26.
{
  const slide = deck.slides.add();
  addText(slide, "NEXT STEP", { left: 42, top: 42, width: 280, height: 34 }, { fontSize: 18, color: C.green, bold: true });
  addText(slide, "Approve.\nActivate.\nHand over.", { left: 42, top: 176, width: 880, height: 330 }, {
    fontSize: 74, bold: true, autoFit: "none",
  });
  addText(slide, "On the call we will review the build, complete the setup decisions, and capture your feedback.", { left: 42, top: 548, width: 790, height: 76 }, { fontSize: 26, color: C.muted });
  addText(slide, "office@bridgeworks.agency", { left: 880, top: 590, width: 358, height: 34 }, { fontSize: 20, alignment: "right", color: C.green, bold: true });
  addRule(slide, 42, 652, 1196, C.accent, 4);
  addNotes(slide,
    "Close by asking for the three decisions: content approval, preferred setup/cutover sequence, and confirmation that the delivered system meets expectations. Then ask for candid feedback.",
    ["OLIVIKS-SCOPE-AND-DECISIONS-2026-07-14.md", "OLIVIKS-HANDOVER-2026-07-14.md"]);
}

await fs.mkdir(outputDir, { recursive: true });
for (const [index, slide] of deck.slides.items.entries()) {
  const stem = `slide-${String(index + 1).padStart(2, "0")}`;
  const png = await deck.export({ slide, format: "png", scale: 1 });
  await fs.writeFile(path.join(outputDir, `${stem}.png`), new Uint8Array(await png.arrayBuffer()));
  const layout = await slide.export({ format: "layout" });
  await fs.writeFile(path.join(outputDir, `${stem}.layout.json`), await layout.text(), "utf8");
}
const montage = await deck.export({ format: "webp", montage: true, scale: 1 });
await fs.writeFile(path.join(outputDir, "deck-montage.webp"), new Uint8Array(await montage.arrayBuffer()));
const pptx = await PresentationFile.exportPptx(deck);
await pptx.save(finalPptx);

console.log(JSON.stringify({ finalPptx, slides: deck.slides.items.length, outputDir }, null, 2));
