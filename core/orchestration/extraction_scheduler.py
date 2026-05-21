from __future__ import annotations


def schedule(plan: dict):
    return {"scheduled": list(plan.get("extraction_order", []))}

