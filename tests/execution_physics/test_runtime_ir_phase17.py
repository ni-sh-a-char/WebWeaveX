from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_execution_physics():
    result = compile_runtime_ir(
        source="def run():\n    return 1\n",
        path="main.py",
    )
    physics = result["semantic_execution_physics"]
    assert physics["execution_physics"]["physics_state"] == "stable"
    assert physics["deterministic"] is True
    assert "runtime_energy" in physics
