from core.application import build_workflow_graph
from core.application.application_state_engine import build_application_state
from core.application.application_transition_engine import (
    build_application_transitions,
)


def test_workflow_stability():
    state = build_application_state(route="https://example.com")
    transitions = build_application_transitions([state, state])

    first = build_workflow_graph([state], transitions, [])
    second = build_workflow_graph([state], transitions, [])

    assert first == second
    assert first["nodes"]
