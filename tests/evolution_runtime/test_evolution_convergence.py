from core.evolution_runtime.runtime_convergence_engine import converge_runtime_evolution
from core.evolution_runtime.runtime_evolution_engine import build_runtime_evolution


def test_evolution_convergence():
    evolutions = [
        build_runtime_evolution(
            [{"kind": "selector", "target": "a"}],
            [],
        ),
        build_runtime_evolution(
            [{"kind": "workflow", "target": "b"}],
            [],
        ),
    ]

    first = converge_runtime_evolution(evolutions)
    second = converge_runtime_evolution(evolutions)

    assert first == second
    assert first["consistent"] is True
