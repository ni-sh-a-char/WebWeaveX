from __future__ import annotations
from core.documents.reference_engine import extract_references

def extract_cross_refs(text: str):
    refs=extract_references(text)
    return {"cross_links": sorted(set(refs.get("internal_links",[]) + refs.get("repo_references",[])))}
