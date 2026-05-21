from __future__ import annotations

from typing import Any, Dict, List


_INFRA_MARKERS = (
    "docker-compose",
    "Dockerfile",
    "kubernetes",
    "k8s/",
    "deployment.yaml",
    "helm/",
    ".github/workflows",
    "terraform",
    "pulumi",
)


def detect_infra_signals(files: List[str]) -> Dict[str, Any]:
    signals = []
    for f in files or []:
        fl = f.replace("\\", "/").lower()
        for m in _INFRA_MARKERS:
            if m.lower() in fl:
                signals.append({"file": f, "signal": m})
                break
    return {
        "signals": signals,
        "evidence": [f"infra:{s['signal']}" for s in signals],
        "deterministic_inputs": [f"signals={len(signals)}"],
    }
