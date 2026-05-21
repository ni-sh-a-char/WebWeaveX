from core.connectors import run_live_runtime
from core.ir.live_runtime_ir import live_runtime_ir_to_graph


def test_live_runtime_graph_determinism():
    snapshot = {
        "database": {"tables": ["users"]},
        "kubernetes": {
            "deployments": [{"name": "api"}],
            "pods": [{"name": "api-0"}],
        },
        "containers": {
            "containers": [{"id": "c1"}],
        },
    }

    first = run_live_runtime(snapshot=snapshot)
    second = run_live_runtime(snapshot=snapshot)

    assert first["graph"] == second["graph"]
    graph_ir = live_runtime_ir_to_graph(first["live_ir"])
    assert graph_ir["nodes"]
