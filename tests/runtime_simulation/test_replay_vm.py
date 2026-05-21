from core.runtime.semantic_replay_vm import (
    replay_semantic_events,
)


def test_replay():

    r = replay_semantic_events([
        {
            "id": "e1",
            "type": "start",
        }
    ])

    assert r["event_count"] == 1
