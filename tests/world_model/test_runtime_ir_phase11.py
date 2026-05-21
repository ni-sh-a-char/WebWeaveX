from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_world_model():
    source = "def run():\n    return 1\n"
    result = compile_runtime_ir(
        source=source,
        path="main.py",
        graph={
            "repository_irs": [
                {
                    "path": "main.py",
                    "semantic_ast": {
                        "symbols": [{"name": "run"}],
                        "imports": [],
                    },
                }
            ],
        },
    )
    assert result["repository_world_model"]["file_count"] == 1
    assert "semantic_architecture_graph" in result
    assert result["semantic_impact_analysis"]["target"] == "main.py"
