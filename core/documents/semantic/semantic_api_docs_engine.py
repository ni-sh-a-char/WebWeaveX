from __future__ import annotations

import re


def extract_semantic_api_docs(text: str):
    source = text or ""
    endpoints = sorted(set(re.findall(r"`(GET|POST|PUT|DELETE|PATCH)\s+([^`]+)`", source)))
    params = sorted(set(re.findall(r"\b(?:param|query|path|body)\s*:\s*([A-Za-z_][A-Za-z0-9_]*)", source, flags=re.IGNORECASE)))
    return {
        "endpoints": [{"method": m, "path": p.strip()} for m, p in endpoints],
        "parameters": params,
    }
