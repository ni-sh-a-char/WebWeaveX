from core.evolution_runtime.runtime_repair_engine import repair_runtime_failures


def test_repair_stability():
    failures = ["broken_selector", "sync_divergence"]

    first = repair_runtime_failures(failures)
    second = repair_runtime_failures(failures)

    assert first == second
    assert first["repair_count"] == 2
