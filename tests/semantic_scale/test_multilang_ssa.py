from core.ssa.multilang_ssa_engine import (
    build_multilang_ssa,
)


def test_js_ssa():

    r = build_multilang_ssa(
        "let x = 1\nlet x = 2",
        "javascript",
    )

    assert len(
        r["variables"]
    ) == 2
