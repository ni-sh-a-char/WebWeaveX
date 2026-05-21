from core.connectors import extract_database_runtime


def test_connector_determinism_database():
    snapshot = {
        "schemas": ["public"],
        "tables": ["users", "orders"],
        "metrics": {"connections": 5},
    }

    first = extract_database_runtime("postgresql", snapshot)
    second = extract_database_runtime("postgresql", snapshot)

    assert first == second
    assert first["tables"] == ["orders", "users"]
