from core.ir.repository_ir import compile_repository_ir


def test_repository_ir_includes_semantic_ast():
    code = "def handler(): return 1"
    ir = compile_repository_ir(source=code, path="app.py")
    assert "semantic_ast" in ir
    assert ir["semantic_ast"]["semantic_grounded"] is True
    assert ir["semantic_ast"]["symbols"]["symbol_count"] == 1
