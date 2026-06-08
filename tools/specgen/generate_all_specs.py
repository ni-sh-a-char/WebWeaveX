#!/usr/bin/env python3
"""Generate all canonical specs from origin/python."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPECS = ROOT / "docs" / "specs"
VECTORS = ROOT / "validation"


def py_modules() -> list[str]:
    r = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "core/"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip().endswith(".py")]


def filter_mod(modules: list[str], *parts: str) -> list[str]:
    return [m for m in modules if any(f"core/{p}" in m for p in parts)]


def main() -> None:
    SPECS.mkdir(parents=True, exist_ok=True)
    mods = py_modules()
    pkgs = sorted({m.split("/")[1] for m in mods if m.count("/") >= 2})

    specs = {
        "canonical_runtime_spec.json": {
            "title": "WebWeaveX Runtime",
            "module_count": len(mods),
            "packages": pkgs,
            "modules": mods,
        },
        "canonical_graph_spec.json": {"modules": filter_mod(mods, "graph", "graph_intelligence", "topology")},
        "canonical_vm_spec.json": {"modules": filter_mod(mods, "vm", "bytecode")},
        "canonical_semantic_spec.json": {"modules": filter_mod(mods, "semantic", "ontology", "contradiction")},
        "canonical_replay_spec.json": {"modules": filter_mod(mods, "replay", "reconstruction")},
        "canonical_validation_spec.json": {
            "python_validators": [
                p
                for p in subprocess.run(
                    ["git", "ls-tree", "-r", "--name-only", "origin/python", "--", "validation/"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                ).stdout.splitlines()
                if p.endswith(".py") and "validate" in p
            ]
        },
        "canonical_governance_spec.json": {
            "files": [
                "CONTRIBUTING.md",
                "SECURITY.md",
                "ROADMAP.md",
                "LICENSE",
                "GOVERNANCE.md",
                "MAINTAINERS.md",
                "SUPPORT.md",
                "RELEASE.md",
                "CODEOWNERS",
            ]
        },
        "canonical_release_spec.json": {
            "npm": {"package": "webweavex", "formats": ["esm", "cjs"], "publishDir": "dist"},
            "python": {"package": "webweavex", "build": "pyproject.toml"},
        },
    }

    for name, body in specs.items():
        (SPECS / name).write_text(json.dumps(body, indent=2), encoding="utf-8")
        print(f"  {name}")

    # topology map
    topo = {p: [m for m in mods if f"core/{p}/" in m] for p in pkgs}
    (SPECS / "canonical_topology_spec.json").write_text(json.dumps(topo, indent=2), encoding="utf-8")
    print("  canonical_topology_spec.json")


if __name__ == "__main__":
    main()
