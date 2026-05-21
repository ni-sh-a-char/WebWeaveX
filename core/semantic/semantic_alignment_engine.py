from __future__ import annotations

from typing import Any, Dict, Optional


def align_semantic_runtimes(
    browser: Optional[Dict[str, Any]] = None,
    native: Optional[Dict[str, Any]] = None,
    repository: Optional[Dict[str, Any]] = None,
    document: Optional[Dict[str, Any]] = None,
    multimodal: Optional[Dict[str, Any]] = None,
    runtime: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    layers = {
        "browser": browser or {},
        "native": native or {},
        "repository": repository or {},
        "document": document or {},
        "multimodal": multimodal or {},
        "runtime": runtime or {},
    }

    aligned_domains = []
    for name, payload in layers.items():
        if payload:
            aligned_domains.append({
                "layer": name,
                "domain": payload.get("domain", payload.get("primary_kind", "")),
            })

    return {
        "layers": layers,
        "aligned_domains": aligned_domains,
        "aligned": True,
        "bounded": True,
    }
