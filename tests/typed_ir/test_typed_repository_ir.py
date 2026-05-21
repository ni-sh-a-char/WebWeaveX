from core.typed_ir import compile_typed_repository_ir


def test_typed_repository_ir_from_ast():
    code = """
def a():
    pass

def b():
    pass
"""
    r = compile_typed_repository_ir(code)
    assert r["typed"] is True
    assert len(r["nodes"]) == 2
    assert len(r["edges"]) == 1
