from core.evolution_runtime.runtime_pattern_engine import build_runtime_patterns


def test_runtime_patterns():
    patterns = build_runtime_patterns(
        ui={"forms": True, "dashboards": True},
        workflows=[{"objective": "monitor_metrics"}],
        semantic={"domain": {"domain": "analytics"}},
        sync_history=[{"tick": 1}],
    )

    assert "forms" in patterns["ui_structures"]
    assert patterns["sync_histories"] == 1
