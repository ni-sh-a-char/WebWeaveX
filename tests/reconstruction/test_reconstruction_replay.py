from core.reconstruction.runtime_replay_builder import build_runtime_replay


def test_timeline_replay_identical():
    actions = [{"id": "a1", "action_id": "a1"}, {"id": "a2", "action_id": "a2"}]

    first = build_runtime_replay(actions=actions, tick=0)
    second = build_runtime_replay(actions=actions, tick=0)

    assert first == second
    assert len(first["replay_chains"]) == 2
