from core.memory.runtime_convergence_memory_engine import converge_runtime_memory


def test_memory_convergence_conflict():
    replicas = [
        {"memory_id": "same", "replicated": True},
        {"memory_id": "same", "replicated": True},
    ]

    first = converge_runtime_memory(replicas)
    second = converge_runtime_memory(replicas)

    assert first == second
    assert first["converged"] is True
