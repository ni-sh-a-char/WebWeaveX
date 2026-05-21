from __future__ import annotations
from core.documents.reference_engine import extract_references

def extract_citations(text: str):
    refs=extract_references(text)
    return {"citations": refs.get("citations", [])}
