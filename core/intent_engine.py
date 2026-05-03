"""
WebWeaveX Intent Engine (Phase 2)

Purpose:
- Convert user input into structured intent
- Deterministic and rule-based
- No external dependencies

STRICT RULES:
- No randomness
- No external calls
- No side effects
"""

from typing import Dict, Any


INTENT_TYPES = {
    "calculator": "ui_app",
    "weather": "information",
    "news": "information",
    "stock": "information",
    "code": "code_request",
    "api": "api_request",
}


def _detect_type(text: str) -> str:
    text_lower = text.lower()

    for keyword, intent_type in INTENT_TYPES.items():
        if keyword in text_lower:
            return intent_type

    return "generic"


def _extract_keywords(text: str) -> list[str]:
    words = text.lower().split()
    return [w for w in words if len(w) > 2]


def _estimate_complexity(text: str) -> str:
    length = len(text.split())

    if length <= 2:
        return "low"
    elif length <= 5:
        return "medium"
    else:
        return "high"


def resolve_intent(user_input: str) -> Dict[str, Any]:
    """
    Convert raw input into structured intent.

    Args:
        user_input (str)

    Returns:
        dict
    """

    if not isinstance(user_input, str):
        raise TypeError("user_input must be a string")

    if user_input.strip() == "":
        raise ValueError("user_input cannot be empty")

    intent = {
        "type": _detect_type(user_input),
        "goal": user_input,
        "keywords": _extract_keywords(user_input),
        "complexity": _estimate_complexity(user_input),
        "version": "v1_phase_2"
    }

    return intent


def validate_intent_engine() -> bool:
    """
    Validation function for intent engine.
    """

    test_input = "calculator app"

    result = resolve_intent(test_input)

    required_keys = ["type", "goal", "keywords", "complexity", "version"]

    if not isinstance(result, dict):
        raise RuntimeError("Intent output is not dict")

    for key in required_keys:
        if key not in result:
            raise RuntimeError(f"Missing key: {key}")

    if result["goal"] != test_input:
        raise RuntimeError("Goal mismatch")

    if not isinstance(result["keywords"], list):
        raise RuntimeError("Keywords must be list")

    return True


if __name__ == "__main__":
    ok = validate_intent_engine()
    print("INTENT ENGINE VALIDATION:", "PASS" if ok else "FAIL")