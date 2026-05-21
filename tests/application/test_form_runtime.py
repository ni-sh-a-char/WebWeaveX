from core.application.form_runtime_engine import build_form_runtime
from core.application.application_recovery_engine import (
    recover_application_runtime,
)


def test_form_recovery():
    html = "<form><input name='email' required></form>"

    recovered = recover_application_runtime(
        html,
        {"route": "/", "modals": [], "authenticated": True},
    )

    assert recovered["forms_recovered"][0]["recovered"] is True


def test_form_runtime_inputs():
    html = """
    <form action='/login'>
      <input name='username' required>
      <input name='csrf_token' value='abc'>
    </form>
    """

    forms = build_form_runtime(html)

    assert forms["forms"][0]["csrf_fields"]
