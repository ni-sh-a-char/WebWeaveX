from core.synchronization.runtime_delta_engine import build_runtime_delta


def test_delta_determinism():
    previous = {"dom": {"a": 1}, "semantic": {"x": 1}}
    current = {"dom": {"a": 2}, "semantic": {"x": 2}}

    first = build_runtime_delta(previous, current, tick=5)
    second = build_runtime_delta(previous, current, tick=5)

    assert first == second
    assert first["timestamp"] == 5
    assert first["changes"]
