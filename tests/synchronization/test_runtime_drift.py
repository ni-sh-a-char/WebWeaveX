from core.synchronization.runtime_drift_engine import detect_runtime_drift


def test_runtime_drift_detection():
    baseline = {"semantic": {"a": 1}, "workflow": {"step": 1}}
    current = {"semantic": {"a": 2}, "workflow": {"step": 2}}

    drift = detect_runtime_drift(baseline, current)

    assert drift["diverged"] is True
    assert drift["drift_count"] >= 2
