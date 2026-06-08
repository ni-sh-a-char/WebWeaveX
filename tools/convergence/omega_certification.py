#!/usr/bin/env python3
"""
WebWeaveX Omega Certification — execution-only orchestrator.
Refuses FINAL_TRUE_EQUALITY_CERTIFICATION.md unless every gate passes.
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
from certification_program import (  # noqa: E402
    count_src_nocheck,
    coverage_certification,
    git_lines,
    npm_run,
    package_from_py,
    write_module_matrix,
    write_package_certification,
)


def run_py(script: str, *args: str, timeout: int = 7200) -> int:
    cmd = [sys.executable, str(ROOT / "tools/convergence" / script), *args]
    return subprocess.run(cmd, cwd=ROOT, timeout=timeout).returncode


def summarize_matrix(matrix: list[dict]) -> dict[str, int]:
    return {
        "total": len(matrix),
        "pass": sum(1 for r in matrix if r.get("status") == "PASS"),
        "fail": sum(1 for r in matrix if r.get("status") == "FAIL"),
        "untested": sum(1 for r in matrix if r.get("status") == "UNTESTED"),
    }


def write_generated_module_certification(ts: str, matrix: list[dict], stats: dict[str, int]) -> None:
    (ARCHIVE / "FINAL_GENERATED_MODULE_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL GENERATED MODULE CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if stats['untested'] == 0 and stats['fail'] == 0 and stats['pass'] == stats['total'] else 'FAIL'}",
                "",
                "| Metric | Count |",
                "|--------|-------|",
                f"| Total modules | {stats['total']} |",
                f"| PASS | {stats['pass']} |",
                f"| FAIL | {stats['fail']} |",
                f"| UNTESTED | {stats['untested']} |",
                "",
                "Evidence: `docs/archive/generated_module_matrix.json` (live probes).",
                "",
            ]
        ),
        encoding="utf-8",
    )


def engine_depth_report(ts: str) -> dict:
    py_engines = [
        p
        for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/")
        if p.endswith("_engine.py") or p.endswith("Engine.py")
    ]
    matrix_path = ARCHIVE / "generated_module_matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8")).get("modules", []) if matrix_path.exists() else []
    by_py = {r["python_module"]: r for r in matrix}
    executed = 0
    for eng in py_engines:
        row = by_py.get(eng)
        if row and row.get("python_executed") and row.get("javascript_executed") and row.get("status") == "PASS":
            executed += 1
    total = len(py_engines)
    pct = round(100.0 * executed / total, 2) if total else 0.0
    payload = {"measured_at": ts, "executed_engines": executed, "total_engines": total, "coverage_pct": pct}
    (ARCHIVE / "FINAL_ENGINE_DEPTH_REPORT.md").write_text(
        "\n".join(
            [
                "# FINAL ENGINE DEPTH REPORT",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if pct >= 100 else 'FAIL'}",
                "",
                f"| Executed engines | {executed} |",
                f"| Total engines | {total} |",
                f"| Coverage | {pct}% |",
                "",
                "Target: 100% engine families executed with Python+JS behavioral PASS.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return payload


def oss_certification(ts: str) -> dict:
    py_wf = set(git_lines("ls-tree", "--name-only", "origin/python", "--", ".github/workflows/"))
    js_wf = set()
    wf_dir = ROOT / ".github/workflows"
    if wf_dir.exists():
        js_wf = {f".github/workflows/{p.name}" for p in wf_dir.glob("*.yml")} | {
            f".github/workflows/{p.name}" for p in wf_dir.glob("*.yaml")
        }
    required = {"ci", "release", "publish", "security", "nightly", "benchmark", "provenance"}
    found = {n.split("/")[-1].split(".")[0].lower() for n in js_wf}
    missing = sorted(required - found)
    docs = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "SECURITY.md", "SUPPORT.md", "GOVERNANCE.md", "MAINTAINERS.md"]
    docs_present = [d for d in docs if (ROOT / d).exists()]
    ok = not missing and len(docs_present) >= 5
    (ARCHIVE / "FINAL_OSS_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL OSS CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if ok else 'FAIL'}",
                "",
                f"| Python workflows (origin/python) | {len(py_wf)} |",
                f"| JavaScript workflows | {len(js_wf)} |",
                f"| Required workflow themes missing | {missing or 'none'} |",
                f"| Governance docs present | {len(docs_present)}/{len(docs)} |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"pass": ok, "missing_workflows": missing, "docs_present": docs_present}


def universal_equivalence_report(ts: str) -> dict:
    diff_ok = npm_run("validate:differential")
    equiv_ok = npm_run("validate:equivalence")
    eco_ok = npm_run("validate:ecosystem")
    ok = diff_ok and equiv_ok and eco_ok
    (ARCHIVE / "FINAL_UNIVERSAL_EQUIVALENCE_REPORT.md").write_text(
        "\n".join(
            [
                "# FINAL UNIVERSAL EQUIVALENCE REPORT",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if ok else 'FAIL'}",
                "",
                f"| validate:differential | {'PASS' if diff_ok else 'FAIL'} |",
                f"| validate:equivalence | {'PASS' if equiv_ok else 'FAIL'} |",
                f"| validate:ecosystem | {'PASS' if eco_ok else 'FAIL'} |",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"pass": ok, "differential": diff_ok, "equivalence": equiv_ok, "ecosystem": eco_ok}


def subsystem_certification(ts: str, matrix: list[dict]) -> bool:
    subsystems = [
        "runtime",
        "memory",
        "graph",
        "replay",
        "workflows",
        "distributed",
        "ontology",
        "semantic",
        "browser",
        "parsers",
        "repository",
        "cognition",
        "world_model",
        "extraction",
        "vm",
    ]
    by_pkg: dict[str, list[dict]] = defaultdict(list)
    for r in matrix:
        by_pkg[package_from_py(r["python_module"])].append(r)

    all_pass = True
    for name in subsystems:
        rows = by_pkg.get(name, [])
        if not rows:
            status = "FAIL"
            detail = "no modules mapped"
            all_pass = False
        else:
            passed = [r for r in rows if r.get("status") == "PASS"]
            failed = [r for r in rows if r.get("status") == "FAIL"]
            untested = [r for r in rows if r.get("status") == "UNTESTED"]
            status = "PASS" if passed and not failed and not untested else "FAIL"
            if status != "PASS":
                all_pass = False
            detail = f"PASS={len(passed)} FAIL={len(failed)} UNTESTED={len(untested)}"
        (ARCHIVE / f"FINAL_{name.upper()}_CERTIFICATION.md").write_text(
            "\n".join(
                [
                    f"# FINAL {name.upper()} CERTIFICATION",
                    "",
                    f"**Measured:** {ts}",
                    "",
                    f"**Status:** {status}",
                    "",
                    f"**Evidence:** {detail}",
                    "",
                    "Requires Python executed + JavaScript executed + behavioral PASS per module.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return all_pass


def probe_all_modules(
    *,
    limit: int = 0,
    package: str = "",
    regenerate: bool = False,
) -> list[dict]:
    if regenerate:
        print("Regenerating non-protected ports (py2ts)…")
        subprocess.run([sys.executable, str(ROOT / "tools/py2ts/py2ts.py")], cwd=ROOT, check=True)

    print("Materializing Python staging…")
    subprocess.run([sys.executable, str(ROOT / "tools/runtime_vectors/materialize_python.py")], cwd=ROOT, check=True)

    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    if package:
        py_mods = [p for p in py_mods if p.startswith(f"core/{package}/") or p == f"core/{package}.py"]

    matrix: list[dict] = []
    probed = 0
    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        if limit and probed >= limit:
            matrix.append(
                {
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
            )
            continue
        probed += 1
        row = certify_module(py, ts_rel)
        matrix.append(row)
        if probed % 50 == 0:
            print(f"  probed {probed}/{len(py_mods)} …")
    return matrix


def final_decision(
    ts: str,
    stats: dict[str, int],
    nocheck: int,
    cov: dict,
    rw: dict,
    engine: dict,
    univ: dict,
    oss: dict,
    subsystems_ok: bool,
) -> int:
    blockers: list[str] = []
    if stats["untested"]:
        blockers.append(f"untested_modules={stats['untested']}")
    if stats["fail"]:
        blockers.append(f"failed_modules={stats['fail']}")
    if nocheck:
        blockers.append(f"ts_nocheck={nocheck}")
    if not cov.get("threshold_met"):
        blockers.append(
            f"coverage_fail branches={cov.get('branches_pct')}% lines={cov.get('lines_pct')}%"
        )
    if not rw.get("pass"):
        blockers.append(f"real_world_fail match={rw.get('match_pct')}% drift={rw.get('drift_pct')}%")
    if engine.get("coverage_pct", 0) < 100:
        blockers.append(f"engine_depth={engine.get('coverage_pct')}%")
    if not subsystems_ok:
        blockers.append("subsystems_not_pass")
    if not univ.get("pass"):
        blockers.append("universal_equivalence_fail")
    if not oss.get("pass"):
        blockers.append(f"oss_fail missing={oss.get('missing_workflows')}")

    gates = {
        "untested_modules_zero": stats["untested"] == 0,
        "failed_modules_zero": stats["fail"] == 0,
        "ts_nocheck_zero": nocheck == 0,
        "coverage_pass": bool(cov.get("threshold_met")),
        "real_world_pass": bool(rw.get("pass")),
        "engine_depth_100": engine.get("coverage_pct", 0) >= 100,
        "subsystems_pass": subsystems_ok,
        "differential_pass": univ.get("differential"),
        "equivalence_pass": univ.get("equivalence"),
        "ecosystem_pass": univ.get("ecosystem"),
        "oss_pass": oss.get("pass"),
    }

    if blockers:
        cert = "\n".join(
            [
                "# FINAL TRUE EQUALITY CERTIFICATION",
                "",
                "**STATUS: NOT ISSUED**",
                "",
                f"**Measured:** {ts}",
                "",
                "## Blockers",
                "",
                *(f"- {b}" for b in blockers),
                "",
                "## Gates",
                "",
                *(f"- {k}: {'PASS' if v else 'FAIL'}" for k, v in gates.items()),
                "",
            ]
        )
    else:
        cert = f"# FINAL TRUE EQUALITY CERTIFICATION\n\n**ISSUED:** {ts}\n\nAll gates passed.\n"

    (ARCHIVE / "FINAL_TRUE_EQUALITY_CERTIFICATION.md").write_text(cert, encoding="utf-8")
    subprocess.run([sys.executable, str(ROOT / "tools/convergence/true_equality_audit.py")], cwd=ROOT)
    return 0 if not blockers else 1


def main() -> int:
    p = argparse.ArgumentParser(description="Omega certification (execution-only)")
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--package", type=str, default="")
    p.add_argument("--regenerate", action="store_true", help="Re-run py2ts before probing")
    p.add_argument("--skip-probes", action="store_true")
    p.add_argument("--skip-gates", action="store_true")
    args = p.parse_args()

    ts = datetime.now(timezone.utc).isoformat()
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    run_py("generate_url_matrix.py")

    if args.skip_probes:
        matrix = json.loads((ARCHIVE / "generated_module_matrix.json").read_text(encoding="utf-8")).get("modules", [])
        if not matrix:
            print("No existing matrix; run without --skip-probes first.")
            return 1
    else:
        matrix = probe_all_modules(limit=args.limit, package=args.package, regenerate=args.regenerate)
        write_module_matrix(ts, matrix)
        by_pkg: dict[str, list[dict]] = defaultdict(list)
        for r in matrix:
            by_pkg[package_from_py(r["python_module"])].append(r)
        for pkg, rows in sorted(by_pkg.items()):
            write_package_certification(pkg, rows, ts)

    stats = summarize_matrix(matrix)
    write_generated_module_certification(ts, matrix, stats)
    nocheck = count_src_nocheck()

    if args.skip_gates:
        return 1

    cov = coverage_certification(ts)
    rw_ok = npm_run("validate:realworld", timeout=600)
    rw_path = SPECS / "real_world_probe.json"
    rw = json.loads(rw_path.read_text(encoding="utf-8")) if rw_path.exists() else {"pass": rw_ok}
    engine = engine_depth_report(ts)
    univ = universal_equivalence_report(ts)
    oss = oss_certification(ts)
    subsystems_ok = subsystem_certification(ts, matrix)

    return final_decision(ts, stats, nocheck, cov, rw, engine, univ, oss, subsystems_ok)


if __name__ == "__main__":
    raise SystemExit(main())
