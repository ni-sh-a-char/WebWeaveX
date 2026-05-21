def assert_measurable(result: dict, metric: str = "accuracy") -> None:
    assert metric in result or "f1" in result, f"missing metric in {result}"
    val = result.get(metric, result.get("f1"))
    assert isinstance(val, (int, float)), "metric must be numeric"
    assert 0.0 <= float(val) <= 1.0, "metric must be in [0,1]"
