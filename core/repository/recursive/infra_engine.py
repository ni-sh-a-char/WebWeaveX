from __future__ import annotations


def extract_infra(text: str):
    src = (text or "").lower()
    out = [k for k in ("terraform", "kubernetes", "helm", "docker") if k in src]
    return {"infra_stack": sorted(set(out))}

