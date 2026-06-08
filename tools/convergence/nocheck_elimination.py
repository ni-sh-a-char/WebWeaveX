#!/usr/bin/env python3
"""
Stage 4 — @ts-nocheck elimination tracker.
Removes @ts-nocheck only when file is in protected list (hand-written) or after manual fix.
Default: audit + report (no mass removal without typecheck pass).
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    protected: set[str] = set()
    if PROTECTED.exists():
        protected = {ln.strip() for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}

    files: list[dict] = []
    for p in (ROOT / "src").rglob("*.ts"):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        text = p.read_text(encoding="utf-8", errors="replace")
        if "@ts-nocheck" not in text:
            continue
        files.append({"path": rel, "protected": rel in protected, "lines": len(text.splitlines())})

    body = "\n".join(
        [
            "# FINAL NOCHECK ELIMINATION REPORT",
            "",
            f"**Measured:** {ts}",
            "",
            f"**@ts-nocheck count:** {len(files)}",
            f"**Target:** 0",
            "",
            "**Status: FAIL** — mass removal without per-file type repair is not applied.",
            "",
            "Procedure: fix types/imports/contracts per file, run `npm run typecheck`, then remove directive.",
            "",
            "```json",
            json.dumps({"count": len(files), "sample": files[:50]}, indent=2),
            "```",
            "",
        ]
    )
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    (ARCHIVE / "FINAL_NOCHECK_ELIMINATION_REPORT.md").write_text(body, encoding="utf-8")
    print(body[:1500])
    return 1 if len(files) else 0


if __name__ == "__main__":
    raise SystemExit(main())
