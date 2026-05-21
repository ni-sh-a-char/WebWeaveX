from core.memory.runtime_merge_engine import merge_runtime_memories
from core.memory.runtime_memory_engine import build_runtime_memory


def test_memory_merge():
    a = build_runtime_memory(
        runtime_history=[{"tick": 1, "kind": "workflow"}],
        lineage=[{"id": "a:1"}],
    )
    b = build_runtime_memory(
        runtime_history=[{"tick": 2, "kind": "sync"}],
        lineage=[{"id": "b:1"}],
    )

    first = merge_runtime_memories([a, b])
    second = merge_runtime_memories([a, b])

    assert first == second
    assert len(first["runtime_history"]) == 2
