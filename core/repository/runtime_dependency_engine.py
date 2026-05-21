from __future__ import annotations

from typing import Any, Dict, List, Optional


def resolve_runtime_dependencies(parsed: Dict[str, Any], text_fallback: str = "") -> Dict[str, Any]:
    """Parser-first runtime deps; bounded regex fallback for requirements.txt."""
    deps: List[str] = []
    evidence: List[str] = []
    if parsed:
        d = parsed.get("dependencies", {}) or {}
        deps = list(d.get("dependencies", []) or [])
        if deps:
            evidence.append("parser:dependencies")
        runtime = parsed.get("runtime", {}) or {}
        for k in ("packages", "modules"):
            items = runtime.get(k, []) or []
            if items:
                deps.extend(str(x) for x in items[:100])
                evidence.append(f"parser:runtime_{k}")
    if not deps and text_fallback:
        import re

        for m in re.finditer(r"^([A-Za-z0-9_.\-]+)\s*(?:==|>=)", text_fallback, re.M):
            deps.append(m.group(1))
            evidence.append("fallback:requirements_line")
    return {
        "dependencies": sorted(set(deps))[:200],
        "evidence": sorted(set(evidence)),
        "parser_first": bool(parsed and evidence and evidence[0].startswith("parser")),
    }
