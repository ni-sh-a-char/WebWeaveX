from core.adaptive.runtime_reconciliation_engine import reconcile_runtime_state


def test_runtime_reconciliation():
    result = reconcile_runtime_state(
        browser_runtime={"available": True, "url": "https://example.com"},
        stream_runtime={"events": [{"id": "stream_0"}]},
        interaction_runtime={"interactions": [{"step": 0}]},
        extraction_runtime={"fields": ["title", "items"]},
    )

    assert result["consistent"] is True
