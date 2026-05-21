from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_semantic_engineering():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    engineering = result["semantic_engineering"]
    assert engineering["diagnostics"]["healthy"] is True
    assert engineering["deterministic"] is True
    assert "engineering_graph" in engineering
