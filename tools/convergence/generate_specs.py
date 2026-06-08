#!/usr/bin/env python3
"""Generate canonical machine-readable specs from Python (source of truth)."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs" / "specs"


def git_py_modules() -> list[str]:
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(".py")]


def main() -> None:
    SPECS.mkdir(parents=True, exist_ok=True)
    modules = git_py_modules()
    packages = sorted({p.split("/")[1] for p in modules if p.startswith("core/") and p.count("/") >= 2})

    runtime_spec = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "WebWeaveX Runtime Cognition Spec",
        "description": "Canonical subsystem map generated from origin/python",
        "packages": packages,
        "module_count": len(modules),
        "modules": modules,
    }
    (SPECS / "canonical_runtime_spec.json").write_text(json.dumps(runtime_spec, indent=2), encoding="utf-8")

    for name, subs in {
        "semantic": ["semantic", "ontology", "contradiction", "lineage"],
        "graph": ["graph", "graph_intelligence", "topology"],
        "vm": ["vm", "bytecode"],
        "replay": ["replay", "reconstruction"],
    }.items():
        matched = [m for m in modules if any(f"core/{s}/" in m or f"core/{s}." in m for s in subs)]
        (SPECS / f"canonical_{name}_spec.json").write_text(
            json.dumps({"modules": matched, "count": len(matched)}, indent=2),
            encoding="utf-8",
        )

    print(f"Wrote specs under {SPECS}")


if __name__ == "__main__":
    main()
