from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.ir._base import empty_confidence, empty_lineage, merge_evidence
from core.ast import compile_semantic_ast_ir
from core.repository.repository_execution_ir_engine import build_repository_execution_ir

RepositoryIR = Dict[str, Any]


def empty_repository_ir() -> RepositoryIR:
    return {
        "services": [],
        "runtimes": [],
        "dependencies": [],
        "events": [],
        "queues": [],
        "apis": [],
        "deployments": [],
        "infra": [],
        "execution_flows": [],
        "topology": [],
        "runtime_constraints": [],
        "semantic_evidence": {},
        "graph": {},
        "lineage": empty_lineage("repository_ir"),
        "confidence": empty_confidence(),
    }


def compile_repository_ir(
    source: str = "",
    path: str = "",
    files: Optional[List[str]] = None,
    openapi_spec: Optional[Dict[str, Any]] = None,
) -> RepositoryIR:
    raw = build_repository_execution_ir(source, path, files, openapi_spec)
    deps = raw.get("runtime_dependencies", {}) or {}
    flow = raw.get("execution", {}) or {}
    services = raw.get("services", {}) or {}
    deploy = raw.get("deployment", {}) or {}
    api = raw.get("api_contracts", {}) or {}
    ir = empty_repository_ir()
    ir["dependencies"] = deps.get("dependencies", [])
    ir["runtimes"] = [{"language": raw.get("language", "text"), "evidence": deps.get("evidence", [])}]
    ir["execution_flows"] = flow.get("execution_flow", {}).get("flow", [])
    ir["services"] = services.get("nodes", [])
    ir["topology"] = flow.get("topology", {}).get("edges", [])
    ir["deployments"] = deploy.get("deployment_artifacts", [])
    ir["infra"] = [s.get("file") for s in deploy.get("infra", {}).get("signals", []) if isinstance(s, dict)]
    ir["apis"] = api.get("contracts", [])
    ir["graph"] = {"nodes": services.get("nodes", []), "edges": services.get("edges", [])}
    ir["semantic_evidence"] = merge_evidence(raw.get("evidence", []))
    ir["lineage"] = empty_lineage("repository_execution_ir")
    ir["confidence"] = {"score": 0.8 if deps.get("parser_first") else 0.4, "basis": raw.get("evidence", []), "deterministic": True}
    try:
        semantic_ast = compile_semantic_ast_ir(source or "")
    except SyntaxError:
        semantic_ast = {"semantic_grounded": False, "deterministic": True}
    ir["semantic_ast"] = semantic_ast
    ir["_raw"] = raw
    return ir
