from core.identity.navigator_runtime_engine import build_navigator_runtime


def test_navigator_runtime():
    navigator = build_navigator_runtime("default")

    assert navigator["webdriver"] is False
    assert navigator["hardwareConcurrency"] == 8
    assert navigator["languages"]
