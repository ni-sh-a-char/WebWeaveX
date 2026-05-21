from core.treesitter import (
    parse_universal_ast,
)


def test_universal_ast_python():

    r = parse_universal_ast(
        "def run(): pass",
        "main.py",
    )

    assert r["grounded"] is True
