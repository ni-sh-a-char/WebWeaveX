from core.causality.causal_recovery_engine import recover_causal_runtime
from core.causality.runtime_causality_engine import build_runtime_causality


def test_causal_recovery_replay_safe():
    events = [
        {"id": "browser:evt:0", "runtime": "browser", "step": 0},
    ]
    causality = build_runtime_causality(events, {"browser": 1})
    causality["propagation_order"] = ["", "browser:evt:0"]

    recovered = recover_causal_runtime(causality, events)

    assert recovered["synchronization_restored"] is True
    assert recovered["broken_chains_fixed"] >= 0
    assert recovered["recovered_events"]
