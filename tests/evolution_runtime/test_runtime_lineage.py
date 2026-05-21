from core.evolution_runtime import run_evolution_runtime


def test_lineage_replay():
    result = run_evolution_runtime(
        adaptive_memory={"healed_selectors": {"#a": "#b"}},
        tick=2,
    )

    first = result["replay"]
    second = result["replay"]

    assert first == second
    assert result["lineage"]
