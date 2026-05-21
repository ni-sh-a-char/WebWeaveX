from core.identity.webgl_runtime_engine import build_webgl_runtime


def test_webgl_runtime():
    webgl = build_webgl_runtime("default")

    assert webgl["vendor"]
    assert webgl["renderer"]
    assert webgl["extensions"]
