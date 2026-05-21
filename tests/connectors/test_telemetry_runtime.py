from core.connectors import extract_telemetry_runtime


def test_telemetry_stability():
    snapshot = {
        "metrics": [{"name": "http_requests", "value": 100}],
        "traces": [{"trace_id": "t1"}],
        "spans": [{"span_id": "s1"}],
        "correlations": [{"from": "s1", "to": "t1"}],
    }

    first = extract_telemetry_runtime(snapshot=snapshot)
    second = extract_telemetry_runtime(snapshot=snapshot)

    assert first == second
    assert first["metrics"][0]["name"] == "http_requests"
