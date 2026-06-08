#!/usr/bin/env python3
"""Build FINAL_JS_INVENTORY.json and FINAL_JS_INVENTORY_REPORT.md."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
ARCHIVE = ROOT / "docs/archive"
PROTECTED = ROOT / "tools/convergence/protected_js.txt"

GENERATED_MARK = re.compile(r"@generated|Converted from Python", re.I)
EXPERIMENTAL_MARK = re.compile(r"experimental|TODO|FIXME|placeholder", re.I)


def load_protected() -> set[str]:
    if not PROTECTED.exists():
        return set()
    return {ln.strip().replace("\\", "/") for ln in PROTECTED.read_text(encoding="utf-8").splitlines() if ln.strip()}


def classify(rel: str, text: str, protected: set[str]) -> str:
    key = f"src/{rel}"
    if key in protected:
        return "PROTECTED"
    if GENERATED_MARK.search(text[:800]):
        return "GENERATED"
    if EXPERIMENTAL_MARK.search(text[:1200]):
        return "EXPERIMENTAL"
    if "/_" in rel or rel.startswith("_"):
        return "PRODUCTION"
    return "PRODUCTION"


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    protected = load_protected()
    modules: list[dict] = []
    counts: dict[str, int] = {}

    for path in sorted(SRC.rglob("*.ts")):
        rel = str(path.relative_to(SRC)).replace("\\", "/")
        text = path.read_text(encoding="utf-8", errors="replace")
        has_export = bool(re.search(r"^export ", text, re.M))
        has_nocheck = "@ts-nocheck" in text
        kind = classify(rel, text, protected)
        counts[kind] = counts.get(kind, 0) + 1
        modules.append(
            {
                "path": f"src/{rel}",
                "classification": kind,
                "has_export": has_export,
                "ts_nocheck": has_nocheck,
                "lines": text.count("\n") + 1,
            }
        )

    payload = {"measured_at": ts, "total": len(modules), "counts": counts, "modules": modules}
    (ARCHIVE / "FINAL_JS_INVENTORY.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    report = [
        "# FINAL JS INVENTORY REPORT",
        "",
        f"**Measured:** {ts}",
        "",
        "| Classification | Count |",
        "|----------------|-------|",
    ]
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        report.append(f"| {k} | {v} |")
    report.extend(
        [
            "",
            f"**Total TypeScript modules:** {len(modules)}",
            f"**Protected (hand-written):** {counts.get('PROTECTED', 0)}",
            f"**Generated (py2ts port):** {counts.get('GENERATED', 0)}",
            f"**@ts-nocheck:** {sum(1 for m in modules if m['ts_nocheck'])}",
            "",
            "Evidence: `docs/archive/FINAL_JS_INVENTORY.json`",
            "",
        ]
    )
    (ARCHIVE / "FINAL_JS_INVENTORY_REPORT.md").write_text("\n".join(report), encoding="utf-8")
    print(f"Inventory: {len(modules)} modules, {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
