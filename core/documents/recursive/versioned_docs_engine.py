from __future__ import annotations

import re


def detect_versions(text: str):
    versions = sorted(set(re.findall(r"\b(v?\d+\.\d+(?:\.\d+)?)\b", text or "")))
    return {"versions": versions}

