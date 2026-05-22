#!/usr/bin/env python3
"""Reconstruction determinism validation."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
    from core.reconstruction.runtime_reconstruction_orchestrator import run_reconstruction_runtime

    base = {
        "semantic_ir": {"ir": "semantic_runtime", "domain": "app"},
        "workflow_ir": {"ir": "workflow_runtime", "objective": "monitor"},
        "synchronization_ir": {"ir": "synchronization_runtime"},
        "execution_ir": {"ir": "execution_runtime"},
        "memory_ir": {"ir": "runtime_memory"},
    }
    r1 = reconstruct_runtime(**base, runtime_type="browser", tick=0)
    r2 = reconstruct_runtime(**base, runtime_type="browser", tick=0)
    full = run_reconstruction_runtime(sources=base, runtime_type="browser", tick=0)

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "runtime_id_match": r1["runtime_id"] == r2["runtime_id"],
        "runtime_id": r1["runtime_id"],
        "orchestrator_valid": full.get("validation", {}).get("valid"),
    }
    out = ROOT / "validation" / "reports" / "reconstruction_validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["runtime_id_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
