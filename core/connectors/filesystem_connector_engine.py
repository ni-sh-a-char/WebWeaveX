from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_filesystem_runtime(
    root: str = ".",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if snapshot is not None:
        return {
            "root": str(snapshot.get("root", root)),
            "topology": sorted(snapshot.get("files", []), key=str),
            "mutation_streams": list(snapshot.get("mutations", [])),
            "synchronization_state": dict(snapshot.get("sync", {})),
            "permissions": dict(snapshot.get("permissions", {})),
            "inode_relationships": list(snapshot.get("inodes", [])),
            "bounded": True,
        }

    topology: List[str] = []
    try:
        base = Path(root)
        if base.exists():
            for path in sorted(base.rglob("*"))[:5000]:
                if path.is_file():
                    topology.append(str(path.relative_to(base)))
    except Exception:
        return {
            "root": root,
            "topology": [],
            "degraded": True,
            "bounded": True,
        }

    return {
        "root": root,
        "topology": topology,
        "mutation_streams": [],
        "synchronization_state": {},
        "permissions": {},
        "inode_relationships": [],
        "bounded": True,
    }
