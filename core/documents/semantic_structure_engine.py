from __future__ import annotations

import re
from typing import Dict, Any


def extract_structural_blocks(text: str) -> Dict[str, Any]:
    src = text or ""
    code_blocks = re.findall(r"```[\w-]*\n(.*?)```", src, flags=re.DOTALL)
    tables = re.findall(r"^\|.*\|$", src, flags=re.MULTILINE)
    lists = re.findall(r"^\s*(?:-|\*|\d+\.)\s+.+$", src, flags=re.MULTILINE)
    configs = re.findall(r"(?:package\.json|pyproject\.toml|requirements\.txt|pubspec\.yaml|Cargo\.toml)", src)
    examples = re.findall(r"(?:^|\n)\s*(?:>>>|\$)\s+.+", src)
    return {"code_blocks": sorted([c.strip() for c in code_blocks if c.strip()]), "tables": sorted(set(tables)), "lists": sorted(set(lists)), "examples": sorted(set(examples)), "configs": sorted(set(configs))}
