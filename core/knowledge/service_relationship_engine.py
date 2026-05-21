from __future__ import annotations


def build_service_relationships(services: list):
    ordered = sorted(set(services or []))
    edges = [{"from": "service", "to": s} for s in ordered]
    return {"nodes": ["service"] + ordered, "edges": edges}
