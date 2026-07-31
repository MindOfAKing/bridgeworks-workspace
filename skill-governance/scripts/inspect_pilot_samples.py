#!/usr/bin/env python3
"""Collect native-structure evidence for the MarkItDown pilot samples."""

from __future__ import annotations

import argparse
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image
from pypdf import PdfReader

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}


def xml_count(archive: zipfile.ZipFile, name: str, query: str, ns: dict) -> int:
    return len(ET.fromstring(archive.read(name)).findall(query, ns))


def inspect(path: Path, kind: str) -> dict:
    result = {"path": str(path), "format": kind, "bytes": path.stat().st_size}
    if kind == "pdf":
        reader = PdfReader(path)
        result.update(pages=len(reader.pages), metadata_keys=sorted((reader.metadata or {}).keys()))
    elif kind == "docx":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            result.update(
                paragraphs=xml_count(archive, "word/document.xml", ".//w:p", NS),
                tables=xml_count(archive, "word/document.xml", ".//w:tbl", NS),
                images=len([n for n in names if n.startswith("word/media/")]),
                hyperlinks=xml_count(archive, "word/document.xml", ".//w:hyperlink", NS),
            )
    elif kind == "pptx":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            slides = [n for n in names if n.startswith("ppt/slides/slide") and n.endswith(".xml")]
            text_runs = sum(xml_count(archive, n, ".//a:t", NS) for n in slides)
            result.update(
                slides=len(slides),
                text_runs=text_runs,
                images=len([n for n in names if n.startswith("ppt/media/")]),
                charts=len([n for n in names if n.startswith("ppt/charts/chart") and n.endswith(".xml")]),
            )
    elif kind == "xlsx":
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            sheets = [n for n in names if n.startswith("xl/worksheets/sheet") and n.endswith(".xml")]
            result.update(
                sheets=len(sheets),
                cells=sum(xml_count(archive, n, ".//s:c", NS) for n in sheets),
                formulas=sum(xml_count(archive, n, ".//s:f", NS) for n in sheets),
                tables=len([n for n in names if n.startswith("xl/tables/table") and n.endswith(".xml")]),
                drawings=len([n for n in names if n.startswith("xl/drawings/drawing") and n.endswith(".xml")]),
            )
    elif kind == "png":
        with Image.open(path) as image:
            result.update(width=image.width, height=image.height, mode=image.mode, metadata_keys=sorted(image.info.keys()))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    results = [inspect(Path(item["path"]), item["format"]) for item in manifest["samples"]]
    args.output.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
