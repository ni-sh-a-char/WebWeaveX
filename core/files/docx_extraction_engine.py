from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from core.documents.universal_document_extraction_engine import (
    extract_document_runtime,
)

try:
    from docx import Document
except Exception:
    Document = None

MAX_PARAGRAPHS = 10000


def _with_document_runtime(payload: Dict[str, Any]) -> Dict[str, Any]:
    text = payload.get("text", "")
    payload["document_runtime"] = extract_document_runtime(text)
    return payload


def extract_docx_text(path: str) -> Dict[str, Any]:
    if Document is None:
        return _with_document_runtime({
            "available": False,
            "text": "",
            "reason": "python_docx_missing",
            "bounded": True,
        })

    if not Path(path).is_file():
        return _with_document_runtime({
            "available": False,
            "text": "",
            "reason": "file_not_found",
            "bounded": True,
        })

    try:
        document = Document(path)
    except Exception as exc:
        return _with_document_runtime({
            "available": False,
            "text": "",
            "reason": str(exc)[:200],
            "bounded": True,
        })

    paragraphs = []

    for para in document.paragraphs[:MAX_PARAGRAPHS]:
        text = para.text.strip()

        if text:
            paragraphs.append(text[:10000])

    return _with_document_runtime({
        "available": True,
        "paragraphs": paragraphs,
        "text": "\n".join(paragraphs),
        "bounded": True,
    })
