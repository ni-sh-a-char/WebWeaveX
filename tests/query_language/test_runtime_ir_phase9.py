from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_phase9():
    r = compile_runtime_ir(
        source="x = 1",
        path="main.py",
        graph={"nodes": [{"id": "api", "type": "service"}]},
    )
    assert "query_ast" in r
    assert "query_plan_v2" in r
    assert r["dag_execution"]["deterministic"] is True
