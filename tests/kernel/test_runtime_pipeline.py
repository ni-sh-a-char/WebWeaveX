from core.contracts.runtime_contracts import UniversalInput
from core.kernel.runtime_pipeline import run_canonical_pipeline


def test_canonical_pipeline_example_com():
    result = run_canonical_pipeline(
        UniversalInput(source="https://example.com", source_type="web"),
        options={"kernel": {"semantic": False, "sync": False, "memory": False}},
    )
    assert result["kind"] == "web"
    assert result["pipeline_hash"]
    assert result["bounded"] is True
