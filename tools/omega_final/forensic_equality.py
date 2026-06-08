#!/usr/bin/env python3
"""
Omega-Infinity forensic inventory + implementation_equality_matrix.json
+ FINAL_FORENSIC_EQUALITY_REPORT.md
"""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
SPECS = ROOT / "docs/specs"
SRC = ROOT / "src"
MATRIX_PATH = ARCHIVE / "generated_module_matrix.json"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"

sys_path_py2ts = ROOT / "tools/py2ts"
import sys

sys.path.insert(0, str(ROOT / "tools/py2ts"))
from py2ts import py_path_to_ts  # noqa: E402


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def load_matrix() -> dict[str, dict]:
    if not MATRIX_PATH.exists():
        return {}
    data = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    return {r["python_module"]: r for r in data.get("modules", []) if r.get("python_module")}


def load_protected() -> set[str]:
    if not PROTECTED.exists():
        return set()
    return {ln.strip().replace("\\", "/") for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}


def ts_modules() -> dict[str, str]:
    """rel path -> package"""
    out: dict[str, str] = {}
    for p in SRC.rglob("*.ts"):
        rel = str(p.relative_to(SRC)).replace("\\", "/")
        pkg = rel.split("/")[0] if "/" in rel else "(root)"
        out[f"src/{rel}"] = pkg
    return out


def classify_mapping(py: str, ts_rel: str, row: dict | None, ts_exists: bool) -> str:
    if not ts_exists:
        return "MISSING"
    if row is None:
        return "UNTESTED"
    status = row.get("status")
    if status == "PASS":
        return "EQUAL"
    if status == "UNTESTED":
        return "UNTESTED"
    err = str(row.get("error") or "")
    if "missing_ts" in err or "Transform failed" in err or "Syntax error" in err:
        return "BROKEN"
    if status == "FAIL":
        if row.get("python_executed") and row.get("javascript_executed") and not row.get("output_match"):
            return "PARTIAL"
        return "BROKEN"
    return "UNTESTED"


def engine_inventory(py_mods: list[str]) -> dict[str, list[str]]:
    engines: dict[str, list[str]] = defaultdict(list)
    for py in py_mods:
        base = Path(py).name
        if base.endswith("_engine.py") or base.endswith("Engine.py"):
            pkg = py.removeprefix("core/").split("/")[0]
            engines[pkg].append(py)
    return dict(engines)


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    ts_all = ts_modules()
    protected = load_protected()
    matrix = load_matrix()

    mappings: list[dict] = []
    class_counts: dict[str, int] = defaultdict(int)
    pkg_stats: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    py_to_ts: dict[str, str] = {}
    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        py_to_ts[py] = ts_rel
        row = matrix.get(py)
        ts_exists = (ROOT / ts_rel).exists()
        classification = classify_mapping(py, ts_rel, row, ts_exists)
        class_counts[classification] += 1
        pkg = py.removeprefix("core/").split("/")[0]
        pkg_stats[pkg][classification] += 1
        mappings.append(
            {
                "python_module": py,
                "javascript_module": ts_rel,
                "package": pkg,
                "classification": classification,
                "certification_status": row.get("status") if row else None,
                "protected": ts_rel in protected,
                "python_executed": row.get("python_executed") if row else False,
                "javascript_executed": row.get("javascript_executed") if row else False,
                "output_match": row.get("output_match") if row else False,
            }
        )

    # Orphan JS (no Python counterpart). Two kinds of orphan are runtime
    # support rather than missing implementations and are reported in a
    # separate `support_files` inventory, not as MISSING pairs:
    #  - src/runtime/pyCompat.ts (the Python-semantics substrate; JS-only
    #    by design — it has no Python counterpart to be equal to)
    #  - generated ModuleNotFoundError parity stubs (the module is absent
    #    in BOTH runtimes; the stub mirrors Python's import failure)
    def is_support(rel: str) -> bool:
        if rel == "src/runtime/pyCompat.ts":
            return True
        try:
            head = (ROOT / rel).read_text(encoding="utf-8", errors="replace")[:400]
        except OSError:
            return False
        return "does not exist in the Python" in head and "ModuleNotFoundError" in head

    py_ts_set = set(py_to_ts.values())
    orphans = [rel for rel in ts_all if rel not in py_ts_set and rel not in protected]
    support_files = [rel for rel in orphans if is_support(rel)]
    orphans = [rel for rel in orphans if rel not in support_files]
    for rel in orphans[:500]:
        mappings.append(
            {
                "python_module": None,
                "javascript_module": rel,
                "package": ts_all[rel],
                "classification": "MISSING",
                "certification_status": None,
                "protected": rel in protected,
                "orphan_js": True,
            }
        )
        class_counts["MISSING"] += 1

    cert_pass = sum(1 for r in matrix.values() if r.get("status") == "PASS")
    cert_fail = sum(1 for r in matrix.values() if r.get("status") == "FAIL")
    cert_untested = sum(1 for r in matrix.values() if r.get("status") == "UNTESTED")

    payload = {
        "measured_at": ts,
        "authority": "webweavex-spec",
        "python_modules": len(py_mods),
        "javascript_modules": len(ts_all),
        "mapped_pairs": len(py_mods),
        "classification_counts": dict(class_counts),
        "certification": {
            "probed": len(matrix),
            "pass": cert_pass,
            "fail": cert_fail,
            "untested": cert_untested,
        },
        "support_files": support_files,
        "mappings": mappings,
    }
    out_json = SPECS / "implementation_equality_matrix.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (ARCHIVE / "implementation_equality_matrix.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    engines = engine_inventory(py_mods)
    forensic_pass = (
        cert_fail == 0
        and cert_untested == 0
        and cert_pass >= len(py_mods)
        and class_counts.get("EQUAL", 0) == len(py_mods)
        and all(v == 0 for k, v in class_counts.items() if k != "EQUAL")
    )
    report = [
        "# FINAL FORENSIC EQUALITY REPORT",
        "",
        f"**Measured:** {ts}",
        "",
        (
            "**STATUS: ISSUED** (every mapped pair EQUAL with execution evidence)"
            if forensic_pass
            else "**STATUS: NOT ISSUED** (execution certification incomplete)"
        ),
        "",
        "## Inventory",
        "",
        "| Asset | Python (origin/python) | JavaScript (src/) |",
        "|-------|------------------------|-------------------|",
        f"| Modules | {len(py_mods)} | {len(ts_all)} |",
        f"| Protected hand-written TS | — | {len(protected)} |",
        f"| Engine files (`*_engine.py`) | {sum(len(v) for v in engines.values())} | (mirrored under src/) |",
        "",
        "## Implementation mapping classification",
        "",
        "| Classification | Count | Meaning |",
        "|----------------|-------|---------|",
        f"| EQUAL | {class_counts.get('EQUAL', 0)} | Probed PASS — execution match |",
        f"| PARTIAL | {class_counts.get('PARTIAL', 0)} | Mapped but untested or output mismatch |",
        f"| BROKEN | {class_counts.get('BROKEN', 0)} | Probe/transform/runtime failure |",
        f"| MISSING | {class_counts.get('MISSING', 0)} | No counterpart or orphan |",
        f"| EXACT | {class_counts.get('EXACT', 0)} | Reserved for structural identity |",
        "",
        "## Module execution certification (live matrix)",
        "",
        f"| PASS | {cert_pass} |",
        f"| FAIL | {cert_fail} |",
        f"| UNTESTED | {cert_untested} |",
        f"| Target | {len(py_mods)} |",
        "",
        "## Package engines (Python)",
        "",
    ]
    for pkg in sorted(engines.keys())[:40]:
        stats = pkg_stats[pkg]
        report.append(
            f"- **{pkg}**: {len(engines[pkg])} engines — "
            f"EQUAL={stats.get('EQUAL', 0)} PARTIAL={stats.get('PARTIAL', 0)} "
            f"BROKEN={stats.get('BROKEN', 0)} MISSING={stats.get('MISSING', 0)}"
        )
    report.extend(
        [
            "",
            "## Architecture authority",
            "",
            "Specification (`specification/`) is canonical. Neither Python nor JavaScript is runtime authority.",
            "",
            "## Evidence",
            "",
            "- `docs/specs/implementation_equality_matrix.json`",
            "- `docs/archive/generated_module_matrix.json`",
            "- `docs/archive/FINAL_JS_INVENTORY.json`",
            "- `docs/archive/FINAL_PYTHON_DEPENDENCY_AUDIT.md`",
            "",
            "**IMPLEMENTATION_EQUALITY = FALSE** until PASS = ALL modules.",
            "",
        ]
    )
    (ARCHIVE / "FINAL_FORENSIC_EQUALITY_REPORT.md").write_text("\n".join(report), encoding="utf-8")

    # Module execution certification summary
    (ARCHIVE / "FINAL_MODULE_EXECUTION_CERTIFICATION.md").write_text(
        "\n".join(
            [
                "# FINAL MODULE EXECUTION CERTIFICATION",
                "",
                f"**Measured:** {ts}",
                "",
                f"**Status:** {'PASS' if cert_fail == 0 and cert_untested == 0 and cert_pass >= len(py_mods) else 'FAIL'}",
                "",
                "| Metric | Value | Target |",
                "|--------|-------|--------|",
                f"| PASS | {cert_pass} | {len(py_mods)} |",
                f"| FAIL | {cert_fail} | 0 |",
                f"| UNTESTED | {cert_untested} | 0 |",
                "",
                "Evidence: live probes in `generated_module_matrix.json`.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(
        f"Forensic: py={len(py_mods)} ts={len(ts_all)} "
        f"EQUAL={class_counts.get('EQUAL', 0)} cert PASS={cert_pass} FAIL={cert_fail}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
