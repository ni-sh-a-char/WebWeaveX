#!/usr/bin/env python3
"""
Certify generated modules package-by-package (resume-friendly).
Merges results into docs/archive/generated_module_matrix.json.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
MATRIX = ARCHIVE / "generated_module_matrix.json"

sys.path.insert(0, str(ROOT / "tools/convergence"))
from certification_program import (  # noqa: E402
    PROTECTED,
    count_src_nocheck,
    git_lines,
    package_from_py,
    write_module_matrix,
    write_package_certification,
)
from module_certifier import certify_module  # noqa: E402

sys.path.insert(0, str(ROOT / "tools/py2ts"))
from py2ts import py_path_to_ts  # noqa: E402


def load_matrix() -> dict:
    if MATRIX.exists():
        return json.loads(MATRIX.read_text(encoding="utf-8"))
    return {"measured_at": "", "modules": []}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("packages", nargs="*", help="core package names (default: all under core/)")
    p.add_argument("--workers", type=int, default=1, help="Reserved for future parallel probe runs")
    p.add_argument("--timeout", type=int, default=60, help="Per-module probe timeout seconds")
    args = p.parse_args()

    subprocess.run([sys.executable, str(ROOT / "tools/runtime_vectors/materialize_python.py")], cwd=ROOT, check=True)

    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}

    py_mods = [p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")]
    if args.packages:
        allowed = set(args.packages)
        py_mods = [p for p in py_mods if package_from_py(p) in allowed]

    existing = {r["python_module"]: r for r in load_matrix().get("modules", [])}
    ts = datetime.now(timezone.utc).isoformat()
    by_pkg: dict[str, list[dict]] = defaultdict(list)

    for py in py_mods:
        ts_rel = "src/" + py_path_to_ts(py)
        is_protected = ts_rel in protected
        if is_protected:
            row = certify_module(py, ts_rel, protected=True, timeout=args.timeout)
        else:
            row = certify_module(py, ts_rel, protected=False, timeout=args.timeout)
        existing[py] = row
        by_pkg[package_from_py(py)].append(row)
        status = row.get("status")
        print(f"{status:8} {py}")

    merged = list(existing.values())
    write_module_matrix(ts, merged)
    for pkg, rows in sorted(by_pkg.items()):
        write_package_certification(pkg, rows, ts)

    untested = sum(1 for r in merged if r.get("status") == "UNTESTED")
    fail = sum(1 for r in merged if r.get("status") == "FAIL")
    pass_n = sum(1 for r in merged if r.get("status") == "PASS")
    print(f"\nBatch complete: PASS={pass_n} FAIL={fail} UNTESTED={untested} @ts-nocheck={count_src_nocheck()}")
    return 0 if fail == 0 and untested == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
