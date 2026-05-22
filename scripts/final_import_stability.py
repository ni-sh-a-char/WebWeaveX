#!/usr/bin/env python3
"""Final import stability audit."""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
REPORT = ARCHIVE / "FINAL_IMPORT_STABILITY_REPORT.md"


def main() -> int:
    sys.path.insert(0, str(ROOT))
    results = []
    for mod in ("webweavex", "core.kernel.runtime_pipeline", "core.determinism", "core.replay"):
        t0 = time.perf_counter()
        try:
            importlib.invalidate_caches()
            m = importlib.import_module(mod)
            ms = round((time.perf_counter() - t0) * 1000, 2)
            results.append((mod, True, ms, ""))
        except Exception as exc:
            ms = round((time.perf_counter() - t0) * 1000, 2)
            results.append((mod, False, ms, str(exc)))

    t0 = time.perf_counter()
    import webweavex  # noqa: F401

    import_ms = round((time.perf_counter() - t0) * 1000, 2)
    version = webweavex.__version__

    lines = [
        "# FINAL IMPORT STABILITY REPORT",
        "",
        f"- `import webweavex` time: **{import_ms} ms**",
        f"- Version: **{version}**",
        "",
        "## Module checks",
        "",
        "| Module | OK | ms |",
        "|--------|-----|-----|",
    ]
    for mod, ok, ms, err in results:
        lines.append(f"| `{mod}` | {ok} | {ms} |")
        if err:
            lines.append(f"  - Error: {err}")
    lines += [
        "",
        "## Rules",
        "",
        "- No import-time browser launch",
        "- No import-time network I/O",
        "- Lazy IR package exports",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {REPORT}")
    return 0 if all(r[1] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
