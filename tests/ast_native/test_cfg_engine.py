from core.ast import (
    parse_python_ast,
    build_control_flow_graph,
)


def test_cfg():

    code = """
def a():
    pass

def b():
    pass
"""

    ast_ir = parse_python_ast(code)

    r = build_control_flow_graph(ast_ir)

    assert len(r["nodes"]) == 2
