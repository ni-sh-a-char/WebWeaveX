from __future__ import annotations

import re


def extract_semantic_specs(text: str):
    source = text or ""
    rfc = sorted(set(re.findall(r"\bRFC\s*-?\s*(\d+)\b", source, flags=re.IGNORECASE)))
    versioned = sorted(set(re.findall(r"\bv\d+(?:\.\d+){0,2}\b", source)))
    keywords = []
    for kw in ["MUST", "SHOULD", "MAY", "REQUIRED", "OPTIONAL"]:
        if re.search(rf"\b{kw}\b", source):
            keywords.append(kw)
    return {"rfc": rfc, "versions": versioned, "normative_keywords": sorted(keywords)}
