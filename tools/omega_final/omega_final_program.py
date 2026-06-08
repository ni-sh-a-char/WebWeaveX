#!/usr/bin/env python3
"""Omega-Final — run decoupling, npm audit, forensic, and certification reports."""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
TOOLS = ROOT / "tools/omega_final"


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd[:4]), "...", flush=True)
    return subprocess.call(cmd, cwd=ROOT)


def count_nocheck() -> int:
    n = 0
    for p in (ROOT / "src").rglob("*.ts"):
        if "@ts-nocheck" in p.read_text(encoding="utf-8", errors="replace"):
            n += 1
    return n


def load_matrix_stats() -> dict:
    p = ARCHIVE / "generated_module_matrix.json"
    if not p.exists():
        return {"pass": 0, "fail": 0, "untested": 0, "total": 0}
    mods = json.loads(p.read_text(encoding="utf-8")).get("modules", [])
    return {
        "pass": sum(1 for r in mods if r.get("status") == "PASS"),
        "fail": sum(1 for r in mods if r.get("status") == "FAIL"),
        "untested": sum(1 for r in mods if r.get("status") == "UNTESTED"),
        "total": len(mods),
    }


def oss_check() -> tuple[int, int]:
    required = [
        "README.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "GOVERNANCE.md",
    ]
    present = sum(1 for f in required if (ROOT / f).exists())
    return present, len(required)


def write_coverage_report(ts: str, nocheck: int) -> None:
    cov_pass = False
    cov_detail = "not run"
    try:
        proc = subprocess.run(
            ["npm", "run", "coverage", "--", "--reporter=json-summary"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=600,
        )
        summary_path = ROOT / "coverage/coverage-summary.json"
        if summary_path.exists():
            data = json.loads(summary_path.read_text(encoding="utf-8"))
            total = data.get("total", {})
            branches = total.get("branches", {}).get("pct", 0)
            lines = total.get("lines", {}).get("pct", 0)
            cov_pass = branches >= 95 and lines >= 98
            cov_detail = f"lines={lines}% branches={branches}%"
    except Exception as exc:  # noqa: BLE001
        cov_detail = str(exc)

    (ARCHIVE / "FINAL_COVERAGE_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL COVERAGE CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if cov_pass else 'FAIL'}",
                "",
                f"Detail: {cov_detail}",
                "",
                "Targets: statements/functions/lines ≥98%, branches ≥95%.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_oss_report(ts: str) -> None:
    present, total = oss_check()
    (ARCHIVE / "FINAL_OSS_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL OSS CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if present >= total else 'FAIL'}",
                "",
                f"Core governance files present: {present}/{total}",
                "",
                "See FINAL_REPOSITORY_CLEANUP_REPORT.md for archive classification.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_cleanup_report(ts: str) -> None:
    archive_n = len(list(ARCHIVE.glob("*.md"))) if ARCHIVE.exists() else 0
    (ARCHIVE / "FINAL_REPOSITORY_CLEANUP_REPORT.md").write_text(
        "\n".join(
            [
                "# FINAL REPOSITORY CLEANUP REPORT",
                "",
                f"**Measured:** {ts}",
                "",
                "**Status:** IN PROGRESS",
                "",
                "| Area | Action |",
                "|------|--------|",
                f"| `docs/archive/` ({archive_n} markdown reports) | ARCHIVE — not in npm pack |",
                "| `tools/convergence/`, `tools/py2ts/` | KEEP dev-only |",
                "| `specification/` | KEEP — canonical authority |",
                "| Broken generated ports | DELETE/REPLACE via py2ts fixes |",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_final_decision(ts: str, stats: dict, decouple_rc: int, npm_rc: int, nocheck: int) -> None:
    blockers = []
    if stats["pass"] < 1724 or stats["fail"] or stats["untested"]:
        blockers.append(f"Module execution: PASS={stats['pass']} FAIL={stats['fail']} UNTESTED={stats['untested']}")
    if decouple_rc != 0:
        blockers.append("JS decoupling: src runtime blockers")
    if npm_rc != 0:
        blockers.append("npm pack audit failed")
    if nocheck:
        blockers.append(f"@ts-nocheck: {nocheck}")

    issued = not blockers
    (ARCHIVE / "FINAL_RELEASE_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL RELEASE CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**STATUS: {'ISSUED' if issued else 'NOT ISSUED'}**",
                "",
                "## JavaScript (npm install webweavex)",
                "",
                f"- Self-contained runtime (`src/`): {'YES' if decouple_rc == 0 else 'NO'}",
                f"- npm pack: {'PASS' if npm_rc == 0 else 'FAIL'}",
                f"- Module certification: {stats['pass']}/1724 PASS",
                "",
                "## Python (pip install webweavex)",
                "",
                "- Certified from this repository pass: **NO** (Python product lives on `origin/python`)",
                "",
                "## Blockers",
                "",
                *(f"- {b}" for b in blockers) if blockers else ["- None"],
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    run([sys.executable, str(TOOLS / "sync_spec_vectors.py")])
    decouple_rc = run([sys.executable, str(TOOLS / "js_decoupling_audit.py")])
    npm_rc = run(["npx", "tsx", str(TOOLS / "npm_release_audit.ts")])
    run([sys.executable, str(TOOLS / "forensic_equality.py")])
    run([sys.executable, str(TOOLS / "emit_omega_infinity_reports.py")])
    stats = load_matrix_stats()
    nocheck = count_nocheck()
    write_coverage_report(ts, nocheck)
    write_oss_report(ts)
    write_cleanup_report(ts)
    write_final_decision(ts, stats, decouple_rc, npm_rc, nocheck)
    print(f"Omega-Final complete: PASS={stats['pass']} decouple={decouple_rc} npm={npm_rc}")
    return 0 if decouple_rc == 0 and npm_rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
