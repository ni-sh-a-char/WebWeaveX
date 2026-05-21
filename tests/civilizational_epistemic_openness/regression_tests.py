from core.repository.event_topology_engine import infer_event_topology


def test_event_topology_regression():
    r = infer_event_topology("from celery import Celery\n", path="t.py")
    assert r["evidence"] in ("parser_imports", "text_fallback")
