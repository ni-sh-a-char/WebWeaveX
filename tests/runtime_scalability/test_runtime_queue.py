from core.runtime.runtime_queue_engine import RuntimeQueue


def test_queue_drops_when_full():
    q = RuntimeQueue(max_size=2)
    assert q.enqueue({"id": "1"}) is True
    assert q.enqueue({"id": "2"}) is True
    assert q.enqueue({"id": "3"}) is False
