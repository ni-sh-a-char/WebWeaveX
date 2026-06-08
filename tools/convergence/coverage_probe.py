#!/usr/bin/env python3
"""Run vitest coverage and emit canonical JSON metrics (Windows-safe)."""
from __future__ import annotations

import json
import platform
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "specs" / "coverage_probe.json"


def npm_cmd(script: str) -> list[str] | str:
    if platform.system() == "Windows":
        return f"npm run {script}"
    return ["npm", "run", script]


def main() -> int:
    proc = subprocess.run(
        npm_cmd("coverage"),
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
        shell=platform.system() == "Windows",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    metrics = {
        "lines_pct": None,
        "functions_pct": None,
        "branches_pct": None,
        "statements_pct": None,
        "exit_code": proc.returncode,
    }
    for line in out.splitlines():
        if "All files" in line and "|" in line:
            cols = [c.strip() for c in line.split("|") if c.strip()]
            if len(cols) >= 5:
                try:
                    metrics["statements_pct"] = float(cols[1].replace("%", ""))
                    metrics["branches_pct"] = float(cols[2].replace("%", ""))
                    metrics["functions_pct"] = float(cols[3].replace("%", ""))
                    metrics["lines_pct"] = float(cols[4].replace("%", ""))
                except ValueError:
                    pass
    metrics["threshold_met"] = (
        (metrics["branches_pct"] or 0) >= 95
        and (metrics["lines_pct"] or 0) >= 98
        and (metrics["functions_pct"] or 0) >= 98
        and (metrics["statements_pct"] or 0) >= 98
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))
    return 0 if metrics["threshold_met"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
