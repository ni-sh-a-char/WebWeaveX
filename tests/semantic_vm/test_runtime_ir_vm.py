from core.ir.runtime_ir import compile_runtime_ir


def test_runtime_ir_includes_vm_and_journal():
    ir = compile_runtime_ir(source="def run(): pass", path="main.py")
    assert ir["semantic_bytecode"]["bounded"] is True
    assert ir["semantic_vm"]["bounded"] is True
    assert ir["transaction"]["committed"] is True
    assert ir["journal"]["count"] == 1
