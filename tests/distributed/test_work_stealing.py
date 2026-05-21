from core.distributed import balance_semantic_workloads


def test_work_stealing_balances():
    workloads = {"a": [{"id": "1"}, {"id": "2"}], "b": []}
    r = balance_semantic_workloads(workloads)
    assert r["deterministic"] is True
    assert "balanced" in r
