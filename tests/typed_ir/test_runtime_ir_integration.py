from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_ssa_and_topology():
    code = "x = 1\nx = 2"
    ir = compile_runtime_ir(source=code, graph={"events": [{"id": "e1", "timestamp": 1}, {"id": "e2", "timestamp": 2}]})
    assert ir["ssa"]["variable_versions"]["x"] == 2
    assert ir["event_stream"]["bounded"] is True
    assert len(ir["event_stream"]["edges"]) == 1
    assert ir["distributed_topology"]["bounded"] is True
