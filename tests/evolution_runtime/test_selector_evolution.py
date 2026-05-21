from core.evolution_runtime.selector_evolution_engine import evolve_selector_runtime


def test_evolution_determinism_selectors():
    healed = {"#btn": "[data-test='submit']", "#nav": "nav.main"}

    first = evolve_selector_runtime({}, healed)
    second = evolve_selector_runtime({}, healed)

    assert first == second
    assert first["count"] == 2
