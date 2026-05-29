// Render the CEEFM handover markdown into a branded BridgeWorks Word document.
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, HeadingLevel, VerticalAlign, ImageRun,
} = require("docx");

const CHART_DIR = "C:\\Users\\ELITEX21012G2\\Projects\\bridgeworks-workspace\\clients\\ceefm\\brand-visuals\\charts\\";

const SRC = "C:\\Users\\ELITEX21012G2\\Projects\\bridgeworks-workspace\\clients\\ceefm\\CEEFM-HANDOVER-2026-05.md";
const OUT = "C:\\Users\\ELITEX21012G2\\Projects\\bridgeworks-workspace\\clients\\ceefm\\CEEFM-HANDOVER-2026-05.docx";

const NAVY = "0F1A2E";
const GOLD = "B8860B";
const CHARCOAL = "1C2B3A";
const WARMGRAY = "6B6560";
const IVORY = "F5F0E8";
const WHITE = "FFFFFF";
const BODY = "Inter";
const HEAD = "Playfair Display";

const CONTENT_W = 9360; // US Letter, 1" margins

// ---- inline bold parser ----
function runs(text, base = {}) {
  const out = [];
  for (const seg of text.split(/(\*\*.*?\*\*)/g)) {
    if (!seg) continue;
    if (seg.startsWith("**") && seg.endsWith("**")) {
      out.push(new TextRun({ text: seg.slice(2, -2), bold: true, font: BODY, color: base.color || CHARCOAL, size: base.size || 21 }));
    } else {
      out.push(new TextRun({ text: seg, font: BODY, color: base.color || CHARCOAL, size: base.size || 21 }));
    }
  }
  if (out.length === 0) out.push(new TextRun({ text: "", font: BODY }));
  return out;
}

const cellBorder = { style: BorderStyle.SINGLE, size: 2, color: "D8D2C7" };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

function buildTable(rows) {
  const ncols = Math.max(...rows.map((r) => r.length));
  const colW = Math.floor(CONTENT_W / ncols);
  const widths = Array(ncols).fill(colW);
  widths[ncols - 1] = CONTENT_W - colW * (ncols - 1);

  const trs = rows.map((cells, ri) =>
    new TableRow({
      tableHeader: ri === 0,
      children: Array.from({ length: ncols }, (_, ci) => {
        const txt = (cells[ci] || "").replace(/\*\*/g, "");
        const isHead = ri === 0;
        const fill = isHead ? NAVY : ri % 2 === 0 ? IVORY : WHITE;
        return new TableCell({
          width: { size: widths[ci], type: WidthType.DXA },
          borders: cellBorders,
          shading: { fill, type: ShadingType.CLEAR, color: "auto" },
          margins: { top: 60, bottom: 60, left: 110, right: 110 },
          verticalAlign: VerticalAlign.CENTER,
          children: [new Paragraph({
            children: [new TextRun({
              text: txt, font: BODY, size: 18,
              bold: isHead, color: isHead ? WHITE : CHARCOAL,
            })],
          })],
        });
      }),
    })
  );

  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: trs,
  });
}

// ---- parse markdown ----
const lines = fs.readFileSync(SRC, "utf8").split(/\r?\n/);
let i = 0;
while (i < lines.length && lines[i].trim() !== "---") i++; // skip header block
i++;

const body = [];
let tbuf = [];

function flushTable() {
  if (!tbuf.length) return;
  const rows = tbuf
    .filter((r) => !/^\|[\s:\-|]+\|?\s*$/.test(r.trim()))
    .map((r) => r.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim()));
  if (rows.length) { body.push(buildTable(rows)); body.push(new Paragraph({ spacing: { after: 120 } })); }
  tbuf = [];
}

for (; i < lines.length; i++) {
  const line = lines[i];
  const s = line.trim();

  if (s.startsWith("|")) { tbuf.push(line); continue; }
  flushTable();

  if (s === "---" || s === "") continue;

  const chartM = s.match(/^!\[chart:([a-z0-9-]+)\]$/);
  if (chartM) {
    const imgPath = CHART_DIR + chartM[1] + ".png";
    if (fs.existsSync(imgPath)) {
      const png = fs.readFileSync(imgPath);
      // chart is 1568x812-ish; scale to ~5.6" wide preserving ratio
      const w = 540, h = Math.round(w * 0.52);
      body.push(new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 120, after: 160 },
        children: [new ImageRun({
          type: "png", data: png,
          transformation: { width: w, height: h },
          altText: { title: chartM[1], description: "CEEFM chart", name: chartM[1] },
        })],
      }));
    }
    continue;
  }

  if (s.startsWith("### ")) {
    body.push(new Paragraph({
      spacing: { before: 180, after: 80 },
      children: [new TextRun({ text: s.slice(4), bold: true, font: BODY, size: 24, color: GOLD })],
    }));
  } else if (s.startsWith("## ")) {
    body.push(new Paragraph({
      spacing: { before: 280, after: 120 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 2 } },
      children: [new TextRun({ text: s.slice(3), bold: true, font: HEAD, size: 30, color: NAVY })],
    }));
  } else if (s.startsWith("# ")) {
    body.push(new Paragraph({
      spacing: { before: 200, after: 160 },
      children: [new TextRun({ text: s.slice(2), bold: true, font: HEAD, size: 40, color: NAVY })],
    }));
  } else if (/^\d+\.\s/.test(s)) {
    body.push(new Paragraph({
      numbering: { reference: "nums", level: 0 },
      spacing: { after: 60 },
      children: runs(s.replace(/^\d+\.\s/, "")),
    }));
  } else if (s.startsWith("- ")) {
    body.push(new Paragraph({
      numbering: { reference: "bullets", level: 0 },
      spacing: { after: 40 },
      children: runs(s.slice(2)),
    }));
  } else if (s.startsWith(">")) {
    body.push(new Paragraph({
      spacing: { after: 80 }, indent: { left: 360 },
      border: { left: { style: BorderStyle.SINGLE, size: 18, color: GOLD, space: 8 } },
      children: runs(s.replace(/^>\s?/, ""), { color: WARMGRAY }),
    }));
  } else if (s.startsWith("*") && s.endsWith("*") && !s.startsWith("**")) {
    body.push(new Paragraph({
      spacing: { before: 120, after: 60 },
      children: [new TextRun({ text: s.replace(/^\*|\*$/g, ""), italics: true, font: BODY, size: 16, color: WARMGRAY })],
    }));
  } else {
    body.push(new Paragraph({ spacing: { after: 100 }, children: runs(s) }));
  }
}
flushTable();

// ---- title page ----
const sp = (n) => Array.from({ length: n }, () => new Paragraph({ children: [] }));
const titlePage = [
  ...sp(5),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "BRIDGEWORKS", bold: true, font: BODY, size: 28, color: GOLD, characterSpacing: 60 })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200 }, children: [new TextRun({ text: "CEEFM Kft", bold: true, font: HEAD, size: 80, color: NAVY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: [new TextRun({ text: "Digital Growth Handover", font: HEAD, size: 40, color: CHARCOAL })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 4 } }, children: [] }),
  ...sp(2),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Prepared for Victor, CEEFM Kft", font: BODY, size: 22, color: WARMGRAY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Prepared by BridgeWorks", font: BODY, size: 22, color: WARMGRAY })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "May 29, 2026", font: BODY, size: 22, color: WARMGRAY })] }),
  new Paragraph({ children: [new PageBreak()] }),
];

const doc = new Document({
  creator: "BridgeWorks",
  title: "CEEFM Kft Digital Growth Handover",
  styles: { default: { document: { run: { font: BODY, size: 21, color: CHARCOAL } } } },
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: "bullet", text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
      { reference: "nums", levels: [{ level: 0, format: "decimal", text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1296, right: 1440, bottom: 1296, left: 1440 } } },
    footers: {
      default: new Footer({ children: [new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: "BridgeWorks   ·   CEEFM Digital Growth Handover   ·   ", font: BODY, size: 14, color: WARMGRAY }),
          new TextRun({ children: [PageNumber.CURRENT], font: BODY, size: 14, color: WARMGRAY }),
        ],
      })] }),
    },
    children: [...titlePage, ...body],
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log("SAVED", OUT, buf.length, "bytes"); });
