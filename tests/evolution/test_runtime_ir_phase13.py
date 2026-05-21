from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_semantic_evolution():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    evolution = result["semantic_evolution"]
    assert evolution["stability"]["stable"] is True
    assert evolution["deterministic"] is True
    assert "evolution" in evolution
