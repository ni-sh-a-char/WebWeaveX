from __future__ import annotations


def strategy_for(url: str):
    u = (url or "").lower()
    if "github.com" in u:
        return {"mode": "repository"}
    if "docs" in u:
        return {"mode": "documentation"}
    return {"mode": "web"}

