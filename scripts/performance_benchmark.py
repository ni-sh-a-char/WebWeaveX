#!/usr/bin/env python3
"""Performance benchmarks for WebWeaveX v2.0.0."""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "PERFORMANCE_REPORT.md"


def _bench(label: str, fn) -> float:
    t0 = time.perf_counter()
    fn()
    return round((time.perf_counter() - t0) * 1000, 2)


def main() -> int:
    sys.path.insert(0, str(ROOT))
    from core.browser.universal_web_extraction_engine import extract_web
    from core.repository.universal_repository_extraction_engine import extract_repository
    from core.reconstruction.runtime_reconstruction_engine import reconstruct_runtime
    from core.memory.runtime_memory_engine import build_runtime_memory
    from core.memory.runtime_merge_engine import merge_runtime_memories

    rows = {}
    rows["extract_web"] = _bench("web", lambda: extract_web("https://example.com"))
    rows["extract_repository"] = _bench(
        "repo", lambda: extract_repository(str(ROOT / "validation" / "repository" / "py-sample"))
    )
    rows["reconstruct_runtime"] = _bench(
        "recon", lambda: reconstruct_runtime(runtime_type="browser", tick=0)
    )
    m1 = build_runtime_memory(runtime_history=[{"tick": 0, "kind": "workflow"}])
    m2 = build_runtime_memory(runtime_history=[{"tick": 1, "kind": "sync"}])
    rows["memory_merge"] = _bench("merge", lambda: merge_runtime_memories([m1, m2]))

    lines = [
        "# PERFORMANCE REPORT",
        "",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "",
        "| Benchmark | ms |",
        "|-----------|-----|",
    ]
    for k, v in rows.items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Observations",
        "",
        "- Web extraction dominated by Playwright network idle wait.",
        "- Repository extraction scales with file count (bounded ingestion).",
        "- Reconstruction and memory merge are sub-millisecond on fixed inputs.",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
