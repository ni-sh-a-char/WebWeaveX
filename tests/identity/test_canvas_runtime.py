from core.identity.canvas_runtime_engine import build_canvas_runtime


def test_canvas_stability():
    first = build_canvas_runtime("default")
    second = build_canvas_runtime("default")

    assert first["canvas_fingerprint"] == second["canvas_fingerprint"]
