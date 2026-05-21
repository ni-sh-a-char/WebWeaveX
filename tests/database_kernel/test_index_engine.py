from core.database.semantic_index_engine import SemanticIndex


def test_index_lookup():
    index = SemanticIndex()

    index.insert(
        "service",
        {"id": "api"},
    )

    result = index.lookup("service")

    assert len(result) == 1
