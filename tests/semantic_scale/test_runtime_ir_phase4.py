from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_phase4_fields():
    ir = compile_runtime_ir(
        source="let x = 1",
        path="app.js",
        graph={"tasks": [{"priority": 2, "weight": 1}, {"priority": 1, "weight": 0}]},
    )
    assert ir["query_plan"]["planner"] == "v2"
    assert ir["cache_key"]
    assert ir["optimized_semantic_ir"]["deterministic"] is True
    assert ir["multilang_ssa"]["supported"] is True
