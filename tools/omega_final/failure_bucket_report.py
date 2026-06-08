#!/usr/bin/env python3
"""Generate docs/archive/FINAL_FAILURE_BUCKET_REPORT.md from live certification matrix."""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/archive/generated_module_matrix.json"
OUT = ROOT / "docs/archive/FINAL_FAILURE_BUCKET_REPORT.md"


def classify_error(err: str, module: str) -> tuple[str, str]:
    e = err or ""
    el = e.lower()
    if "transform failed" in el or "syntax error" in el:
        return "Transform", "py2ts emit / invalid TS syntax"
    if "barrel_export" in el:
        return "Export", "package index.ts missing re-exports"
    if "cannot find module" in el or "does not provide an export" in el or "cannot find package" in el:
        return "Import", "module resolution / missing npm export"
    if "output_or_state_mismatch" in el:
        return "Behavioral", "executable but output/state/hash differs"
    if "not iterable" in el or "foreach is not a function" in el or "items is not" in el or "values is not" in el:
        return "Iteration", "Python iteration semantics not mirrored"
    if "winerror 123" in el or "filename, directory name" in el:
        return "Runtime", "URL/path used as filesystem path in probe"
    if "beautifulsoup" in el or "hashlib" in el or "pathlib" in el:
        return "Import", "Python-only library referenced in generated TS"
    if "serialization" in el or "json" in el and "parse" in el:
        return "Serialization", "JSON/canonical serialization drift"
    if "memory" in el and "drift" in el:
        return "Memory", "memory state mismatch"
    if "replay" in el:
        return "Replay", "replay state mismatch"
    if "workflow" in el:
        return "Workflow", "workflow state mismatch"
    if "semantic" in el and "mismatch" in el:
        return "Semantic", "semantic state mismatch"
    if "distributed" in el:
        return "Distributed", "distributed state mismatch"
    if "browser" in el or "dom" in el:
        return "Browser", "browser/DOM extraction drift"
    if el.startswith("py=none js="):
        msg = e.split("js=", 1)[1][:120]
        if " is not defined" in msg:
            return "Transform", f"undefined symbol: {msg.split(' is not defined')[0][-40:]}"
        if "transform failed" in msg.lower():
            return "Transform", "nested transform failure"
        if "cannot find" in msg.lower() or "does not provide" in msg.lower():
            return "Import", msg[:80]
        return "Runtime", msg[:80]
    if "python_import" in el:
        return "Import", "Python module import failed during probe"
    if "timeout" in el:
        return "Runtime", "probe timeout"
    if "missing_ts" in el:
        return "Transform", "missing TypeScript counterpart"
    return "Runtime", (e[:100] if e else "unknown")


def main() -> int:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    modules = data.get("modules", [])
    fails = [m for m in modules if m.get("status") == "FAIL"]
    untested = [m for m in modules if m.get("status") == "UNTESTED"]
    passes = [m for m in modules if m.get("status") == "PASS"]

    buckets: dict[str, list[dict]] = defaultdict(list)
    root_causes: dict[str, str] = {}

    for row in fails:
        bucket, root = classify_error(str(row.get("error") or ""), row.get("module", ""))
        root_causes[bucket] = root
        buckets[bucket].append(row)

    ranked = sorted(buckets.items(), key=lambda kv: -len(kv[1]))

    lines = [
        "# WebWeaveX Final Failure Bucket Report",
        "",
        f"**Measured at:** {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Certification snapshot",
        "",
        "```text",
        f"PASS      = {len(passes)}",
        f"FAIL      = {len(fails)}",
        f"UNTESTED  = {len(untested)}",
        f"TOTAL     = {len(modules)}",
        "STATUS    = NOT ISSUED",
        "```",
        "",
        "## Ranked FAIL buckets (fix largest first)",
        "",
        "| Rank | Bucket | Count | Root cause |",
        "|------|--------|------:|------------|",
    ]
    for i, (bucket, rows) in enumerate(ranked, 1):
        lines.append(f"| {i} | **{bucket}** | {len(rows)} | {root_causes.get(bucket, '')} |")

    lines.extend(["", "## Bucket detail", ""])
    for bucket, rows in ranked:
        lines.append(f"### {bucket} ({len(rows)})")
        lines.append("")
        lines.append(f"**Root cause:** {root_causes.get(bucket, '')}")
        lines.append("")
        # sub-pattern counts
        sub: dict[str, int] = defaultdict(int)
        for r in rows:
            e = str(r.get("error") or "")[:100]
            if "js=" in e:
                key = e.split("js=", 1)[1][:60]
            else:
                key = e[:60]
            sub[key] += 1
        lines.append("**Top error patterns:**")
        lines.append("")
        for pat, cnt in sorted(sub.items(), key=lambda x: -x[1])[:12]:
            lines.append(f"- `{cnt}` — `{pat}`")
        lines.append("")
        lines.append("**Affected modules (sample):**")
        lines.append("")
        for r in rows[:25]:
            lines.append(f"- `{r.get('module')}` — `{str(r.get('error') or '')[:90]}`")
        if len(rows) > 25:
            lines.append(f"- … and {len(rows) - 25} more")
        lines.append("")

    if untested:
        lines.extend(["## UNTESTED breakdown", ""])
        uc = defaultdict(int)
        for u in untested:
            uc[str(u.get("error") or "none")] += 1
        for k, v in sorted(uc.items(), key=lambda x: -x[1]):
            lines.append(f"- `{v}` — `{k}`")
        lines.append("")

    lines.extend(
        [
            "## Fix priority order",
            "",
            "1. **Import** — `npm install`, registry exports, protected hand-written barrels",
            "2. **Transform** — py2ts + replace chronic failures with native TS",
            "3. **Iteration** — `pyCompat` helpers everywhere",
            "4. **Export** — align `index.ts` with Python `__init__.py`",
            "5. **Behavioral** — native implementations per package",
            "6. **Runtime** — probe args, path/URL normalization",
            "",
            "**Rule:** Fix root causes globally, not single modules.",
            "",
        ]
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT} ({len(fails)} FAIL, {len(ranked)} buckets)")
    for bucket, rows in ranked[:8]:
        print(f"  {len(rows):4} {bucket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
