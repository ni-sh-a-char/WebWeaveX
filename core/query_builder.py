"""
WebWeaveX Query Builder (Phase 4)

Purpose:
    Convert intent + source plan into search queries
    Deterministic and rule-based

STRICT RULES:
    No randomness
    No external calls
    No side effects
"""

from typing import Dict, Any, List


def _build_base_query(intent: Dict[str, Any]) -> str:
    return intent.get("goal", "").strip()


def _enhance_for_source(base_query: str, source: str) -> str:
    """
    Modify query based on source type.
    """

    if source == "github":
        return f"{base_query} implementation github"

    elif source == "stackoverflow":
        return f"{base_query} error solution stackoverflow"

    elif source == "codepen":
        return f"{base_query} javascript demo codepen"

    elif source == "docs":
        return f"{base_query} official documentation"

    elif source == "news":
        return f"{base_query} latest news"

    elif source == "web":
        return base_query

    return base_query


def build_queries(intent: Dict[str, Any], source_plan: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build queries for each source.

    Args:
        intent (dict)
        source_plan (dict)

    Returns:
        dict
    """

    if not isinstance(intent, dict):
        raise TypeError("intent must be a dict")

    if not isinstance(source_plan, dict):
        raise TypeError("source_plan must be a dict")

    if "sources" not in source_plan:
        raise ValueError("source_plan missing 'sources'")

    base_query = _build_base_query(intent)
    original_input = intent.get("goal", "")

    import hashlib
    input_signature = hashlib.sha256(original_input.encode()).hexdigest()[:12]

    queries = []

    seen = set()

    for item in source_plan["sources"]:
        source = item.get("source")

        if not source:
            continue

        query = _enhance_for_source(base_query, source)

        if query not in seen:
            queries.append({
                "source": source,
                "query": query,
                "priority": item.get("priority", 0),
                "input_signature": input_signature
            })
            seen.add(query)

    expansion_suffixes = [
        "tutorial", "example", "github",
        "how to build", "implementation",
        "architecture", "best practices"
    ]
    for suffix in expansion_suffixes:
        exp_query = f"{base_query} {suffix}"
        exp_enhanced = _enhance_for_source(exp_query, "web")
        if exp_enhanced not in seen:
            queries.append({
                "source": "web",
                "query": exp_enhanced,
                "priority": 10,
                "input_signature": input_signature
            })
            seen.add(exp_enhanced)

    result = {
        "base_query": base_query,
        "original_input": original_input,
        "input_signature": input_signature,
        "queries": queries,
        "total_queries": len(queries),
        "version": "v1_phase_4"
    }

    return result


def validate_query_builder() -> bool:
    """
    Validation for query builder.
    """

    test_intent = {
        "type": "ui_app",
        "goal": "calculator app",
        "keywords": ["calculator", "app"],
        "complexity": "medium",
        "version": "v1_phase_2"
    }

    test_source_plan = {
        "intent_type": "ui_app",
        "sources": [
            {"source": "github", "priority": 1},
            {"source": "codepen", "priority": 2},
            {"source": "stackoverflow", "priority": 3}
        ],
        "total_sources": 3,
        "version": "v1_phase_3"
    }

    result = build_queries(test_intent, test_source_plan)

    if not isinstance(result, dict):
        raise RuntimeError("Result is not dict")

    if "queries" not in result:
        raise RuntimeError("Missing queries")

    if len(result["queries"]) == 0:
        raise RuntimeError("No queries generated")

    return True


if __name__ == "__main__":
    ok = validate_query_builder()
    print("QUERY BUILDER VALIDATION:", "PASS" if ok else "FAIL")