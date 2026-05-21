from core.ssa import build_ssa_form


def test_ssa_versions():

    code = """
x = 1
x = 2
"""

    r = build_ssa_form(code)

    assert r["variable_versions"]["x"] == 2
