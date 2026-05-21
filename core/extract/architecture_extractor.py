from __future__ import annotations

import re


ARCH_SECTIONS = ("architecture", "design", "flow", "components", "overview")


def extract_architecture(text: str) -> dict:
    src = text or ""
    lines = [line.strip() for line in src.splitlines() if line.strip()]
    matched = [ln for ln in lines if any(s in ln.lower() for s in ARCH_SECTIONS)]
    routes = sorted(set(re.findall(r"(?:GET|POST|PUT|PATCH|DELETE)\s+(/[A-Za-z0-9_\-/{}:]+)", src)))
    return {"sections": sorted(set(matched)), "api_routes": routes}

