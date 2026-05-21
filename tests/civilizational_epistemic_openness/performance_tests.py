import time

from core.evidence import structure_cognition


def test_openness_performance_budget():
    start = time.perf_counter()
    for _ in range(50):
        structure_cognition({"a": 1, "b": 2}, {"c": 3}, {"a": 1})
    elapsed = time.perf_counter() - start
    assert elapsed < 5.0
