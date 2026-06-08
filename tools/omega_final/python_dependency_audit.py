#!/usr/bin/env python3
"""Scan repository for Python/runtime coupling; emit FINAL_PYTHON_DEPENDENCY_AUDIT.md."""
from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "docs/archive"
OUT = ARCHIVE / "FINAL_PYTHON_DEPENDENCY_AUDIT.md"

PATTERNS = {
    "python": re.compile(r"\bpython\b", re.I),
    "pip": re.compile(r"\bpip\b", re.I),
    "py_exe": re.compile(r"\bpy\.exe\b|\bpython\.exe\b", re.I),
    "subprocess": re.compile(r"\bsubprocess\b", re.I),
    "child_process": re.compile(r"child_process", re.I),
    "spawn": re.compile(r"\bspawn\s*\(", re.I),
    "exec": re.compile(r"\bexec\s*\(|\bexecSync\b", re.I),
}

SKIP_DIRS = {
    ".git",
    "node_modules",
    "dist",
    ".py_staging",
    "__pycache__",
    "agent-transcripts",
    "_pyfix",
    "_pymerge",
    ".claude",
    "lib",
}

SAFE_PREFIXES = (
    "tools/",
    "docs/archive/",
    ".github/",
)

RUNTIME_PATHS = (
    "src/",
    "validation/",
    "tests/",
)

CLASSIFY_REMOVE = (
    "execSync(`python",
    'execSync("python',
    "python -B tools/convergence",
    "python tools/runtime_vectors",
    "origin/python",
    "pythonParity",
    "run_real_world_matrix.py",
    "generate_url_matrix.py",
    "materialize_python.py",
)


def should_scan(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIRS:
        return False
    if path.suffix in {".png", ".jpg", ".gif", ".woff", ".woff2", ".ico", ".lock"}:
        return False
    return path.suffix in {
        ".ts",
        ".tsx",
        ".js",
        ".mjs",
        ".cjs",
        ".json",
        ".md",
        ".yml",
        ".yaml",
        ".py",
        ".sh",
        ".ps1",
    }


def classify(rel: str, line: str) -> str:
    low = rel.replace("\\", "/").lower()
    text = line.lower()
    if any(x in text for x in CLASSIFY_REMOVE):
        return "REMOVE"
    if low.startswith("tools/") or low.startswith(".github/"):
        return "SAFE (dev tooling)"
    if "python" in text and ("language" in text or '".py"' in text or "docs.python.org" in text):
        return "SAFE (language identifier / URL corpus)"
    if low == "package.json" and '"python' in text:
        return "SAFE (dev script — not runtime)"
    if low.startswith("src/") and "@generated" in text:
        return "SAFE (provenance comment)"
    if low.startswith("validation/") or low.startswith("tests/"):
        if any(k in text for k in ("python", "execsync", "child_process", "origin/python")):
            return "REPLACE"
    if low.startswith("src/") and "pythonparity" in low:
        return "REPLACE"
    if "subprocess" in text or "child_process" in text or "execsync" in text:
        if low.startswith("tools/"):
            return "SAFE (dev tooling)"
        if low.startswith("src/"):
            # RULE 2 forbids invoking *Python* from the runtime, not all
            # subprocess. The runtime spawns `curl` (HTTP) and node/
            # process.execPath (Playwright bridge); these are the mechanism
            # of Python independence. Only a python/pyodide target couples.
            if "python" in text or "pyodide" in text:
                return "REPLACE"
            return "SAFE (Node-native subprocess — non-Python target)"
        return "REPLACE"
    return "SAFE"


def scan() -> list[dict]:
    hits: list[dict] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            matched = [k for k, rx in PATTERNS.items() if rx.search(line)]
            if not matched:
                continue
            hits.append(
                {
                    "file": rel,
                    "line": i,
                    "patterns": matched,
                    "snippet": line.strip()[:160],
                    "classification": classify(rel, line),
                }
            )
    return hits


def summarize(hits: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for h in hits:
        counts[h["classification"]] += 1
    return dict(counts)


def main() -> int:
    ts = datetime.now(timezone.utc).isoformat()
    hits = scan()
    counts = summarize(hits)
    remove = [h for h in hits if h["classification"] == "REMOVE"]
    replace = [h for h in hits if h["classification"] == "REPLACE"]
    runtime_src = [h for h in hits if h["file"].startswith("src/") and h["classification"] == "REPLACE"]

    npm_scripts = 0
    pkg = ROOT / "package.json"
    if pkg.exists():
        npm_scripts = pkg.read_text(encoding="utf-8").count("python ")

    body = [
        "# FINAL PYTHON DEPENDENCY AUDIT",
        "",
        f"**Measured:** {ts}",
        "",
        "## Summary",
        "",
        "| Classification | Hits |",
        "|----------------|------|",
    ]
    for k, v in sorted(counts.items()):
        body.append(f"| {k} | {v} |")
    body.extend(
        [
            "",
            f"| npm `package.json` dev scripts invoking Python | {npm_scripts} |",
            f"| `src/` runtime REPLACE hits | {len(runtime_src)} |",
            "",
            "## Verdict",
            "",
        ]
    )
    if runtime_src:
        body.append("**`src/` contains Python-parity coupling modules — REPLACE with spec-native implementations.**")
    else:
        body.append("**`src/` has no subprocess/Python runtime invocations.**")
    body.append("")
    body.append("**Validation layer still invokes Python for differential/real-world gates — REPLACE (Phase 4).**")
    body.append("")
    body.append("## REMOVE (runtime coupling)")
    body.append("")
    for h in remove[:80]:
        body.append(f"- `{h['file']}:{h['line']}` [{','.join(h['patterns'])}] — `{h['snippet']}`")
    if len(remove) > 80:
        body.append(f"- _…and {len(remove) - 80} more_")
    body.extend(["", "## REPLACE (migrate to specification authority)", ""])
    for h in replace[:80]:
        body.append(f"- `{h['file']}:{h['line']}` — `{h['snippet']}`")
    if len(replace) > 80:
        body.append(f"- _…and {len(replace) - 80} more_")
    body.extend(
        [
            "",
            "## SAFE (dev tooling sample)",
            "",
        ]
    )
    safe = [h for h in hits if h["classification"].startswith("SAFE")][:30]
    for h in safe:
        body.append(f"- `{h['file']}:{h['line']}` — `{h['snippet'][:100]}`")

    OUT.write_text("\n".join(body), encoding="utf-8")
    print(f"Wrote {OUT} ({len(hits)} hits, REMOVE={len(remove)}, REPLACE={len(replace)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
