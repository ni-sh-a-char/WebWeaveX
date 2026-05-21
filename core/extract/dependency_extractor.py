from __future__ import annotations

import json
import re
from typing import Dict, Any


def extract_dependencies(text: str) -> Dict[str, Any]:
    src = text or ""
    deps = sorted(set(re.findall(r"(?:pip install|npm i|npm install)\s+([A-Za-z0-9_\-\.@/]+)", src)))
    try:
        data = json.loads(src)
    except Exception:
        data = {}
    if isinstance(data, dict):
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            section = data.get(key, {})
            if isinstance(section, dict):
                deps.extend(section.keys())
    return {"packages": sorted(set(deps))}

