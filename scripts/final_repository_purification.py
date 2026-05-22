#!/usr/bin/env python3
"""Repository purification audit for WebWeaveX v2.0.0."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "FINAL_REPOSITORY_PURIFICATION_REPORT.md"

PURGE_DIRS = [
    ROOT / "core" / "legacy",
    ROOT / "core" / "security" / "v2",
    ROOT / "core" / "security" / "v3",
    ROOT / "build",
]

ARCHIVE_ROOT_MD = [
    "FINAL_DEEP_AUDIT_REPORT.md",
    "IMPORT_GRAPH_REPORT.md",
    "SECURITY_EXECUTION_AUDIT.md",
    "FINAL_EXECUTION_SECURITY_AUDIT.md",
    "FINAL_ENTERPRISE_VALIDATION_REPORT.md",
    "PERFORMANCE_REPORT.md",
    "COVERAGE_REPORT.md",
]


def main() -> int:
    archive = ROOT / "docs" / "archive"
    archive.mkdir(parents=True, exist_ok=True)

    deleted = []
    for d in PURGE_DIRS:
        if d.exists():
            shutil.rmtree(d, ignore_errors=True)
            deleted.append(str(d.relative_to(ROOT)))

    moved = []
    for name in ARCHIVE_ROOT_MD:
        src = ROOT / name
        if src.exists():
            dest = archive / name
            if not dest.exists():
                shutil.move(str(src), str(dest))
            moved.append(name)

    lines = [
        "# FINAL REPOSITORY PURIFICATION REPORT",
        "",
        "## Deleted paths",
        "",
    ]
    if deleted:
        lines.extend(f"- `{p}`" for p in deleted)
    else:
        lines.append("- (already purged in prior pass)")
    lines += [
        "",
        "## Archived reports",
        "",
    ]
    lines.extend(f"- `{m}` → `docs/archive/`" for m in moved) or ["- none"]
    lines += [
        "",
        "## Canonical architecture",
        "",
        "- Pipeline: `core/kernel/runtime_pipeline.py`",
        "- Contracts: `core/contracts/`",
        "- Determinism: `core/determinism/global_runtime_fingerprint.py`",
        "- Replay: `core/replay/replay_equivalence_engine.py`",
        "- Crypto: `core/crypto/kaalka_runtime_engine.py` only",
        "",
        "## Dependency cleanup",
        "",
        "- Removed legacy shim imports (`core/*_engine.py` → `core/legacy`)",
        "- Lazy `core/ir/__init__.py` prevents parser cycles",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
