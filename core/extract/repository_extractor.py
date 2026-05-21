from __future__ import annotations

import re


def extract_repository_data(text: str, source_url: str = "") -> dict:
    src = text or ""
    tree_lines = [ln.strip() for ln in src.splitlines() if "/" in ln or "." in ln]
    readme_sections = sorted(set(re.findall(r"^#{1,6}\s+(.+)$", src, flags=re.MULTILINE)))
    return {
        "repository": {"source": source_url, "structure_hints": sorted(set(tree_lines))[:200]},
        "readme": {"sections": readme_sections},
    }

