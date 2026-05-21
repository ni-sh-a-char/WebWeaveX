from __future__ import annotations
import re

def extract_code_context(text: str):
    blocks = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)```", text or "", flags=re.DOTALL)
    return {
        "count": len(blocks),
        "languages": sorted({lang.lower() for lang, _ in blocks if lang}),
        "snippets": sorted({body.strip()[:200] for _, body in blocks if body.strip()}),
    }
