from __future__ import annotations

import re


def extract_semantic_examples(text: str):
    source = text or ""
    fenced = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)```", source, flags=re.DOTALL)
    return {
        "count": len(fenced),
        "languages": sorted({lang.lower() for lang, _ in fenced if lang}),
        "snippets": sorted({snippet.strip()[:200] for _, snippet in fenced if snippet.strip()}),
    }
