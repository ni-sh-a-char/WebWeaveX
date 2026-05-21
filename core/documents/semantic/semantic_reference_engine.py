from __future__ import annotations

import re


def extract_semantic_references(text: str):
    source = text or ""
    links = sorted(set(re.findall(r"https?://[^\s)\]>'\"]+", source)))
    anchors = sorted(set(re.findall(r"\[[^\]]+\]\((#[^)]+)\)", source)))
    citations = sorted(set(re.findall(r"\[(\d+)\]", source)))
    return {"external": links, "anchors": anchors, "citations": citations}
