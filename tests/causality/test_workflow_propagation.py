from core.causality.cross_runtime_alignment_engine import align_cross_runtime_events
from core.causality.runtime_dependency_engine import build_runtime_dependencies
from core.causality.workflow_propagation_engine import build_workflow_propagation


def test_workflow_propagation_handoffs():
    events = [
        {"id": "browser:evt:0", "runtime": "browser", "step": 0},
        {"id": "electron:evt:1", "runtime": "electron", "step": 1},
    ]
    aligned = align_cross_runtime_events(events)
    deps = build_runtime_dependencies(events, {"synchronization_chains": []})
    propagation = build_workflow_propagation(aligned, deps)

    assert propagation["handoffs"]
    assert propagation["handoffs"][0]["from"] == "browser"
