from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

INFRA_FILES = {
    "Dockerfile": "docker",
    "docker-compose.yml": "docker-compose",
    "docker-compose.yaml": "docker-compose",
    "terraform.tf": "terraform",
    "main.tf": "terraform",
    "deployment.yaml": "kubernetes",
    "deployment.yml": "kubernetes",
    "service.yaml": "kubernetes",
    "k8s.yaml": "kubernetes",
}


def detect_repository_infra(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    infra = []

    for file in files:
        name = Path(file["path"]).name

        provider = INFRA_FILES.get(name)

        if provider:
            infra.append({
                "file": file["path"],
                "type": provider,
            })

    return {
        "infra": sorted(
            infra,
            key=lambda x: x["file"],
        ),
        "bounded": True,
    }
