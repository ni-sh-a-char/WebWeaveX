from core.ast import parse_python_ast


def test_parse_imports():

    code = """
import os
import sys
"""

    r = parse_python_ast(code)

    assert r["ast_grounded"] is True

    assert len(r["imports"]) == 2
