from core.ir import compile_document_ir, compile_repository_ir
from core.ir.repository_ir import empty_repository_ir
from core.ir.document_ir import empty_document_ir


def test_repository_ir_schema():
    ir = empty_repository_ir()
    assert "services" in ir and "execution_flows" in ir and "semantic_evidence" in ir


def test_compile_document_ir():
    ir = compile_document_ir("# Title\n\n## Section\n")
    assert len(ir["rhetorical_units"]) >= 1


def test_compile_repository_ir():
    ir = compile_repository_ir("import os\n", path="m.py")
    assert ir["confidence"]["deterministic"] is True
