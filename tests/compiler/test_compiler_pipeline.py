from core.compiler import compile_semantic_pipeline


def test_compiler_pipeline():
    ir = {
        "edges": [
            {"from": "a", "to": "b"},
            {"from": "a", "to": "b"},
        ]
    }

    result = compile_semantic_pipeline(ir)

    assert result["optimized_ir"]["deterministic"] is True
