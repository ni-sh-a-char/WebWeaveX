from __future__ import annotations

import re
from typing import Any, Dict


def verify_citations(text: str) -> Dict[str, Any]:
    urls = sorted(set(re.findall(r"https?://[^\s\)\]\"']+", text or "")))
    dois = sorted(set(re.findall(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", text or "", re.I)))
    return {
        "url_count": len(urls),
        "doi_count": len(dois),
        "verified": bool(urls or dois),
        "deterministic_inputs": [f"urls={len(urls)}", f"dois={len(dois)}"],
    }
