from core.query_language import (
    parse_semantic_query,
    build_query_ast,
    plan_semantic_query,
    optimize_semantic_query,
    execute_semantic_plan,
)


def test_query_executor_pipeline():
    parsed = parse_semantic_query("SELECT id WHERE type = service LIMIT 10")
    ast = build_query_ast(parsed)
    plan = optimize_semantic_query(plan_semantic_query(ast))
    result = execute_semantic_plan(
        plan,
        [
            {"id": "a", "type": "service"},
            {"id": "b", "type": "database"},
        ],
    )
    assert result["count"] == 1
