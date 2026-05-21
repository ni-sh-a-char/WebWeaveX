from __future__ import annotations

import re


def extract_code_features(text: str) -> dict:
    src = text or ""
    imports = sorted(set(re.findall(r"^\s*(?:import|from)\s+([A-Za-z0-9_\.]+)", src, flags=re.MULTILINE)))
    exports = sorted(set(re.findall(r"^\s*export\s+(?:default\s+)?(?:const|class|function)?\s*([A-Za-z0-9_]+)?", src, flags=re.MULTILINE)))
    return {"imports": imports, "exports": [e for e in exports if e]}

