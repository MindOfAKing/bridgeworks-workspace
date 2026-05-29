"""
BridgeWorks branded Markdown -> HTML -> PDF generator.

Follows business-brain/world-model/org/brand/brand-visual.md:
- Ivory #F5F0E8 background (never pure white), Navy headlines, Charcoal body
- Playfair Display for display/headlines, Inter for body/UI
- Gold thin rule under section headers (the bridge motif), accent only
- Sage for positive/growth metrics
- Embeds the real brand TTF fonts via @font-face and the BridgeWorks SVG logo

Renders with Playwright Chromium (preferred per pdf skill); falls back to weasyprint.
Usage: python build-pdf.py <input.md> <output.pdf> [--title "..."] [--subtitle "..."]
"""
import sys, os, re, base64, html

FONT_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\operations\fonts"
LOGO_SVG = r"C:\Users\ELITEX21012G2\Projects\business-brain\world-model\org\brand\logos\bridgeworks-logo-dark.svg"
CHART_DIR = r"C:\Users\ELITEX21012G2\Projects\bridgeworks-workspace\clients\ceefm\brand-visuals\charts"

NAVY="#0F1A2E"; GOLD="#B8860B"; IVORY="#F5F0E8"; SAGE="#4A6741"
CHARCOAL="#1C2B3A"; WARMGRAY="#6B6560"; TAUPE="#E2DDD5"

def font_face(family, fname, weight, style="normal"):
    path = os.path.join(FONT_DIR, fname)
    if not os.path.exists(path):
        return ""
    b64 = base64.b64encode(open(path,"rb").read()).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"font-style:{style};src:url(data:font/ttf;base64,{b64}) format('truetype');}}")

FONTS = "".join([
    font_face("Inter","Inter-Light.ttf",300),
    font_face("Inter","Inter-Regular.ttf",400),
    font_face("Inter","Inter-Medium.ttf",500),
    font_face("Playfair Display","PlayfairDisplay-Regular.ttf",400),
    font_face("Playfair Display","PlayfairDisplay-Bold.ttf",700),
])

def logo_inline():
    if os.path.exists(LOGO_SVG):
        return open(LOGO_SVG,encoding="utf-8").read()
    return "<strong>BridgeWorks</strong>"

# ---------- tiny markdown -> html ----------
def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t

def md_to_html(md, skip_to_rule=True):
    lines = md.split("\n")
    i = 0
    if skip_to_rule:
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1
    out=[]; tbl=[]; in_ul=False; in_ol=False

    def close_lists():
        nonlocal in_ul,in_ol
        if in_ul: out.append("</ul>"); in_ul=False
        if in_ol: out.append("</ol>"); in_ol=False

    def flush_tbl():
        if not tbl: return
        rows=[r for r in tbl if not re.match(r"^\|[\s:\-|]+\|?$", r.strip())]
        parsed=[[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
        if parsed:
            h="".join(f"<th>{inline(c)}</th>" for c in parsed[0])
            body="".join("<tr>"+"".join(f"<td>{inline(c)}</td>" for c in r)+"</tr>" for r in parsed[1:])
            out.append(f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>")
        tbl.clear()

    while i < len(lines):
        s=lines[i].rstrip(); st=s.strip()
        if st.startswith("|"):
            close_lists(); tbl.append(s); i+=1; continue
        else:
            flush_tbl()
        cm=re.match(r"^!\[chart:([a-z0-9-]+)\]$", st)
        if cm:
            close_lists()
            p=os.path.join(CHART_DIR, cm.group(1)+".png")
            if os.path.exists(p):
                b64=base64.b64encode(open(p,"rb").read()).decode()
                out.append(f'<div class="chart"><img src="data:image/png;base64,{b64}"/></div>')
            i+=1; continue
        if st=="---" or st=="":
            close_lists()
            i+=1; continue
        if st.startswith("### "):
            close_lists(); out.append(f"<h3>{inline(st[4:])}</h3>")
        elif st.startswith("## "):
            close_lists(); out.append(f"<h2>{inline(st[3:])}</h2>")
        elif st.startswith("# "):
            close_lists(); out.append(f"<h1>{inline(st[2:])}</h1>")
        elif st.startswith("> "):
            close_lists(); out.append(f"<blockquote>{inline(st[2:])}</blockquote>")
        elif re.match(r"^\d+\.\s", st):
            if not in_ol: close_lists(); out.append("<ol>"); in_ol=True
            out.append(f"<li>{inline(re.sub(r'^\d+\.\s','',st))}</li>")
        elif st.startswith("- "):
            if not in_ul: close_lists(); out.append("<ul>"); in_ul=True
            out.append(f"<li>{inline(st[2:])}</li>")
        elif st.startswith("*") and st.endswith("*") and not st.startswith("**"):
            close_lists(); out.append(f'<p class="meta">{inline(st.strip("*"))}</p>')
        else:
            close_lists(); out.append(f"<p>{inline(st)}</p>")
        i+=1
    close_lists(); flush_tbl()
    return "\n".join(out)

CSS = f"""
{FONTS}
@page {{ size: A4; margin: 22mm 20mm 20mm 20mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family:'Inter',sans-serif; font-weight:400; font-size:10.5pt;
  color:{CHARCOAL}; background:{IVORY}; line-height:1.6; margin:0; }}
.page {{ background:{IVORY}; }}
h1 {{ font-family:'Playfair Display',serif; font-weight:700; font-size:24pt;
  color:{NAVY}; margin:18pt 0 8pt; line-height:1.15; }}
h2 {{ font-family:'Playfair Display',serif; font-weight:700; font-size:16pt;
  color:{NAVY}; margin:20pt 0 4pt; padding-bottom:5pt;
  border-bottom:1.5pt solid {GOLD}; }}
h3 {{ font-family:'Inter',sans-serif; font-weight:500; font-size:11.5pt;
  color:{NAVY}; margin:12pt 0 4pt; letter-spacing:0.01em; }}
p {{ margin:0 0 7pt; }}
strong {{ font-weight:500; color:{NAVY}; }}
code {{ font-family:Consolas,monospace; font-size:9pt; background:#EDE7DC;
  padding:1px 4px; border-radius:3px; color:{CHARCOAL}; }}
ul,ol {{ margin:0 0 8pt; padding-left:18pt; }}
li {{ margin:0 0 3pt; }}
blockquote {{ margin:0 0 8pt; padding:6pt 12pt; border-left:3pt solid {GOLD};
  background:#EFE9DE; color:{WARMGRAY}; font-style:italic; }}
.meta {{ font-size:8.5pt; color:{WARMGRAY}; font-style:italic; }}
table {{ border-collapse:collapse; width:100%; margin:6pt 0 12pt; font-size:9pt; }}
th {{ background:{NAVY}; color:{IVORY}; font-weight:500; text-align:left;
  padding:6pt 8pt; }}
td {{ padding:5pt 8pt; border-bottom:0.5pt solid {TAUPE}; color:{CHARCOAL};
  vertical-align:top; }}
tbody tr:nth-child(even) {{ background:#EFE9DE; }}
.chart {{ text-align:center; margin:10pt 0 14pt; }}
.chart img {{ width:90%; max-width:520px; }}

/* Title page */
.cover {{ height:247mm; display:flex; flex-direction:column;
  justify-content:center; align-items:center; text-align:center;
  page-break-after:always; }}
.cover .logo {{ width:230px; margin-bottom:40pt; }}
.cover .label {{ font-family:'Inter'; font-weight:500; font-size:10pt;
  letter-spacing:0.18em; text-transform:uppercase; color:{GOLD};
  margin-bottom:10pt; }}
.cover h1.title {{ font-family:'Playfair Display'; font-weight:700;
  font-size:44pt; color:{NAVY}; margin:0; border:0; }}
.cover .subtitle {{ font-family:'Playfair Display'; font-weight:400;
  font-size:20pt; color:{CHARCOAL}; margin:6pt 0 22pt; }}
.cover .rule {{ width:120px; height:2pt; background:{GOLD}; margin:0 0 22pt; }}
.cover .who {{ font-size:11pt; color:{WARMGRAY}; line-height:1.8; }}
"""

def build(md_path, pdf_path, title, subtitle):
    md = open(md_path,encoding="utf-8").read()
    body = md_to_html(md)
    cover = f"""
    <div class="cover">
      <div class="logo">{logo_inline()}</div>
      <div class="label">Client Handover</div>
      <h1 class="title">{html.escape(title)}</h1>
      <div class="subtitle">{html.escape(subtitle)}</div>
      <div class="rule"></div>
      <div class="who">Prepared for Victor, CEEFM Kft<br/>Prepared by BridgeWorks<br/>May 29, 2026</div>
    </div>"""
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='page'>{cover}{body}</div></body></html>"
    html_path = pdf_path.replace(".pdf",".html")
    open(html_path,"w",encoding="utf-8").write(doc)

    footer = (f'<div style="font-family:Inter,sans-serif;font-size:7pt;color:{WARMGRAY};'
              'width:100%;text-align:center;">BridgeWorks &nbsp;·&nbsp; CEEFM Digital Growth Handover '
              '&nbsp;·&nbsp; <span class="pageNumber"></span></div>')
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(headless=True)
            pg = b.new_page()
            pg.goto("file:///"+html_path.replace("\\","/"), wait_until="networkidle")
            pg.pdf(path=pdf_path, format="A4", print_background=True,
                   display_header_footer=True, header_template="<div></div>",
                   footer_template=footer,
                   margin={"top":"22mm","bottom":"18mm","left":"20mm","right":"20mm"})
            b.close()
        print("PDF via Chromium:", pdf_path)
        return
    except Exception as e:
        print("Chromium failed, trying weasyprint:", e)
    from weasyprint import HTML
    HTML(html_path).write_pdf(pdf_path)
    print("PDF via weasyprint:", pdf_path)

if __name__ == "__main__":
    a = sys.argv
    md = a[1]; pdf = a[2]
    title = "CEEFM Kft"; subtitle = "Digital Growth Handover"
    if "--title" in a: title = a[a.index("--title")+1]
    if "--subtitle" in a: subtitle = a[a.index("--subtitle")+1]
    build(md, pdf, title, subtitle)
