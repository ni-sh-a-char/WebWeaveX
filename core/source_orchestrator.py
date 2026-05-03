"""
WebWeaveX Source Orchestrator (Phase 3)

Purpose:
    Decide where to fetch data from
    Based on structured intent
    Deterministic and rule-based

STRICT RULES:
    No randomness
    No external calls
    No side effects
"""

from typing import Dict, Any, List


SOURCE_MAP = {
    "ui_app": ["github", "codepen", "stackoverflow"],
    "code_request": ["github", "stackoverflow"],
    "api_request": ["docs", "github"],
    "information": ["web", "news"],
    "generic": ["web"],
}


def _select_sources(intent_type: str) -> List[str]:
    return SOURCE_MAP.get(intent_type, ["web"])


def _assign_priority(sources: List[str]) -> List[Dict[str, Any]]:
    return [
        {"source": src, "priority": i + 1}
        for i, src in enumerate(sources)
    ]


def build_source_plan(intent: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a deterministic source execution plan.

    Args:
        intent (dict): Output from intent_engine

    Returns:
        dict: Source plan
    """

    if not isinstance(intent, dict):
        raise TypeError("intent must be a dictionary")

    if "type" not in intent:
        raise ValueError("intent missing 'type' field")

    intent_type = intent["type"]

    sources = _select_sources(intent_type)
    prioritized = _assign_priority(sources)

    plan = {
        "intent_type": intent_type,
        "sources": prioritized,
        "total_sources": len(prioritized),
        "version": "v1_phase_3"
    }

    return plan


def validate_source_orchestrator() -> bool:
    """
    Validation for source orchestrator.
    """

    test_intent = {
        "type": "ui_app",
        "goal": "calculator",
        "keywords": ["calculator"],
        "complexity": "low",
        "version": "v1_phase_2"
    }

    plan = build_source_plan(test_intent)

    if not isinstance(plan, dict):
        raise RuntimeError("Plan is not dict")

    required_keys = ["intent_type", "sources", "total_sources", "version"]

    for key in required_keys:
        if key not in plan:
            raise RuntimeError(f"Missing key: {key}")

    if not isinstance(plan["sources"], list):
        raise RuntimeError("Sources must be list")

    if len(plan["sources"]) == 0:
        raise RuntimeError("No sources assigned")

    return True


if __name__ == "__main__":
    ok = validate_source_orchestrator()
    print("SOURCE ORCHESTRATOR VALIDATION:", "PASS" if ok else "FAIL")