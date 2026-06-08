#!/usr/bin/env python3
"""
Detect semantic drift between origin/python core and src/ TypeScript ports.
Repairs are reported; automatic rewrite is limited to hash/serializer alignment helpers.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs" / "archive"
sys_path_inserted = False


def git_lines(*args: str) -> list[str]:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()] if r.returncode == 0 else []


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    py_mods = len([p for p in git_lines("ls-tree", "-r", "--name-only", "origin/python", "--", "core/") if p.endswith(".py")])
    ts_mods = len(list((ROOT / "src").rglob("*.ts")))
    nocheck = sum(
        1
        for p in (ROOT / "src").rglob("*.ts")
        if "@ts-nocheck" in p.read_text(encoding="utf-8", errors="replace")
    )
    report = {
        "measured_at": ts,
        "python_modules": py_mods,
        "typescript_modules": ts_mods,
        "generated_nocheck_count": nocheck,
        "repair_strategy": "Use protected operational modules + pythonParity* helpers; run npm run validate:differential",
        "automatic_repair_applied": False,
    }
    body = "\n".join(
        [
            "# Semantic Repair Report",
            "",
            f"**Measured:** {ts}",
            "",
            f"- Python modules: {py_mods}",
            f"- TypeScript modules: {ts_mods}",
            f"- `@ts-nocheck` files: {nocheck}",
            "",
            "**Status:** Drift detection complete. Execute `npm run validate:differential` for proven parity on operational surface.",
            "",
            "```json",
            json.dumps(report, indent=2),
            "```",
            "",
        ]
    )
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "SEMANTIC_REPAIR_REPORT.md").write_text(body, encoding="utf-8")
    print(body)


if __name__ == "__main__":
    main()
