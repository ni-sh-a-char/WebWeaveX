from __future__ import annotations

import re


def detect_monorepo(text: str):
    src = text or ""
    workspaces = sorted(set(re.findall(r"(?:packages/[\w\-./]+|workspace[s]?)", src, flags=re.IGNORECASE)))
    return {"workspaces": workspaces}

