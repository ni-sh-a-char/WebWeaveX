from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_execution_reality():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    reality = result["semantic_execution_reality"]
    assert reality["state_convergence"]["converged"] is True
    assert reality["deterministic"] is True
    assert "execution_pressure" in reality
