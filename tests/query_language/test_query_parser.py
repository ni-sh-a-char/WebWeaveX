from core.query_language import parse_semantic_query


def test_query_parser():
    result = parse_semantic_query(
        "SELECT id WHERE type = service LIMIT 5"
    )

    assert result["limit"] == 5
