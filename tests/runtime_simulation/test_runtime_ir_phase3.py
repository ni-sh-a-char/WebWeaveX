from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_simulation_and_replay():
    ir = compile_runtime_ir(
        source="def run(): pass",
        path="main.py",
        graph={
            "transitions": [{"from": "a", "to": "b"}, {"from": "b", "to": "c"}],
            "events": [{"id": "e1", "type": "start", "timestamp": 0}],
        },
    )
    assert ir["runtime_simulation"]["final_state"] == "c"
    assert ir["semantic_replay"]["event_count"] == 1
    assert ir["universal_ast"]["grounded"] is True
    assert ir["persistence"]["persisted"] is True
