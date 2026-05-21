from __future__ import annotations

import re
from typing import Any, Dict, List, Optional


def extract_repository_semantics(
    files: Optional[List[str]] = None,
    text: str = "",
) -> Dict[str, Any]:
    files = files or []
    combined = f"{text} {' '.join(files)}"

    roles = []
    if re.search(r"api|routes|controller", combined, re.I):
        roles.append("api_surface")
    if re.search(r"docker|k8s|helm|terraform", combined, re.I):
        roles.append("deployment_topology")
    if re.search(r"service|worker|queue", combined, re.I):
        roles.append("service_boundary")
    if re.search(r"react|vue|angular|next", combined, re.I):
        roles.append("frontend_framework")
    if re.search(r"django|flask|fastapi|express", combined, re.I):
        roles.append("backend_framework")

    purpose = "application"
    if "docs" in combined.lower():
        purpose = "documentation"
    elif "infra" in combined.lower():
        purpose = "infrastructure"

    return {
        "architecture_roles": sorted(set(roles)),
        "service_boundaries": [r for r in roles if r == "service_boundary"],
        "api_ownership": "api_surface" in roles,
        "deployment_topology": "deployment_topology" in roles,
        "framework_semantics": [r for r in roles if "framework" in r],
        "repository_purpose": purpose,
        "bounded": True,
    }
