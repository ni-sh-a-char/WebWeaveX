"""Generate API_REFERENCE.md from PARITY_MANIFEST.json (source of truth)."""
import json

m = json.load(open('PARITY_MANIFEST.json', encoding='utf-8-sig'))
apis = sorted(m['apis'], key=lambda a: (a['classification'], a['api']))
counts = m['counts']

GROUP_DESC = {
    "Complete": "Parity-certified 3-way (Python == JavaScript == Dart) by "
                "executed proof.",
    "Partial": "Deterministic core certified; a documented network or "
               "live-browser sub-path is excluded by design.",
    "Deferred": "Platform-bound (live page / OS coupling); not part of the "
                "portable surface.",
}

lines = [
    "# WebWeaveX API Reference",
    "",
    "Generated from `PARITY_MANIFEST.json` by `tools/gen_api_reference.py` "
    "— do not edit by hand.",
    "",
    f"**{counts['Complete']} Complete · {counts['Partial']} Partial · "
    f"{counts['Deferred']} Deferred · 0 Missing** "
    "(see CERTIFICATION.md for what each class means and how it is proven).",
    "",
    "Naming: Python/JS export `snake_case`/`camelCase` per language "
    "convention; the Dart symbol is listed explicitly.",
    "",
]
for group in ("Complete", "Partial", "Deferred"):
    rows = [a for a in apis if a['classification'] == group]
    lines += [f"## {group} ({len(rows)})", "", GROUP_DESC[group], "",
              "| API | Dart symbol | Proof |", "|---|---|---|"]
    for a in rows:
        lines.append(
            f"| `{a['api']}` | `{a.get('dart_symbol') or '—'}` | "
            f"{a.get('proof_type') or '—'} |")
    lines.append("")

open('API_REFERENCE.md', 'w', encoding='utf-8').write('\n'.join(lines))
print(f"API_REFERENCE.md: {len(apis)} APIs")
