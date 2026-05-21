from __future__ import annotations

def resolve_conflicts(values: list[str]):
    uniq = sorted(set(values or []))
    return {"resolved": uniq, "conflicts": max(0, len(values or []) - len(uniq))}
