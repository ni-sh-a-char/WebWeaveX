from core.execution_physics import (
    align_runtime_phases,
    analyze_collapse_dynamics,
    analyze_execution_waves,
    analyze_runtime_thermodynamics,
    analyze_runtime_turbulence,
    assess_stability_mechanics,
    build_equilibrium_field,
    build_pressure_field,
    compute_execution_physics,
    compute_resonance_physics,
    compute_runtime_friction,
    compute_runtime_gravity,
    compute_runtime_inertia,
    compute_runtime_orbits,
    compute_scheduler_force,
    compute_semantic_momentum,
    measure_execution_coherence,
    propagate_runtime_energy,
    stabilize_runtime_recovery,
)


def test_energy_propagation():
    result = propagate_runtime_energy(
        {
            "distributed_topology": {
                "edges": [{"from": "a", "to": "b"}]
            }
        }
    )
    assert len(result["energy_propagation"]) == 1


def test_momentum():
    result = compute_semantic_momentum(
        {"transitions": [{}, {}]}
    )
    assert result["runtime_momentum"] == 2


def test_inertia():
    runtime = {
        "semantic_momentum": {"runtime_momentum": 5},
        "distributed_workers": [{}, {}],
    }
    result = compute_runtime_inertia(runtime)
    assert result["runtime_inertia"] == 10


def test_pressure_field():
    result = build_pressure_field(
        {"distributed_workers": [{"worker": "w1"}]}
    )
    assert result["pressure_field"][0]["worker"] == "w1"


def test_turbulence_high():
    result = analyze_runtime_turbulence(
        {"runtime_entropy": {"entropy_score": 2000}}
    )
    assert result["runtime_turbulence"] == "high"


def test_equilibrium_field():
    runtime = {
        "execution_physics": {"execution_pressure": 50}
    }
    result = build_equilibrium_field(runtime)
    assert result["field_state"] == "equilibrium"


def test_gravity():
    result = compute_runtime_gravity(
        {
            "distributed_topology": {
                "nodes": [{}],
                "edges": [{}, {}],
            }
        }
    )
    assert result["gravity"] == 3


def test_scheduler_force():
    result = compute_scheduler_force(
        {
            "tasks": [{}, {}],
            "distributed_workers": [{}],
        }
    )
    assert result["scheduler_force"] == 2


def test_resonance_physics():
    result = compute_resonance_physics(
        {
            "semantic_momentum": {"runtime_momentum": 10},
            "runtime_entropy": {"entropy_score": 5},
        }
    )
    assert result["resonance_amplitude"] == 15


def test_recovery_stabilization():
    result = stabilize_runtime_recovery(
        {"journal": {"entries": [{"e": 1}]}}
    )
    assert result["stabilized"] is True


def test_execution_waves():
    result = analyze_execution_waves(
        {"events": [{"id": "e1"}]}
    )
    assert len(result["execution_waves"]) == 1


def test_thermodynamics():
    runtime = {
        "execution_physics": {"execution_pressure": 100},
        "runtime_entropy": {"entropy_score": 50},
    }
    result = analyze_runtime_thermodynamics(runtime)
    assert result["temperature"] == 150


def test_coherence():
    runtime = {
        "state_convergence": {"converged": True},
        "runtime_turbulence": {"runtime_turbulence": "low"},
    }
    result = measure_execution_coherence(runtime)
    assert result["coherent"] is True


def test_friction():
    result = compute_runtime_friction(
        {
            "runtime_conflicts": {
                "conflicts": [1, 2]
            }
        }
    )
    assert result["friction"] == 20


def test_collapse_dynamics():
    runtime = {
        "execution_physics": {"execution_pressure": 20000}
    }
    result = analyze_collapse_dynamics(runtime)
    assert result["collapse_risk"] == "imminent"


def test_orbits():
    result = compute_runtime_orbits(
        {
            "distributed_topology": {
                "nodes": [{"id": "b"}, {"id": "a"}]
            }
        }
    )
    assert result["orbits"][0]["node"] == "a"


def test_phase_alignment():
    result = align_runtime_phases(
        {
            "tasks": [{}],
            "distributed_workers": [{}, {}],
        }
    )
    assert result["phase_aligned"] is True


def test_stability_mechanics():
    runtime = {
        "execution_physics": {"physics_state": "stable"},
        "execution_coherence": {"coherent": True},
    }
    result = assess_stability_mechanics(runtime)
    assert result["stable"] is True
