from core.integrations import augment_metadata, supports_capability
from core.integrations.capability_registry import CapabilityRegistry
from core.ir import compile_document_ir


def test_kernel_without_llm():
    ir = compile_document_ir("test")
    assert supports_capability("semantic_summarization") is False
    out = augment_metadata({"metadata": {}}, "semantic_summarization", {"summary": "x"})
    assert "llm" in out["metadata"]
    assert "semantic_summarization" not in out["metadata"]["llm"] or not out["metadata"]["llm"].get("semantic_summarization")


def test_capability_gated_augment():
    CapabilityRegistry.register("semantic_summarization")
    out = augment_metadata({"metadata": {}}, "semantic_summarization", {"summary": "ok"})
    assert out["metadata"]["llm"]["semantic_summarization"]["summary"] == "ok"
