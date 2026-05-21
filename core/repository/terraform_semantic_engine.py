from __future__ import annotations

import re
from typing import Any, Dict, List


RESOURCE_RE = re.compile(
    r'resource\s+"([^"]+)"\s+"([^"]+)"'
)


def parse_terraform_semantics(
    text: str,
) -> Dict[str, Any]:

    resources: List[Dict[str, Any]] = []

    for match in RESOURCE_RE.finditer(text):

        resources.append({
            "resource_type": match.group(1),
            "resource_name": match.group(2),
        })

    return {
        "resources": resources,
        "count": len(resources),
        "grounded": True,
    }
