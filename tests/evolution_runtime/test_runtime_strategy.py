from core.evolution_runtime.runtime_strategy_engine import build_runtime_strategy


def test_runtime_strategy_deterministic():
    evidence = {"drift_count": 2, "failed_steps": 1}

    first = build_runtime_strategy(evidence)
    second = build_runtime_strategy(evidence)

    assert first == second
    assert first["extraction_path"] == "repair_then_extract"
