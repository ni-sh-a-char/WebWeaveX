from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.documents.universal_document_extraction_engine import (
    extract_document_runtime,
)

try:
    import pypdf
except Exception:
    pypdf = None

MAX_PAGES = 1000


def _with_document_runtime(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("text", "")
    payload["document_runtime"] = extract_document_runtime(text)
    return payload


def extract_pdf_text(path: str) -> Dict[str, Any]:
    if pypdf is None:
        return _with_document_runtime({
            "text": "",
            "pages": [],
            "available": False,
            "reason": "pypdf_not_installed",
            "bounded": True,
        })

    if not Path(path).is_file():
        return _with_document_runtime({
            "text": "",
            "pages": [],
            "available": False,
            "reason": "file_not_found",
            "bounded": True,
        })

    try:
        reader = pypdf.PdfReader(path)
    except Exception as exc:
        return _with_document_runtime({
            "text": "",
            "pages": [],
            "available": False,
            "reason": str(exc)[:200],
            "bounded": True,
        })

    pages = []

    for index, page in enumerate(reader.pages[:MAX_PAGES]):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""

        pages.append({
            "page": index,
            "text": text[:50000],
        })

    full_text = "\n".join(
        p["text"] for p in pages
    )

    extracted_text = full_text[:5_000_000]

    return _with_document_runtime({
        "available": True,
        "page_count": len(pages),
        "pages": pages,
        "text": extracted_text,
        "bounded": True,
    })
