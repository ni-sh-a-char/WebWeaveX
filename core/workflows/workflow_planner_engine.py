from __future__ import annotations

from typing import Any, Dict, Optional

from core.workflows.objective_engine import build_runtime_objective


def build_workflow_plan(
    objective: str,
    semantic_runtime: Optional[Dict[str, Any]] = None,
    causality: Optional[Dict[str, Any]] = None,
    application_runtime: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    runtime_objective = build_runtime_objective(objective)
    semantic_runtime = semantic_runtime or {}
    domain = semantic_runtime.get("domain", {}).get("domain", "saas")

    plan_steps = []
    for index, step in enumerate(runtime_objective["steps"]):
        plan_steps.append({
            "id": f"step:{index}",
            "action": step,
            "runtime": _runtime_for_step(step, domain),
            "depends_on": f"step:{index - 1}" if index > 0 else "",
        })

    if application_runtime:
        workflow = application_runtime.get("workflow", {})
        for edge in workflow.get("edges", [])[:100]:
            plan_steps.append({
                "id": f"app:{len(plan_steps)}",
                "action": str(edge.get("relation", "transition")),
                "runtime": "application",
                "depends_on": plan_steps[-1]["id"] if plan_steps else "",
            })

    if causality:
        inner = causality.get("causality", causality)
        for handoff in inner.get("propagation", {}).get("handoffs", [])[:50]:
            plan_steps.append({
                "id": f"causal:{len(plan_steps)}",
                "action": "cross_runtime_handoff",
                "runtime": str(handoff.get("to", "native")),
                "depends_on": plan_steps[-1]["id"] if plan_steps else "",
            })

    return {
        "objective": objective,
        "domain": domain,
        "steps": plan_steps,
        "bounded": True,
    }


def _runtime_for_step(step: str, domain: str) -> str:
    if "terminal" in step:
        return "terminal"
    if "repository" in step or "api" in step:
        return "repository"
    if "infra" in step or domain == "infrastructure":
        return "native"
    if "notification" in step:
        return "desktop"
    return "browser"
