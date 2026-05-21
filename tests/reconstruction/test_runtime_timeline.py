from core.reconstruction.runtime_timeline_engine import build_runtime_timeline


def test_timeline_determinism():
    actions = [{"id": "a1", "tick": 1}, {"id": "a2", "tick": 2}]

    first = build_runtime_timeline(actions=actions, tick=0)
    second = build_runtime_timeline(actions=actions, tick=0)

    assert first == second
    assert first["replay_deterministic"] is True
