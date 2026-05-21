from __future__ import annotations

from typing import Any, Dict, Optional


def extract_application_semantics(
    application_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    application_result = application_result or {}
    workflow = application_result.get("workflow", {})
    execution = application_result.get("execution", {})
    forms = application_result.get("forms", {})

    return {
        "workflow_purpose": str(application_result.get("intent", {}).get("intent", "operate")),
        "runtime_intent": str(execution.get("objective", "")),
        "business_operations": [
            str(step.get("action", ""))
            for step in execution.get("executed", [])
        ],
        "ui_functionality": list(application_result.get("ui_semantics", {}).keys()),
        "operational_actions": len(workflow.get("edges", [])),
        "form_operations": len(forms.get("forms", [])),
        "bounded": True,
    }
