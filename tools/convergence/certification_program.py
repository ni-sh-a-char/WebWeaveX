#!/usr/bin/env python3
"""
Phase Omega — WebWeaveX Final Certification Program.
Builds generated_module_matrix.json, package certifications, and certification decision.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
SPECS = ROOT / "docs/specs"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"

sys.path.insert(0, str(ROOT / "tools/convergence"))
sys.path.insert(0, str(ROOT / "tools/py2ts"))
from py2ts import py_path_to_ts  # noqa: E402
from module_certifier import certify_module  # noqa: E402


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def npm_run(script: str, timeout: int = 1800) -> bool:
    if platform.system() == "Windows":
        cmd = ["cmd", "/c", "npm", "run", script]
        shell = False
    else:
        cmd = ["npm", "run", script]
        shell = False
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        shell=shell,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "")[-400:]
        print(f"npm run {script} failed (exit {proc.returncode}): {tail}")
    return proc.returncode == 0


def package_from_py(py_path: str) -> str:
    parts = py_path.removeprefix("core/").split("/")
    return parts[0] if parts else "(root)"


def count_src_nocheck() -> int:
    n = 0
    src = ROOT / "src"
    if not src.exists():
        return 0
    for p in src.rglob("*.ts"):
        if "@ts-nocheck" in p.read_text(encoding="utf-8", errors="replace"):
            n += 1
    return n


def write_module_matrix(ts: str, matrix: list[dict]) -> None:
    payload = {"measured_at": ts, "modules": matrix}
    text = json.dumps(payload, indent=2)
    (SPECS / "generated_module_matrix.json").write_text(text, encoding="utf-8")
    (ARCHIVE / "generated_module_matrix.json").write_text(text, encoding="utf-8")


def write_package_certification(pkg: str, rows: list[dict], ts: str) -> None:
    passed = [r for r in rows if r.get("status") == "PASS"]
    failed = [r for r in rows if r.get("status") == "FAIL"]
    untested = [r for r in rows if r.get("status") == "UNTESTED"]
    hash_mismatch = [r for r in failed if r.get("error") == "output_or_state_mismatch"]
    state_mismatch = [
        r
        for r in failed
        if r.get("python_executed")
        and r.get("javascript_executed")
        and not r.get("output_match")
    ]
    status = "PASS" if passed and not failed and not untested else "FAIL"
    body = "\n".join(
        [
            f"# FINAL PACKAGE {pkg.upper()} EXECUTION CERTIFICATION",
            "",
            f"**Measured:** {ts}",
            "",
            f"**Status:** {status}",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Modules tested | {len(rows)} |",
            f"| PASS | {len(passed)} |",
            f"| FAIL | {len(failed)} |",
            f"| UNTESTED | {len(untested)} |",
            f"| Hash mismatches | {len(hash_mismatch)} |",
            f"| State mismatches | {len(state_mismatch)} |",
            "",
            "## Behavioral mismatches",
            "",
            *(f"- `{r['python_module']}` — {r.get('error')}" for r in failed[:40]),
            *(["", f"_…and {len(failed) - 40} more FAIL_"] if len(failed) > 40 else []),
            "",
            "## UNTESTED",
            "",
            *(f"- `{r['python_module']}` — {r.get('error', 'no probe')}" for r in untested[:20]),
            "",
            "**Certification:** NOT ELIGIBLE until PASS == TOTAL.",
            "",
        ]
    )
    safe = pkg.replace("/", "_").replace("(", "").replace(")", "")
    (ARCHIVE / f"FINAL_PACKAGE_{safe}_EXECUTION_CERTIFICATION.md").write_text(body, encoding="utf-8")
    (ARCHIVE / f"FINAL_PACKAGE_{safe}_CERTIFICATION.md").write_text(body, encoding="utf-8")


def coverage_certification(ts: str) -> dict:
    subprocess.run(
        [sys.executable, str(ROOT / "tools/convergence/coverage_probe.py")],
        cwd=ROOT,
        capture_output=True,
        timeout=900,
    )
    cov_path = SPECS / "coverage_probe.json"
    cov = json.loads(cov_path.read_text(encoding="utf-8")) if cov_path.exists() else {}
    ok = bool(cov.get("threshold_met"))
    (ARCHIVE / "FINAL_COVERAGE_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL COVERAGE CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if ok else 'FAIL'}",
                "",
                "| Metric | Value | Target |",
                "|--------|-------|--------|",
                f"| Lines | {cov.get('lines_pct')}% | ≥98% |",
                f"| Functions | {cov.get('functions_pct')}% | ≥98% |",
                f"| Statements | {cov.get('statements_pct')}% | ≥98% |",
                f"| Branches | {cov.get('branches_pct')}% | ≥95% |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return cov


def real_world_certification(ts: str) -> bool:
    ok = npm_run("validate:realworld", timeout=120)
    (ARCHIVE / "FINAL_REAL_WORLD_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL REAL WORLD CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS (bounded gate)' if ok else 'FAIL'}",
                "",
                "1000+ URL matrix: NOT YET EXECUTED. Bounded real-world validator present.",
                "",
                "See `validation/real_world/` for expansion.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return ok


def engine_certifications(ts: str) -> None:
    engines = [
        "Runtime",
        "Memory",
        "Graph",
        "Replay",
        "Workflow",
        "Distributed",
        "Ontology",
        "Semantic",
        "Extraction",
        "World Model",
        "VM",
        "Cognition",
    ]
    for name in engines:
        (ARCHIVE / f"FINAL_{name.upper().replace(' ', '_')}_ENGINE_CERTIFICATION.md").write_text(
            "\n".join(
                [
                    f"# FINAL {name.upper()} ENGINE CERTIFICATION",
                    "",
                    f"**Measured:** {ts}",
                    "",
                    "**Status: NOT COMPLETE**",
                    "",
                    "Vector-scope equivalence PASS; full engine-by-engine exhaustive proof NOT COMPLETE.",
                    "",
                    f"Run `npm run validate:equivalence` and subsystem reports under docs/archive/FINAL_{name.upper()}_EQUALITY_REPORT.md.",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def certification_decision(
    ts: str,
    matrix: list[dict],
    gates: dict[str, bool],
    blockers: list[str],
) -> None:
    if all(gates.values()) and not blockers:
        cert = f"# FINAL TRUE EQUALITY CERTIFICATION\n\n**Issued:** {ts}\n\nAll gates passed.\n"
    else:
        cert = "\n".join(
            [
                "# FINAL TRUE EQUALITY CERTIFICATION",
                "",
                "**STATUS: NOT ISSUED**",
                "",
                f"**Measured:** {ts}",
                "",
                "## Blocking items",
                "",
                *(f"- {b}" for b in blockers),
                "",
                "## Gate status",
                "",
                *(f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in gates.items()),
                "",
                "TRUE EQUALITY NOT ACHIEVED. Continue certification program.",
                "",
            ]
        )
    (ARCHIVE / "FINAL_TRUE_EQUALITY_CERTIFICATION.md").write_text(cert, encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0, help="Max generated modules to probe (0=all)")
    p.add_argument("--package", type=str, default="", help="Only certify this core package")
    p.add_argument("--skip-probes", action="store_true", help="Matrix + reports only from protected rules")
    p.add_argument("--skip-gates", action="store_true", help="Skip coverage/differential/ecosystem gate runs")
    args = p.parse_args()

    ts = datetime.now(timezone.utc).isoformat()
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    SPECS.mkdir(parents=True, exist_ok=True)

    print("Materializing Python staging…")
    subprocess.run([sys.executable, str(ROOT / "tools/runtime_vectors/materialize_python.py")], cwd=ROOT, check=True)

    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}

    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    if args.package:
        py_mods = [p for p in py_mods if p.startswith(f"core/{args.package}/") or p == f"core/{args.package}.py"]

    matrix: list[dict] = []
    by_pkg: dict[str, list[dict]] = defaultdict(list)
    probed = 0

    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        is_protected = ts_rel in protected
        if args.skip_probes and not is_protected:
            row = {
                "module": py,
                "python_module": py,
                "javascript_module": ts_rel,
                "python_executed": False,
                "javascript_executed": False,
                "output_match": False,
                "runtime_match": False,
                "semantic_match": False,
                "memory_match": False,
                "status": "UNTESTED",
                "error": "skip_probes",
                "probe_function": None,
            }
        else:
            if not is_protected and args.limit and probed >= args.limit:
                row = {
                    "module": py,
                    "python_module": py,
                    "javascript_module": ts_rel,
                    "python_executed": False,
                    "javascript_executed": False,
                    "output_match": False,
                    "runtime_match": False,
                    "semantic_match": False,
                    "memory_match": False,
                    "status": "UNTESTED",
                    "error": "probe_limit",
                    "probe_function": None,
                }
            else:
                if not is_protected:
                    probed += 1
                row = certify_module(py, ts_rel, protected=is_protected, timeout=25)
        matrix.append(row)
        by_pkg[package_from_py(py)].append(row)

    write_module_matrix(ts, matrix)

    for pkg, rows in sorted(by_pkg.items()):
        write_package_certification(pkg, rows, ts)

    nocheck_count = count_src_nocheck()
    untested = sum(1 for r in matrix if r.get("status") == "UNTESTED")
    fail = sum(1 for r in matrix if r.get("status") == "FAIL")
    pass_n = sum(1 for r in matrix if r.get("status") == "PASS")
    tested = sum(1 for r in matrix if r.get("python_executed") and r.get("javascript_executed"))

    if args.skip_gates:
        cov = {"threshold_met": False}
        rw_ok = False
        diff_ok = False
        equiv_ok = False
        eco_ok = False
    else:
        cov = coverage_certification(ts)
        rw_ok = real_world_certification(ts)
        engine_certifications(ts)
        diff_ok = npm_run("validate:differential")
        equiv_ok = npm_run("validate:equivalence")
        eco_ok = npm_run("validate:ecosystem")
        subprocess.run([sys.executable, str(ROOT / "tools/convergence/true_equality_audit.py")], cwd=ROOT)
        subprocess.run([sys.executable, str(ROOT / "tools/convergence/nocheck_elimination.py")], cwd=ROOT)

    blockers: list[str] = []
    if untested:
        blockers.append(f"UNTESTED generated modules: {untested}")
    if fail:
        blockers.append(f"FAIL modules: {fail}")
    if nocheck_count:
        blockers.append(f"@ts-nocheck files: {nocheck_count}")
    if not cov.get("threshold_met"):
        blockers.append("Coverage thresholds not met")
    if not rw_ok:
        blockers.append("Real-world validation incomplete")
    if not diff_ok:
        blockers.append("Differential validation failed")
    if not equiv_ok:
        blockers.append("Universal equivalence failed")
    if not eco_ok:
        blockers.append("Ecosystem validation failed")

    gates = {
        "all_modules_tested": untested == 0,
        "all_modules_pass": pass_n == len(matrix),
        "no_ts_nocheck": nocheck_count == 0,
        "coverage": bool(cov.get("threshold_met")),
        "real_world": rw_ok,
        "differential": diff_ok,
        "equivalence": equiv_ok,
        "ecosystem": eco_ok,
    }

    certification_decision(ts, matrix, gates, blockers)

    print(f"Matrix: {len(matrix)} modules | PASS={pass_n} FAIL={fail} UNTESTED={untested} probed={tested} nocheck={nocheck_count}")
    print(f"Certification issued: {all(gates.values()) and not blockers}")
    return 0 if all(gates.values()) and not blockers else 1


if __name__ == "__main__":
    raise SystemExit(main())
