from __future__ import annotations

from typing import Any, Dict, List

from core.repository.deployment_semantics_engine import analyze_deployment_semantics


def model_deployment_causality(files: List[str]) -> Dict[str, Any]:
    deploy = analyze_deployment_semantics(files)
    causal = [
        {"artifact": a, "causes": "deploy"}
        for a in deploy.get("deployment_artifacts", [])[:30]
    ]
    return {"causal": causal, "semantics": deploy.get("semantics"), "evidence": deploy.get("infra", {}).get("evidence", [])}
