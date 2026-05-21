from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_semantic_autonomy():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    autonomy = result["semantic_autonomy"]
    assert autonomy["goal"]["resolved"] is True
    assert autonomy["decomposition"]["count"] > 0
    assert autonomy["deterministic"] is True
