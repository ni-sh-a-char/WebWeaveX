from core.execution.runtime_queue_engine import dequeue_runtime_action, enqueue_runtime_action


def _build_queue():
    queue = []
    queue = enqueue_runtime_action(queue, {"id": "low"}, priority=0)["queue"]
    queue = enqueue_runtime_action(queue, {"id": "high"}, priority=10)["queue"]
    return queue


def test_execution_queue_deterministic():
    first = dequeue_runtime_action(_build_queue())
    second = dequeue_runtime_action(_build_queue())

    assert first["action"] == second["action"]
    assert first["action"]["id"] == "high"
