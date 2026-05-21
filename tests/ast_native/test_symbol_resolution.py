from core.ast import (
    parse_python_ast,
    resolve_symbols,
)


def test_symbols():

    code = """
class A:
    pass

def run(x):
    return x
"""

    ast_ir = parse_python_ast(code)

    r = resolve_symbols(ast_ir)

    assert r["symbol_count"] == 2
