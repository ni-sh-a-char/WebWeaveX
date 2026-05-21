from core.repository.repository_execution_ir_engine import build_repository_execution_ir


def test_execution_ir_parser_evidence():
    ir = build_repository_execution_ir("import requests\n\ndef main():\n    requests.get('x')\n", path="app.py")
    assert "execution" in ir
    assert ir.get("language") == "python" or ir.get("parser_grounding")
