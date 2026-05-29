# Convert a .docx (or .md-derived .docx) to PDF using LibreOffice.
# Usage: powershell -File to-pdf.ps1 "C:\path\to\file.docx"
param([Parameter(Mandatory=$true)][string]$DocxPath)

$soffice = "C:\Program Files\LibreOffice\program\soffice.exe"
if (-not (Test-Path $soffice)) { Write-Error "LibreOffice not found at $soffice"; exit 1 }
if (-not (Test-Path $DocxPath)) { Write-Error "File not found: $DocxPath"; exit 1 }

$dir = Split-Path -Parent $DocxPath
& $soffice --headless --convert-to pdf --outdir $dir $DocxPath 2>$null
$pdf = [System.IO.Path]::ChangeExtension($DocxPath, ".pdf")
if (Test-Path $pdf) { Write-Output "PDF created: $pdf" } else { Write-Error "PDF conversion failed"; exit 1 }
