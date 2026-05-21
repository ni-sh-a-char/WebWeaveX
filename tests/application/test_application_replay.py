from core.application.application_replay_engine import replay_application_runtime
from core.application import run_application_cognition


def test_application_replay():
    html = "<html><nav><a href='/dashboard'>Dashboard</a></nav><div class='widget'>KPI</div></html>"

    cognition = run_application_cognition(
        url="https://example.com",
        html=html,
        objective="extract_dashboard",
    )

    memory = cognition["memory"]
    first = replay_application_runtime(memory)
    second = replay_application_runtime(memory)

    assert first == second
    assert first["workflows"]
