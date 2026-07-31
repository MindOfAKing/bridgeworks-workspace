# MarkItDown pilot

Date: 2026-07-25  
Pinned source: `microsoft/markitdown@2e42a01c404629b06892a1bdb5e7bf5261770c40`  
Installed version: `0.1.6`  
Licence: MIT  
Environment: `skill-governance/.venv-markitdown` with PDF, DOCX, PPTX, and XLSX extras  
Plugins, cloud services, LLM vision, and repeated OCR: disabled

## Decision

Use MarkItDown as an optional text-first preprocessor for selected text-heavy PDF and DOCX work. It may also create a first-pass table view for simple XLSX files.

Do not make it the default for visually meaningful PDFs, presentations, spreadsheets, diagrams, images, or scanned documents. Keep visual or native-format inspection as the approval gate.

## Samples and measurements

The five copied pilot samples contain public academic material or BridgeWorks-owned public-facing templates and visuals. The copies and conversions stay in ignored local folders.

| Sample | Native evidence | Markdown result | Time | Approximate token change | Main failure mode |
|---|---|---:|---:|---:|---|
| Text-heavy PDF | 40 pages | 92,123 characters | 11.315 s | 271,772 to 23,031, about 91.5% lower | Reading order was usable, but headings and page structure were weak |
| Structured DOCX | 318 paragraphs, 1 table, 2 images, 13 hyperlinks | 26,019 characters | 2.791 s | 35,434 to 6,505, about 81.6% lower | Visual hierarchy became bold text; image meaning was not evaluated |
| Branded PPTX | 6 slides, 25 text runs, 1 image | 1,088 characters | 2.380 s | 8,600 to 272, about 96.8% lower | Slide order and text survived, but layout, colour, spatial meaning, and brand treatment did not |
| Meaningful XLSX | 2 sheets, 1,493 cells, no formulas | 63,816 characters | 2.502 s | 5,485 to 15,954, about 191% higher | Tables were readable but verbose; cell types, sheet behaviour, and visual structure need native inspection |
| Visual PNG | 1200 by 630 RGB | 0 characters | 2.008 s | Apparent 100% reduction is total information loss | No useful extraction without OCR or vision |

Token figures are rough source-byte or Markdown-character counts divided by four. Binary source size is not a true token count, so the figures show direction only.

## Quality comparison

### Text-heavy PDF

- Extraction completeness: good for running text in the inspected opening and references.
- Headings and paragraphs: paragraphs survived; semantic heading markers were inconsistent.
- Tables: not a defining feature of this sample.
- Links and metadata: publication metadata appeared in text; native PDF metadata keys were not converted into a useful front matter block.
- Visual loss: page design, spacing, and figures require native inspection.
- Suitability: useful first pass for `pdf`, `client-audit`, `market-*`, and `geo-*` when the file is digitally generated and text-led.

### DOCX

- Extraction completeness: good for the inspected headings, paragraphs, bullets, and links.
- Heading preservation: visual bold text often replaced semantic heading levels.
- Table quality: the single table requires spot-checking against Word.
- Link preservation: hyperlinks were preserved.
- Metadata usefulness: limited.
- Visual loss: two embedded images and page-level layout cannot be approved from Markdown.
- Suitability: strong optional intake layer for `docx`, proposal review, and evidence extraction. Keep native or rendered review for deliverables.

### PPTX

- Extraction completeness: all six slide markers and the inspected slide text appeared.
- Heading preservation: slide titles were useful.
- Visual loss: severe. Colour, spacing, position, logo treatment, and emphasis were lost.
- Suitability: useful for transcript-like review or search. Not suitable for design, narrative hierarchy, brand review, or final approval.

### XLSX

- Extraction completeness: both sheets produced table-like Markdown and the inspected public indicator rows were readable.
- Table quality: readable for lookup, but the output expanded to almost three times the rough source token estimate.
- Native behaviour: cell types, formulas, validation, hidden sheets, charts, and formatting must be checked in the workbook. This sample had no formulas or drawings.
- Suitability: selective use for small, flat tables. Do not use as the default for analytical, financial, dashboard, or client workbooks.

### PNG

- Extraction completeness: none.
- Suitability: rejected without an explicit, approved OCR or vision path. Do not run OCR repeatedly.

## Failure handling

`markitdown_pilot.py` returns a non-zero exit code when the isolated CLI is missing or any conversion fails. Outputs go to an ignored folder. The runner does not fetch remote URLs, enable plugins, call an LLM, or replace native tools.

## Recommendation by workflow

- `docx`: optional text-first extraction, then native/rendered review.
- `pdf`: optional for digital, text-heavy files. Keep page render inspection for visual or scanned files.
- `client-audit`: useful for rapid evidence indexing, not for visual audit conclusions.
- `market-*`: useful for long reports and text sources.
- `geo-*`: useful for extracting explicit claims, links, headings, and tables. Do not infer schema, visual hierarchy, or page UX from Markdown alone.
- PPTX, XLSX, diagrams, scanned documents, and image-heavy files: native and visual inspection remain required.
