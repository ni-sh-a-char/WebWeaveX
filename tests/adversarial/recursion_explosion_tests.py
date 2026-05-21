from core.evidence import build_semantic_integrity_object


def test_deep_lineage_bounded():
    stages = [{"stage": f"s{i}"} for i in range(50)]
    r = build_semantic_integrity_object(lineage_stages=stages)
    assert r["lineage"]["depth"] <= 50
