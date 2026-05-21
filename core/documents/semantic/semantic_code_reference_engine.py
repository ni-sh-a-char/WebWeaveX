from __future__ import annotations

import re


def extract_semantic_code_references(text: str):
    source = text or ""
    inline = sorted(set(re.findall(r"`([^`]+)`", source)))
    symbols = sorted({i for i in inline if "(" in i or "." in i or "/" in i})
    return {"inline": inline, "symbols": symbols}
