from core.index import SemanticIndex


def test_semantic_index():

    idx = SemanticIndex()

    idx.add(
        "symbol",
        {"id": "x"},
    )

    r = idx.search(
        "symbol",
    )

    assert len(r) == 1
