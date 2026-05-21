from __future__ import annotations

def resolve_entities(items: list[str]):
    vals=sorted(set((x or '').strip().lower() for x in items or [] if x))
    return {"entities": vals}
