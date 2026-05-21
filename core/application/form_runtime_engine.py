from __future__ import annotations

from typing import Any, Dict, List

from bs4 import BeautifulSoup

MAX_FORMS = 500


def build_form_runtime(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html or "", "html.parser")
    forms: List[Dict[str, Any]] = []

    for form in soup.find_all("form")[:MAX_FORMS]:
        inputs: List[Dict[str, Any]] = []

        for field in form.find_all(["input", "select", "textarea"]):
            inputs.append({
                "name": str(field.get("name", ""))[:200],
                "type": str(field.get("type", field.name))[:50],
                "required": field.has_attr("required"),
            })

        csrf_fields = [
            inp.get("name", "")
            for inp in form.find_all("input")
            if "csrf" in str(inp.get("name", "")).lower()
        ]

        forms.append({
            "action": str(form.get("action", ""))[:500],
            "inputs": sorted(inputs, key=lambda item: item["name"]),
            "csrf_fields": sorted(csrf_fields),
            "multi_step": len(form.find_all("fieldset")) > 1,
            "bounded": True,
        })

    return {
        "forms": forms,
        "form_count": len(forms),
        "bounded": True,
    }
