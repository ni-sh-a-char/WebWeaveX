from __future__ import annotations

from typing import Any, Dict, Optional


def reconstruct_application_runtime(
    application_ir: Optional[Dict[str, Any]] = None,
    workflow_ir: Optional[Dict[str, Any]] = None,
    execution_ir: Optional[Dict[str, Any]] = None,
    runtime_type: str = "browser",
) -> Dict[str, Any]:
    application_ir = application_ir or {}
    workflow_ir = workflow_ir or {}
    execution_ir = execution_ir or {}

    workflows = workflow_ir.get("workflows", workflow_ir.get("workflow", {}))
    if isinstance(workflows, dict) and "objective" in workflows:
        workflows = [workflows]

    return {
        "runtime_type": runtime_type,
        "workflows": list(workflows) if isinstance(workflows, list) else [],
        "forms": dict(application_ir.get("forms", {})),
        "dashboards": list(application_ir.get("dashboards", [])),
        "modals": list(application_ir.get("modals", [])),
        "tabs": list(application_ir.get("tabs", [])),
        "application_graph": dict(application_ir.get("graph", application_ir.get("action_graphs", {}))),
        "execution_state": dict(execution_ir.get("execution_state", execution_ir.get("state", {}))),
        "replay_safe": True,
        "bounded": True,
    }
