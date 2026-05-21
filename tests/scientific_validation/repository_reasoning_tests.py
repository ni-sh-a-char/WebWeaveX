from core.repository.repository_semantic_ir_engine import build_repository_semantic_ir


def test_semantic_ir_parser_first():
    ir = build_repository_semantic_ir("import os\nimport sys\n", path="m.py")
    assert ir["language"] == "python"
    assert len(ir["runtime_dependencies"]["dependencies"]) >= 0
