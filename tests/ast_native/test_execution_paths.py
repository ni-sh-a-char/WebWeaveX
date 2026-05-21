from core.ast import compile_semantic_ast_ir


def test_execution_paths_bounded():
    code = """
def a():
    pass

def b():
    pass
"""
    ir = compile_semantic_ast_ir(code)
    assert ir["execution_paths"]["path_count"] == 2
    assert ir["execution_paths"]["bounded"] is True
    assert ir["deterministic"] is True
