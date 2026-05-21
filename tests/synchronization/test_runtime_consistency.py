from core.synchronization.runtime_continuity_engine import maintain_runtime_continuity
from core.synchronization import run_synchronized_runtime


def test_continuity_stability():
    continuity = maintain_runtime_continuity(
        session={"authenticated": True},
        identity={"profile": "default"},
        workflow={"objective": "monitor_metrics"},
        semantic={"domain": "analytics"},
    )

    restored = maintain_runtime_continuity(
        session=continuity["authenticated_session"],
        identity=continuity["browser_identity"],
        workflow=continuity["workflows"],
        semantic=continuity["semantic_state"],
    )

    assert restored["continuous"] is True
    assert restored["authenticated_session"] == continuity["authenticated_session"]


def test_runtime_consistency_flag():
    result = run_synchronized_runtime(tick=1)
    assert result["consistency"]["consistent"] is True
