from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_phase10():
    r = compile_runtime_ir(
        source="x = 1",
        path="main.py",
        graph={"tasks": [{"id": "t1", "priority": 1}], "nodes": [{"id": "api"}]},
    )
    assert r["semantic_agent"]["status"] == "completed"
    assert "semantic_service_mesh" in r
    assert r["semantic_cluster"]["cluster_size"] == 1
