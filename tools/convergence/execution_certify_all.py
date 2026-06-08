#!/usr/bin/env python3
"""Run execution certification for all core packages (resume-friendly)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PACKAGES = [
    "adaptive",
    "agents",
    "application",
    "ast",
    "auth",
    "autonomy",
    "browser",
    "bytecode",
    "cognition",
    "connectors",
    "contracts",
    "crawling",
    "distributed",
    "documents",
    "evidence",
    "execution",
    "extraction",
    "graph",
    "memory",
    "ontology",
    "parsers",
    "reconstruction",
    "replay",
    "runtime",
    "semantic",
    "streaming",
    "universal",
    "validation",
    "vm",
    "workflow",
]


def main() -> int:
    start = 0
    if len(sys.argv) > 1:
        if sys.argv[1] == "--from":
            start = PACKAGES.index(sys.argv[2]) if len(sys.argv) > 2 else 0
        else:
            pkgs = sys.argv[1:]
            return subprocess.call(
                [sys.executable, str(ROOT / "tools/convergence/batch_package_certify.py"), *pkgs],
                cwd=ROOT,
            )

    rc = 0
    for pkg in PACKAGES[start:]:
        print(f"\n=== PACKAGE {pkg} ===", flush=True)
        code = subprocess.call(
            [sys.executable, str(ROOT / "tools/convergence/batch_package_certify.py"), pkg],
            cwd=ROOT,
        )
        if code != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
