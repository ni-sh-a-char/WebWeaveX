from __future__ import annotations

from typing import Any, Dict, List

from core.documents.semantic_role_engine import assign_semantic_roles


def model_intent_flow(text: str) -> Dict[str, Any]:
    roles = assign_semantic_roles(text)
    chain: List[Dict[str, str]] = []
    for r in roles.get("roles", []):
        chain.append({"line": r.get("line"), "intent": r.get("role", "span")})
    return {"intent_chain": chain, "evidence": ["discourse:semantic_roles"]}
