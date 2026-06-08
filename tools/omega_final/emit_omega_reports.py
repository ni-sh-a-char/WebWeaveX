#!/usr/bin/env python3
"""Emit Omega-Final decoupling and specification migration reports."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
TS = datetime.now(timezone.utc).isoformat()

DECOUPLE_ACTIONS = [
    ("validation/real_world/validateRealWorld.ts", "REPLACE", "Remove execSync python; use JS-only URL corpus probes"),
    ("validation/differential/common.ts", "REPLACE", "Load vectors from specification/vectors; drop origin/python authority"),
    ("validation/parity/runParityValidation.ts", "REPLACE", "Spec-native parity, not python_vectors.json generation"),
    ("tests/generated/vectorConformance.test.ts", "REPLACE", "Assert source=webweavex-spec"),
    ("src/memory/pythonParityMemory.ts", "REPLACE", "Rename to specMemory / native implementation"),
    ("src/reconstruction/pythonParityReconstruction.ts", "REPLACE", "Spec-native reconstruction"),
    (".github/workflows/nightly.yml", "REPLACE", "Split JS-only nightly from dev parity workflow"),
    ("package.json scripts (22 python entries)", "SAFE", "Dev-only; move under scripts/dev/ or document as non-runtime"),
]

(ARCHIVE / "FINAL_DECOUPLING_REPORT.md").write_text(
    "\n".join(
        [
            "# FINAL DECOUPLING REPORT",
            "",
            f"**Measured:** {TS}",
            "",
            "**Status:** IN PROGRESS",
            "",
            "## Principle",
            "",
            "Python may exist for **development parity validation** only.",
            "The published `webweavex` npm package must never invoke Python.",
            "",
            "## Action matrix",
            "",
            "| Location | Action | Notes |",
            "|----------|--------|-------|",
            *[f"| `{a[0]}` | {a[1]} | {a[2]} |" for a in DECOUPLE_ACTIONS],
            "",
            "## Verified",
            "",
            "- `src/` has **0** subprocess/Python runtime invocations (see FINAL_PYTHON_DEPENDENCY_AUDIT.md)",
            "- `package.json` `files` publishes only `dist`, `README.md`, `LICENSE`",
            "",
        ]
    ),
    encoding="utf-8",
)

(ARCHIVE / "FINAL_SPECIFICATION_MIGRATION_REPORT.md").write_text(
    "\n".join(
        [
            "# FINAL SPECIFICATION MIGRATION REPORT",
            "",
            f"**Measured:** {TS}",
            "",
            "**Status:** STARTED",
            "",
            "## Created",
            "",
            "- `specification/README.md` — authority model",
            "- `specification/vectors/manifest.json` — vector families",
            "",
            "## Pending",
            "",
            "- Re-home `validation/vectors/*` → `specification/vectors/*` with `source: webweavex-spec`",
            "- Add `specification/contracts/` and `specification/schemas/` from `docs/specs/`",
            "- JS validators consume `specification/` only (Phase 4)",
            "- Python validators consume same `specification/` (independent CI)",
            "",
        ]
    ),
    encoding="utf-8",
)

(ARCHIVE / "FINAL_IMPLEMENTATION_EQUALITY_REPORT.md").write_text(
    "\n".join(
        [
            "# FINAL IMPLEMENTATION EQUALITY REPORT",
            "",
            f"**Measured:** {TS}",
            "",
            "**STATUS: NOT ISSUED**",
            "",
            "## Model",
            "",
            "Equality = Python conforms to spec **AND** JavaScript conforms to spec.",
            "Neither implementation is runtime authority over the other.",
            "",
            "## Current evidence",
            "",
            "| Gate | Status |",
            "|------|--------|",
            "| JS execution certification | FAIL (202/1724 PASS in partial matrix) |",
            "| Spec-native JS validation | NOT MIGRATED |",
            "| Python runtime in npm path | ABSENT from `src/` |",
            "| Validation Python coupling | REPLACE required |",
            "",
            "**IMPLEMENTATION EQUALITY = FALSE** until both implementations pass spec certification.",
            "",
        ]
    ),
    encoding="utf-8",
)

(ARCHIVE / "FINAL_JS_RELEASE_CERTIFICATION.md").write_text(
    "\n".join(
        [
            "# FINAL JS RELEASE CERTIFICATION",
            "",
            f"**Measured:** {TS}",
            "",
            "**STATUS: NOT ISSUED**",
            "",
            "## Blockers",
            "",
            "- Self-contained npm certification incomplete",
            "- JS execution certification incomplete (202 PASS / 1724)",
            "- Engine certification incomplete",
            "- Coverage below threshold",
            "- Spec migration incomplete",
            "- Implementation equality not demonstrated via spec",
            "",
        ]
    ),
    encoding="utf-8",
)

print("Wrote decoupling, spec migration, equality, and release reports")
