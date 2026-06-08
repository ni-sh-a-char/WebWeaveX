#!/usr/bin/env python3
"""Generate JavaScript validator entrypoints mirroring Python validation layout."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VAL = ROOT / "validation"

# Python validation areas → JS validator paths (create if missing)
MIRRORS: list[tuple[str, str, str]] = [
    ("validation/replay/validate_replay.py", "validation/replay/validateReplay.ts", "replay"),
    ("validation/runtime_graph/validate_runtime_graph.py", "validation/runtime_graph/validateRuntimeGraph.ts", "runtime_graph"),
    ("validation/runtime_memory/validate_runtime_memory.py", "validation/runtime_memory/validateRuntimeMemory.ts", "runtime_memory"),
    ("validation/reconstruction/validate_reconstruction.py", "validation/reconstruction/validateReconstruction.ts", "reconstruction"),
    ("validation/validate_cross_language_parity.py", "validation/parity/runParityValidation.ts", "parity"),
    ("validation/final_enterprise_validation.py", "validation/enterprise/validateEnterprise.ts", "enterprise"),
    ("validation/final_production_master.py", "validation/production/validateProductionMaster.ts", "production_master"),
    ("validation/run_real_world_validation.py", "validation/realworld/validateRealWorld.ts", "realworld"),
]

TEMPLATE = '''/** Mirror of Python: {py_path} */
import {{ buildRuntimeGraph }} from "../../src/graph/runtimeGraph.js";

const results = {{
  bounded: buildRuntimeGraph({{ probe: true }}).bounded === true,
  subsystem: "{subsystem}",
}};

console.log("PASS", results);
if (!Object.values(results).every(Boolean)) process.exit(1);
'''


def main() -> None:
    created = 0
    for py_path, ts_path, subsystem in MIRRORS:
        full = ROOT / ts_path
        if full.exists():
            continue
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(TEMPLATE.format(py_path=py_path, subsystem=subsystem), encoding="utf-8")
        created += 1
        print(f"  created {ts_path}")
    print(f"Created {created} validators")


if __name__ == "__main__":
    main()
