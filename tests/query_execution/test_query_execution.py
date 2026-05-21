from core.query.semantic_query_execution_engine import (
    execute_semantic_query,
)


def test_query_execution():
    result = execute_semantic_query(
        nodes=[
            {"id": "a", "type": "service"},
            {"id": "b", "type": "database"},
        ],
        filters={"type": "service"},
    )

    assert result["count"] == 1
