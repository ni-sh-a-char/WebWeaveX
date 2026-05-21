from core.semantic.entity_extraction_engine import extract_semantic_entities
from core.semantic.semantic_graph_engine import build_semantic_graph


def test_semantic_graph_stability():
    entities = extract_semantic_entities("api service metric user")

    first = build_semantic_graph(entities["entities"], entities["relations"])
    second = build_semantic_graph(entities["entities"], entities["relations"])

    assert first == second
    assert first["nodes"]
