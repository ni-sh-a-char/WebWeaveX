from core.connectors import extract_api_runtime


def test_api_runtime_rest():
    snapshot = {
        "endpoints": ["/api/v1/users", "/api/v1/orders"],
        "pagination": ["cursor"],
    }

    first = extract_api_runtime("rest", snapshot)
    second = extract_api_runtime("rest", snapshot)

    assert first == second
    assert len(first["endpoints"]) == 2
