from core.application.application_memory_engine import (
    load_application_memory,
    save_application_memory,
)
from core.application import run_application_cognition


def test_application_memory_persistence(tmp_path):
    cognition = run_application_cognition(
        url="https://example.com",
        html="<html><form></form></html>",
        objective="login",
    )

    path = tmp_path / "app.enc"
    save_application_memory(str(path), cognition["memory"], "app-key")

    loaded = load_application_memory(str(path), "app-key")

    assert loaded["available"] is True
    assert loaded["memory"]["objectives"] == ["login"]
