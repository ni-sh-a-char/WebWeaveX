from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_phase8_fields():
    ir = compile_runtime_ir(
        source="x = 1",
        path="main.py",
        graph={"nodes": [{"id": "api", "type": "service"}]},
    )
    assert "compiler_pipeline" in ir
    assert "distributed_schedule" in ir
    assert ir["distributed_schedule"]["deterministic"] is True
