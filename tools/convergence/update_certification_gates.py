#!/usr/bin/env python3
"""Re-run certification gates and refresh FINAL_TRUE_EQUALITY_CERTIFICATION.md."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
MATRIX = ARCHIVE / "generated_module_matrix.json"

sys.path.insert(0, str(ROOT / "tools/convergence"))
from certification_program import (  # noqa: E402
    certification_decision,
    count_src_nocheck,
    coverage_certification,
    engine_certifications,
    npm_run,
    real_world_certification,
)


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    matrix = json.loads(MATRIX.read_text(encoding="utf-8")).get("modules", []) if MATRIX.exists() else []
    untested = sum(1 for r in matrix if r.get("status") == "UNTESTED")
    fail = sum(1 for r in matrix if r.get("status") == "FAIL")
    pass_n = sum(1 for r in matrix if r.get("status") == "PASS")
    nocheck_count = count_src_nocheck()

    cov = coverage_certification(ts)
    rw_ok = real_world_certification(ts)
    engine_certifications(ts)
    diff_ok = npm_run("validate:differential")
    equiv_ok = npm_run("validate:equivalence")
    eco_ok = npm_run("validate:ecosystem")

    blockers: list[str] = []
    if untested:
        blockers.append(f"UNTESTED generated modules: {untested}")
    if fail:
        blockers.append(f"FAIL modules: {fail}")
    if nocheck_count:
        blockers.append(f"@ts-nocheck files: {nocheck_count}")
    if not cov.get("threshold_met"):
        blockers.append("Coverage thresholds not met (branches ≥95%, lines/functions/statements ≥98%)")
    if not rw_ok:
        blockers.append("Real-world validation incomplete (1000+ URL matrix not executed)")
    if not diff_ok:
        blockers.append("Differential validation failed")
    if not equiv_ok:
        blockers.append("Universal equivalence failed")
    if not eco_ok:
        blockers.append("Ecosystem validation failed")

    gates = {
        "all_modules_tested": untested == 0,
        "all_modules_pass": pass_n == len(matrix) and len(matrix) > 0,
        "no_ts_nocheck": nocheck_count == 0,
        "coverage": bool(cov.get("threshold_met")),
        "real_world": rw_ok,
        "differential": diff_ok,
        "equivalence": equiv_ok,
        "ecosystem": eco_ok,
    }
    certification_decision(ts, matrix, gates, blockers)
    print(f"Gates: {gates}")
    print(f"Blockers: {len(blockers)}")
    return 0 if all(gates.values()) and not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
