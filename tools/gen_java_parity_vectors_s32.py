#!/usr/bin/env python3
"""Session-32 cross-language golden vectors from canonical Python 2.1.0 (no-OCR contract).

    python tools/gen_java_parity_vectors_s32.py <out.json>

Covers the OCR cluster under the canonical cross-language contract — OCR runtime treated ABSENT
(exactly as the JavaScript port hardcodes `pytesseract = null` in src/ocr/ocrEngine.ts, and as the
canonical cross-language vectors are generated). Under this contract extract_ocr returns
`ocr_dependencies_missing`, every downstream multimodal engine operates on empty regions, and the
output is fully deterministic and language-portable:
  - extract_multimodal(path)
  - ingest_input(path)
"""
from __future__ import annotations

import json
import sys

import core.ocr.ocr_engine as oe
oe.pytesseract = None  # canonical no-OCR contract (mirrors JS hardcoded null)
oe.Image = None

from core.crypto.kaalka_hash_engine import compute_kaalka_hash
from core.determinism.normalization import stable_serialize
from core.multimodal.universal_multimodal_extraction_engine import extract_multimodal
from core.ingestion.universal_ingestion_engine import ingest_input, detect_input_type


def ev(name, inputs, value):
    return {"name": name, "inputs": inputs,
            "serialized": stable_serialize(value), "hash": compute_kaalka_hash(value)}


def main() -> None:
    out = {"source": "Python 2.1.0 canonical (session 32: OCR cluster, no-OCR contract)"}

    out["extract_multimodal"] = [
        ev("png", {"path": "x.png"}, extract_multimodal("x.png")),
        ev("nested", {"path": "/a/b/photo.jpeg"}, extract_multimodal("/a/b/photo.jpeg")),
    ]

    paths = ["photo.jpg", "scan.png", "doc.pdf", "report.docx", "data.csv",
             "config.json", "page.html", "notes.txt", "readme.md", "mod.py",
             "bundle.zip", "weird.xyz", "noext", "https://a.com/p", ".hidden", "trailing."]
    out["ingest_input"] = [ev(p or "empty", {"path": p}, ingest_input(p)) for p in paths]

    out["detect_input_type"] = [ev(p or "empty", {"path": p}, detect_input_type(p)) for p in paths]

    path = sys.argv[1] if len(sys.argv) > 1 else "golden_vectors_s32.json"
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    total = sum(len(v) for k, v in out.items() if isinstance(v, list))
    print(f"wrote {path} ({total} vectors)")


if __name__ == "__main__":
    main()
