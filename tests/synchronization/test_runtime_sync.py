from core.synchronization.runtime_snapshot_engine import capture_runtime_snapshot
from core.synchronization.runtime_sync_engine import synchronize_runtime


def test_runtime_sync_handlers():
    snapshot = capture_runtime_snapshot(browser={"url": "https://example.com"}, tick=1)
    result = synchronize_runtime([snapshot], tick=1)

    assert result["count"] >= 1
    assert len(result["synchronized"]) == 5
