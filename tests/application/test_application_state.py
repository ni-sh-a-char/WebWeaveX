from core.application.application_state_engine import build_application_state


def test_application_state_shape():
    state = build_application_state(
        route="https://example.com/dashboard",
        forms=[{"action": "/submit"}],
        authenticated=True,
    )

    assert state["route"] == "https://example.com/dashboard"
    assert state["authenticated"] is True
    assert state["bounded"] is True
