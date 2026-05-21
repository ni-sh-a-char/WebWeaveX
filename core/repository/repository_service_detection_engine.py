from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

SERVICE_FILES = {
    "docker-compose.yml",
    "docker-compose.yaml",
    "Dockerfile",
    "package.json",
    "requirements.txt",
    "pyproject.toml",
    "go.mod",
    "Cargo.toml",
}


def detect_repository_services(
    files: List[Dict[str, Any]],
) -> Dict[str, Any]:
    services = []

    for file in files:
        name = Path(file["path"]).name

        if name in SERVICE_FILES:
            services.append({
                "file": file["path"],
                "service_indicator": name,
            })

    return {
        "services": sorted(
            services,
            key=lambda x: x["file"],
        ),
        "bounded": True,
    }
