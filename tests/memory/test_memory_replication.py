from core.memory.runtime_memory_engine import build_runtime_memory
from core.memory.runtime_replication_engine import replicate_runtime_memory
from core.memory.runtime_convergence_memory_engine import converge_runtime_memory


def test_memory_replication():
    runtime = build_runtime_memory(
        runtime_history=[{"tick": 1, "kind": "workflow"}],
        lineage=[{"id": "line:1"}],
    )
    nodes = [{"node_id": "n1"}, {"node_id": "n2"}]

    replication = replicate_runtime_memory(runtime, nodes)
    convergence = converge_runtime_memory(replication["replicas"])

    assert convergence["converged"] is True
    assert replication["replica_count"] == 2
