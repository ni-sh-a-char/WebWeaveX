from __future__ import annotations

from core.documents.document_intelligence import analyze_document


def extract_docs_v2(text: str):
    return analyze_document(text)
