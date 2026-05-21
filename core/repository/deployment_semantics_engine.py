from __future__ import annotations

from typing import Any, Dict, List

from core.repository.infra_relationship_engine import model_infra_relationships


def analyze_deployment_semantics(files: List[str]) -> Dict[str, Any]:
    infra = model_infra_relationships(files)
    deploy_files = [f for f in files if any(k in f.replace("\\", "/").lower() for k in ("docker", "k8s", "helm", "deploy", "workflow"))]
    return {
        "deployment_artifacts": deploy_files,
        "infra": infra,
        "semantics": "container_orchestration" if deploy_files else "unknown",
        "evidence": infra.get("evidence", []) + [f"deploy:{len(deploy_files)}"],
    }
