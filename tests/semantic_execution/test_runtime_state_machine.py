from core.runtime.runtime_state_machine_engine import RuntimeStateMachine


def test_valid_transition_updates_state():
    sm = RuntimeStateMachine()
    t = sm.transition("scheduled", evidence=["test"])
    assert t.valid is True
    assert sm.state == "scheduled"


def test_invalid_transition_preserves_state():
    sm = RuntimeStateMachine()
    sm.transition("scheduled")
    t = sm.transition("completed")
    assert t.valid is False
    assert sm.state == "scheduled"
