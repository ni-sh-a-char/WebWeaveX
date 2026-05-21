from core.semantic.entity_extraction_engine import extract_semantic_entities


def test_entity_determinism():
    text = "Acme Corp API service workflow user kubernetes deploy"

    first = extract_semantic_entities(text)
    second = extract_semantic_entities(text)

    assert first == second
    assert first["entities"]
