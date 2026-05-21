from core.repository.event_topology_engine import infer_event_topology


def test_repository_compat():
    r = infer_event_topology("import celery\n", path="t.py")
    assert "evidence" in r
