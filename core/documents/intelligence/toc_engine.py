from __future__ import annotations
from core.documents.heading_engine import extract_headings

def build_toc(text: str):
    heads=extract_headings(text).get('headings',[])
    return {"toc": [{"title":h.get("title",""),"level":h.get("level",1)} for h in heads]}
