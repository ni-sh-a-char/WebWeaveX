from core.documents.document_semantic_ir_engine import build_document_semantic_ir
from tests.scientific_evaluation.evaluation_helpers import assert_substrate_ir


def test_document_semantic_ir():
    ir = build_document_semantic_ir("# Goal\n\n## Step 1\n\nBecause it works.\n")
    assert_substrate_ir(ir, ["rhetorical", "argument", "progression", "prerequisites", "evidence"])
    assert len(ir["rhetorical"]["rhetorical_roles"]) >= 1
