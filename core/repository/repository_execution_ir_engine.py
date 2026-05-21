from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.repository.api_contract_reasoning_engine import reason_api_contract
from core.repository.deployment_semantics_engine import analyze_deployment_semantics
from core.repository.repository_semantic_ir_engine import build_repository_semantic_ir
from core.repository.runtime_flow_reasoner import reason_runtime_flow
from core.repository.service_runtime_graph_engine import build_service_runtime_graph


def build_repository_execution_ir(
    source: str,
    path: str = "",
    files: Optional[List[str]] = None,
    openapi_spec: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    base = build_repository_semantic_ir(source, path, files)
    flow = reason_runtime_flow(source, path, files)
    services = build_service_runtime_graph(source, path, files)
    deploy = analyze_deployment_semantics(files or [])
    api = reason_api_contract(openapi_spec or {}) if openapi_spec else {}
    return {
        **base,
        "execution": flow,
        "services": services,
        "deployment": deploy,
        "api_contracts": api,
        "evidence": sorted(
            {str(e) for e in (list(base.get("evidence") or []) + list(flow.get("evidence") or [])) if e}
        ),
    }
