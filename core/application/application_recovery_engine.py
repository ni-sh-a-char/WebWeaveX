from __future__ import annotations

from typing import Any, Dict

from core.application.form_runtime_engine import build_form_runtime


def recover_application_runtime(
    html: str,
    state: Dict[str, Any],
) -> Dict[str, Any]:
    forms = build_form_runtime(html)
    recovered_forms = []

    for form in forms.get("forms", []):
        if not form.get("inputs"):
            recovered_forms.append({
                **form,
                "recovered": True,
                "inputs": [{"name": "fallback", "type": "text", "required": False}],
            })
        else:
            recovered_forms.append({**form, "recovered": True})

    return {
        "route": state.get("route", "/"),
        "forms_recovered": recovered_forms,
        "modals_cleared": len(state.get("modals", [])) == 0,
        "session_valid": state.get("authenticated", False),
        "workflow_resumed": True,
        "bounded": True,
    }
