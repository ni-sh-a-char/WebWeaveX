"""
WebWeaveX Reasoning Engine (Phase V4)

Purpose:
    Convert semantics into actionable reasoning and strategy
    - Strategy determination
    - Approach planning
    - Requirement extraction

STRICT RULES:
    - Pure rule-based (no AI)
    - Deterministic
    - No external dependencies
"""

from typing import Dict, Any, List


ENTITY_STRATEGIES = {
    "system": "backend_service",
    "application": "application_deployment",
    "container": "container_deployment",
    "storage": "data_management",
    "backend": "backend_service",
    "frontend": "frontend_deployment",
    "framework": "framework_integration",
    "language": "language_setup",
    "runtime": "runtime_configuration",
    "protocol": "protocol_implementation",
    "query_language": "query_execution",
    "auth": "authentication_setup",
    "actor": "user_management",
    "state": "state_management",
    "credential": "security_setup",
    "orchestration": "orchestration_config",
    "infrastructure": "infrastructure_setup",
    "server": "server_configuration",
    "os": "os_configuration"
}


def _determine_strategy(entities: List[Dict]) -> str:
    """Determine strategy from dominant entity category."""
    if not entities:
        return "general"

    categories = {}
    for entity in entities:
        cat = entity.get("category", "unknown")
        categories[cat] = categories.get(cat, 0) + 1

    if not categories:
        return "general"

    dominant = max(categories.items(), key=lambda x: x[1])[0]
    return ENTITY_STRATEGIES.get(dominant, "general")


def _determine_approach(actions: List[Dict], action_pairs: List[Dict], user_input: str = "") -> List[str]:
    """Determine execution approach from actions."""
    action_types = set()

    for pair in action_pairs:
        if pair.get("normalized_action"):
            action_types.add(pair["normalized_action"])

    for action in actions:
        if action.get("text"):
            action_types.add(action["text"])

    if not action_types and user_input:
        user_lower = user_input.lower()
        if any(w in user_lower for w in ["build", "create", "make"]):
            action_types.add("build")
        if any(w in user_lower for w in ["install", "setup"]):
            action_types.add("install")
        if any(w in user_lower for w in ["run", "start", "execute"]):
            action_types.add("run")
        if any(w in user_lower for w in ["deploy"]):
            action_types.add("deploy")

    if not action_types:
        return ["analyze", "build", "run"]

    approach = []

    if any(a in action_types for a in ["install", "setup", "configure", "install"]):
        approach.append("install")
    if any(a in action_types for a in ["build", "create", "make"]):
        approach.append("build")
    if any(a in action_types for a in ["execute", "run", "start"]):
        approach.append("run")
    if any(a in action_types for a in ["deploy", "publish"]):
        approach.append("deploy")
    if any(a in action_types for a in ["validate", "verify", "check"]):
        approach.append("verify")

    if not approach:
        approach = ["build", "run"]

    return approach


def _extract_requirements(entities: List[Dict], action_pairs: List[Dict], user_input: str = "") -> List[str]:
    """Extract requirements from entities."""
    requirements = []

    for pair in action_pairs:
        entity = pair.get("entity", "")
        if entity:
            requirements.append(entity)

    for entity in entities:
        text = entity.get("text", "")
        cat = entity.get("category", "")
        if cat in ["framework", "language", "runtime"]:
            requirements.append(text)

    if user_input:
        req_map = {
            "api": ["routing", "endpoints", "server"],
            "app": ["ui", "components", "state"],
            "docker": ["dockerfile", "image", "container"],
            "login": ["auth", "session", "token"],
            "rest": ["restful", "endpoints", "http"]
        }
        for key, vals in req_map.items():
            if key in user_input.lower():
                requirements.extend(vals)

    return list(set(requirements))[:10]


def _build_reasoning_strategy(semantics: Dict[str, Any], user_input: str = "") -> Dict[str, Any]:
    """Build complete reasoning strategy from semantics."""
    entities = semantics.get("entities", [])
    actions = semantics.get("actions", [])
    action_pairs = semantics.get("action_pairs", [])

    if not entities and user_input:
        from core.semantic_engine import _extract_entities_from_input
        fallback = _extract_entities_from_input(user_input)
        entities = fallback.get("entities", [])
        actions = fallback.get("actions", [])
        action_pairs = fallback.get("action_pairs", [])

    strategy = _determine_strategy(entities)
    approach = _determine_approach(actions, action_pairs, user_input)
    requirements = _extract_requirements(entities, action_pairs, user_input)

    return {
        "strategy": strategy,
        "approach": approach,
        "requirements": requirements,
        "confidence": min(1.0, (len(entities) * 0.1 + len(actions) * 0.15 + len(action_pairs) * 0.2)),
        "version": "v4_reasoning"
    }


def run_reasoning(semantics: Dict[str, Any], user_input: str = "") -> Dict[str, Any]:
    """Main reasoning entry point."""
    if not isinstance(semantics, dict):
        if user_input:
            return _build_reasoning_strategy({}, user_input)
        return _empty_reasoning()

    result = _build_reasoning_strategy(semantics, user_input)

    if not result.get("approach"):
        result["approach"] = ["analyze", "build", "run"]

    if not result.get("strategy"):
        result["strategy"] = "general"

    if result.get("confidence", 0) == 0 and user_input:
        result["confidence"] = 0.1

    return result


def _empty_reasoning() -> Dict[str, Any]:
    return {
        "strategy": "general",
        "approach": ["analyze", "build", "run"],
        "requirements": [],
        "confidence": 0.1,
        "version": "v4_reasoning"
    }


def validate_reasoning_engine() -> bool:
    """Validate reasoning engine."""
    test_semantics = {
        "entities": [
            {"text": "api", "category": "system"},
            {"text": "python", "category": "language"},
            {"text": "flask", "category": "framework"}
        ],
        "actions": [
            {"text": "build", "type": "verb"},
            {"text": "deploy", "type": "verb"}
        ],
        "action_pairs": [
            {"action": "build", "normalized_action": "build", "entity": "api"}
        ]
    }

    result = run_reasoning(test_semantics, "build REST API")

    if not isinstance(result, dict):
        return False

    if "strategy" not in result:
        return False

    return True


if __name__ == "__main__":
    ok = validate_reasoning_engine()
    print("REASONING ENGINE VALIDATION:", "PASS" if ok else "FAIL")