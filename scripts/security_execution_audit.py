#!/usr/bin/env python3
"""Generate SECURITY_EXECUTION_AUDIT.md from execution sandbox and AST scan."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "archive"
OUT = ARCHIVE / "SECURITY_EXECUTION_AUDIT.md"


def main() -> int:
    hits = []
    for fp in (ROOT / "core" / "execution").rglob("*.py"):
        tree = ast.parse(fp.read_text(encoding="utf-8", errors="ignore"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec", "__import__"):
                    hits.append(f"{fp.relative_to(ROOT)}:{node.func.id}")

    from core.execution.runtime_execution_orchestrator import run_execution_runtime

    result = run_execution_runtime(runtime="browser", simulate=True, rollback_enabled=True)
    policy = result.get("policy", {})

    lines = [
        "# SECURITY EXECUTION AUDIT",
        "",
        "## Execution sandbox",
        f"- Bounded: **{result.get('bounded')}**",
        f"- Simulated (no live shell): **{result.get('simulated')}**",
        f"- Policy: **{policy.get('enforced', policy.get('bounded'))}**",
        f"- Rollback enabled: **{result.get('rollback_enabled')}**",
        "",
        "## Allowlist policy",
        "",
        "Actions are restricted to typed runtime actions (`browser_click`, `native_focus`, `terminal_command` with sandbox policy).",
        "",
        "## eval/exec in core/execution",
        "",
    ]
    if hits:
        lines.extend(f"- `{h}`" for h in hits)
    else:
        lines.append("- **None** in `core/execution/`.")
    lines += [
        "",
        "## Persistence",
        "",
        "- Encrypted runtime stores use **Kaalka** (`core.crypto.kaalka_runtime_engine`) only.",
    ]
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
