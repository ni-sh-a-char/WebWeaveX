from __future__ import annotations

from typing import Any, Dict

from core.parsers import parse_source

_INFRA_DEPS = frozenset(
    {"docker", "kubernetes", "terraform", "helm", "ansible", "k8s", "compose"}
)


def map_infrastructure(text: str, path: str = "") -> Dict[str, Any]:
    parsed = parse_source(text or "", path=path)
    deps = [str(d).lower() for d in parsed.get("dependencies", {}).get("dependencies", [])]
    imports = [str(i).lower() for i in parsed.get("symbols", {}).get("imports", [])]
    evidence = deps + imports
    infra = sorted({k for k in _INFRA_DEPS if any(k in e for e in evidence)})
    if not infra:
        src = (text or "").lower()
        infra = sorted({k for k in _INFRA_DEPS if k in src})
        evidence_kind = "text_fallback"
    else:
        evidence_kind = "parser_dependencies"
    return {"infrastructure": infra, "evidence": evidence_kind}
