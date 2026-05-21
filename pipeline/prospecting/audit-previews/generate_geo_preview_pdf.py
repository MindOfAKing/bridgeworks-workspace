from __future__ import annotations

from pathlib import Path
import textwrap


OUT = Path(__file__).with_name("bridgeworks-geo-audit-preview-pyramidon-2026-05-19.pdf")

PAGE_W = 612
PAGE_H = 792
IVORY = (0.9608, 0.9412, 0.9098)
NAVY = (0.0588, 0.1020, 0.1804)
GOLD = (0.7216, 0.5255, 0.0431)
SAGE = (0.2902, 0.4039, 0.2549)
CHARCOAL = (0.1098, 0.1686, 0.2275)
MUTED = (0.38, 0.38, 0.38)


def esc(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def color(c: tuple[float, float, float]) -> str:
    return f"{c[0]:.4f} {c[1]:.4f} {c[2]:.4f}"


class Page:
    def __init__(self):
        self.ops: list[str] = []
        self.y = 720
        self.ops.append(f"{color(IVORY)} rg 0 0 {PAGE_W} {PAGE_H} re f")

    def rect(self, x, y, w, h, c):
        self.ops.append(f"{color(c)} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")

    def text(self, x, y, text, size=11, font="F1", c=CHARCOAL):
        self.ops.append(f"BT /{font} {size} Tf {color(c)} rg {x:.1f} {y:.1f} Td ({esc(text)}) Tj ET")

    def lines(self, x, y, text, size=11, font="F1", c=CHARCOAL, width=82, leading=15):
        cursor = y
        for para in text.split("\n"):
            if not para.strip():
                cursor -= leading
                continue
            for line in textwrap.wrap(para, width=width):
                self.text(x, cursor, line, size=size, font=font, c=c)
                cursor -= leading
        return cursor

    def footer(self, n):
        self.text(54, 32, "office@bridgeworks.agency | bridgeworks.agency", 8, "F1", MUTED)
        self.text(540, 32, str(n), 8, "F1", MUTED)

    def stream(self) -> str:
        return "\n".join(self.ops)


pages: list[Page] = []

# Page 1
p = Page()
p.rect(0, 610, PAGE_W, 182, NAVY)
p.rect(54, 632, 6, 110, GOLD)
p.text(78, 724, "BridgeWorks.agency", 18, "F2", IVORY)
p.text(78, 684, "GEO Audit Preview", 34, "F2", IVORY)
p.text(78, 650, "Pyramidon | pyramidon.hu/en", 17, "F1", IVORY)
p.text(78, 626, "Prepared 2026-05-19", 10, "F1", IVORY)
p.text(54, 552, "Audit thesis", 19, "F2", NAVY)
p.lines(
    54,
    520,
    "Pyramidon already has strong proof: 6,500+ apartments managed, 35+ years of experience, "
    "98% client satisfaction, named team members, direct emails, and clear Budapest district focus. "
    "The gap is not substance. The gap is that this proof is not yet packaged for AI systems, answer engines, "
    "and local search platforms to confidently cite and recommend the company.",
    size=12,
    width=76,
    leading=17,
)
p.rect(54, 310, 504, 92, (1, 1, 1))
p.rect(54, 310, 6, 92, GOLD)
p.text(78, 360, "Preview GEO Readiness", 15, "F2", NAVY)
p.text(78, 326, "50/100", 34, "F2", NAVY)
p.text(210, 336, "Below Average | preview score, not a full audit score", 11, "F1", CHARCOAL)
p.footer(1)
pages.append(p)

# Page 2
p = Page()
p.text(54, 728, "Three GEO Findings", 25, "F2", NAVY)
p.rect(54, 694, 504, 1.5, GOLD)
items = [
    (
        "1. Strong proof exists, but it is not packaged for AI citation",
        "The homepage has numbers and proof that AI systems like: 6,500+ apartments, 35+ years, 98% satisfaction, "
        "services, districts, team members, and offices. But these are concentrated on one long page. AI systems "
        "cite concise, self-contained answer blocks and dedicated pages more reliably than broad homepage sections.",
        "High",
    ),
    (
        "2. Human trust signals need entity markup",
        "Pyramidon has named staff, roles, emails, phone numbers, services, and office locations. These should be "
        "connected with Organization or LocalBusiness schema, Service schema, Person schema, ContactPoint, FAQPage, "
        "BreadcrumbList, and sameAs links to verified third-party profiles.",
        "High",
    ),
    (
        "3. The AI crawler and indexing layer needs verification",
        "The live homepage is content-rich, but robots.txt, sitemap coverage, llms.txt, schema validation, canonical "
        "signals, Google Search Console, and Bing Webmaster signals need a technical GEO pass before AI accessibility "
        "can be trusted.",
        "Medium",
    ),
]
y = 660
for title, body, severity in items:
    p.text(54, y, title, 14, "F2", NAVY)
    p.text(474, y, f"Severity: {severity}", 9, "F1", GOLD if severity == "High" else SAGE)
    y = p.lines(54, y - 24, body, size=10.5, width=84, leading=14) - 18
p.footer(2)
pages.append(p)

# Page 3
p = Page()
p.text(54, 728, "Business Impact", 25, "F2", NAVY)
p.rect(54, 694, 504, 1.5, GOLD)
y = p.lines(
    54,
    660,
    "Pyramidon has the proof assets many competitors lack. That creates upside. The work is less about inventing "
    "a new message and more about structuring existing proof so search engines, AI systems, and property owners "
    "can understand it faster.",
    size=12,
    width=78,
    leading=17,
)
p.text(54, y - 20, "Likely gains", 17, "F2", NAVY)
y -= 50
for bullet in [
    "More visibility for Budapest property management queries.",
    "Better AI-generated recommendations in ChatGPT, Perplexity, Gemini, and Bing Copilot.",
    "Higher trust from condominium committees and property owners.",
    "Cleaner quote enquiries from better-qualified prospects.",
]:
    p.text(72, y, f"- {bullet}", 11, "F1", CHARCOAL)
    y -= 20
p.text(54, y - 10, "Quick win", 17, "F2", NAVY)
y = p.lines(
    54,
    y - 38,
    "Add a GEO foundation layer: FAQ block with schema, Organization and Service schema, Person schema for leadership, "
    "clean sitemap and robots.txt, and a short llms.txt file summarizing the company, services, team, offices, and proof numbers.",
    size=11,
    width=82,
    leading=15,
) - 10
p.text(54, y, "Bigger opportunity", 17, "F2", NAVY)
p.lines(
    54,
    y - 28,
    "Build a proof hub around the buyer questions Pyramidon already answers: how to compare property management "
    "companies, what transparent condominium accounting includes, and what professional common representation looks like in Districts III, XI, and XIII.",
    size=11,
    width=82,
    leading=15,
)
p.footer(3)
pages.append(p)

# Page 4
p = Page()
p.text(54, 728, "Recommended Next Step", 25, "F2", NAVY)
p.rect(54, 694, 504, 1.5, GOLD)
p.lines(
    54,
    650,
    "The right next step is a full GEO audit and implementation plan. The full audit should verify the technical layer, "
    "score the site across the GEO framework, and turn Pyramidon's existing proof into a structured visibility plan.",
    size=12,
    width=78,
    leading=17,
)
p.text(54, 560, "Full audit should include", 17, "F2", NAVY)
y = 526
for bullet in [
    "Verified GEO score and category breakdown.",
    "AI crawler access report.",
    "Sitemap and indexability review.",
    "Schema recommendations.",
    "AI-citable content plan.",
    "Quick wins ranked by effort and impact.",
    "30-day implementation roadmap.",
]:
    p.text(72, y, f"- {bullet}", 11, "F1", CHARCOAL)
    y -= 20
p.rect(54, 248, 504, 110, NAVY)
p.rect(54, 248, 6, 110, GOLD)
p.text(78, 322, "Suggested call topic", 12, "F1", IVORY)
p.lines(
    78,
    292,
    "How Pyramidon can turn its existing proof into better visibility across Google, ChatGPT, Perplexity, and local property-management searches.",
    size=15,
    font="F2",
    c=IVORY,
    width=56,
    leading=19,
)
p.footer(4)
pages.append(p)

objects: list[str] = []

font1 = "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
font2 = "<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>"
objects.extend([font1, font2])

page_obj_nums = []
content_obj_nums = []
for p in pages:
    content = p.stream().encode("latin-1", "replace")
    content_obj_nums.append(len(objects) + 1)
    objects.append(f"<< /Length {len(content)} >>\nstream\n{content.decode('latin-1')}\nendstream")
    page_obj_nums.append(len(objects) + 1)
    objects.append(
        f"<< /Type /Page /Parent 0 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
        f"/Resources << /Font << /F1 1 0 R /F2 2 0 R >> >> "
        f"/Contents {content_obj_nums[-1]} 0 R >>"
    )

pages_obj_num = len(objects) + 1
kids = " ".join(f"{n} 0 R" for n in page_obj_nums)
objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_nums)} >>")

catalog_obj_num = len(objects) + 1
objects.append(f"<< /Type /Catalog /Pages {pages_obj_num} 0 R >>")

objects = [obj.replace("/Parent 0 0 R", f"/Parent {pages_obj_num} 0 R") for obj in objects]

pdf = bytearray()
pdf.extend(b"%PDF-1.4\n")
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{i} 0 obj\n{obj}\nendobj\n".encode("latin-1", "replace"))
xref = len(pdf)
pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
pdf.extend(b"0000000000 65535 f \n")
for off in offsets[1:]:
    pdf.extend(f"{off:010d} 00000 n \n".encode())
pdf.extend(
    f"trailer\n<< /Size {len(objects)+1} /Root {catalog_obj_num} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
)

OUT.write_bytes(pdf)
print(OUT)
print(OUT.stat().st_size)
