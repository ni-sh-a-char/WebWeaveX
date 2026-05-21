from core.synchronization import run_synchronized_runtime
from core.synchronization.runtime_replay_engine import replay_synchronized_runtime


def test_synchronized_replay():
    result = run_synchronized_runtime(
        tick=3,
        browser={"dom": {"title": "Dashboard"}},
        semantic_result={"semantic": {"domain": {"domain": "analytics"}}},
    )

    memory = result["memory"]
    first = replay_synchronized_runtime(memory)
    second = replay_synchronized_runtime(memory)

    assert first == second
    assert result["replay"] == first
