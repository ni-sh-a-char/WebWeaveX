from core.reconstruction.runtime_fabrication_engine import fabricate_runtime_reality


def test_fabrication_schema():
    result = fabricate_runtime_reality(
        runtime={"runtime_id": "r1", "reconstructed": True, "runtime_type": "browser"},
        environment={"runtime": "browser"},
        portable=True,
    )

    assert result["fabricated"] is True
    assert result["portable"] is True
    assert result["replay_safe"] is True
