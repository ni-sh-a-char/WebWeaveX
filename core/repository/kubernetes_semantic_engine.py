from __future__ import annotations

from typing import Any, Dict, List


def _parse_kubernetes_lines(text: str) -> List[Dict[str, Any]]:
    workloads: List[Dict[str, Any]] = []
    kind: str | None = None
    name: str | None = None
    in_metadata = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("kind:"):
            if kind:
                workloads.append({"kind": kind, "name": name})
            kind = stripped.split(":", 1)[1].strip()
            name = None
            in_metadata = False
        elif stripped == "metadata:":
            in_metadata = True
        elif in_metadata and stripped.startswith("name:"):
            name = stripped.split(":", 1)[1].strip()
            in_metadata = False
    if kind:
        workloads.append({"kind": kind, "name": name})
    return workloads


def parse_kubernetes_semantics(
    text: str,
) -> Dict[str, Any]:

    workloads: List[Dict[str, Any]] = []

    try:
        import yaml  # type: ignore

        docs = list(yaml.safe_load_all(text))
        for doc in docs:
            if not isinstance(doc, dict):
                continue
            kind = doc.get("kind")
            metadata = doc.get("metadata", {})
            workloads.append({
                "kind": kind,
                "name": metadata.get("name"),
            })
    except ImportError:
        workloads = _parse_kubernetes_lines(text)

    return {
        "workloads": workloads,
        "count": len(workloads),
        "grounded": True,
        "deterministic": True,
    }
