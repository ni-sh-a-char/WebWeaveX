from core.adaptive import stabilize_extraction_schema


def test_schema_stability():
    layout_a = {
        "title": "Example",
        "items": [{"name": "a"}],
    }
    layout_b = {
        "items": [{"name": "a"}],
        "title": "Example",
    }

    first = stabilize_extraction_schema(layout_a)
    second = stabilize_extraction_schema(layout_b)

    assert first["fields"] == second["fields"]
