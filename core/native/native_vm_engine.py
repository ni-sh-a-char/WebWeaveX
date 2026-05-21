from __future__ import annotations

from typing import Any, Dict, Optional


VM_BACKENDS = ("virtualbox", "vmware", "qemu", "hyper-v")


def extract_vm_runtime(
    backend: str = "qemu",
    snapshot: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    snap = snapshot or {}
    normalized = backend.lower().replace("_", "-")

    if normalized not in VM_BACKENDS and normalized != "hyperv":
        normalized = "qemu"

    return {
        "backend": normalized,
        "vm_state": str(snap.get("vm_state", "stopped")),
        "window_streams": list(snap.get("window_streams", [])),
        "active_sessions": list(snap.get("active_sessions", [])),
        "metadata": dict(snap.get("metadata", {})),
        "bounded": True,
    }
