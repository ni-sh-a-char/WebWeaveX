from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_causal_intelligence():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    causal = result["semantic_causal_intelligence"]
    assert causal["runtime_equilibrium"]["equilibrium"] == "stable"
    assert causal["deterministic"] is True
    assert "causality_graph" in causal
