from core.semantic.domain_classification_engine import classify_semantic_domain


def test_domain_stability():
    text = "analytics dashboard kpi metrics report subscription billing"

    first = classify_semantic_domain(text)
    second = classify_semantic_domain(text)

    assert first == second
    assert first["domain"] in first["scores"] or first["domain"] == "analytics"
