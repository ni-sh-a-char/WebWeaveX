from core.native.electron_runtime_engine import extract_electron_runtime


def test_electron_state():
    first = extract_electron_runtime("discord", {"routes": ["/channels/@me"]})
    second = extract_electron_runtime("discord", {"routes": ["/channels/@me"]})

    assert first == second
    assert first["application"] == "discord"
    assert first["routes"]
