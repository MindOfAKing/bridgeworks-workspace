# Local-to-Drive Reconciliation Manifest

Compares the local Content Studio mirror
(`C:/Users/User/Projects/BridgeWorks-Content-Studio`) against the canonical
Drive Content Studio folder (`1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY`). Per
operations/cross-model-content-cycle-runbook.md's source-of-truth
hierarchy: Drive is canonical, local is the mirror.

Run this comparison periodically (manually, until an automated version
exists) and log the result below. Do not silently assume the mirror
matches Drive.

## Method

1. List the local top-level folder structure (00-09, 99_Superseded,
   README.md).
2. List the Drive folder's top-level contents via the Drive connector
   (`search_files` with `parentId = '<drive-folder-id>'`).
3. Compare folder names and top-level file presence. For a deeper check,
   compare `00_Project_Core/CONTEXT-MANIFEST.csv` (local file hashes)
   against Drive file metadata and modified times.
4. Log any drift below with the date it was found.

## Run log

### 2026-07-22 (Claude Code Desktop, content-system audit)

Local top-level: `00_Project_Core`, `01_Brand_Context`,
`02_Strategy_And_Messaging`, `03_Inspiration_Research`,
`04_Content_Briefs`, `05_Source_Media`, `06_Production`,
`07_Review_And_Approval`, `08_Approved_Masters`,
`09_Performance_And_Learning`, `99_Superseded`, `README.md`.

Drive top-level (folder `1W7Nw2xn1Yta-SH5jGXZlTaZELdOREclY`): identical
set, `00_Project_Core` through `09_Performance_And_Learning`,
`99_Superseded`, `README.md`. All created 2026-07-16, consistent with the
local mirror's creation date.

Result: in sync at the top level. `07_Review_And_Approval`,
`08_Approved_Masters`, and `09_Performance_And_Learning` contain only a
README.md on both sides (no approved masters, review records, or
performance data yet on either side). Not checked in this pass: byte-level
contents of `01`-`06` beyond what `CONTEXT-MANIFEST.csv` already hashes
locally, and `99_Superseded` (excluded, it is explicitly archival).

Next check due: whenever new content moves through the pipeline, or at
the next full content-system audit.
