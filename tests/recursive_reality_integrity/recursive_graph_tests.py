from core.parsers import parse_source


def test_graph():
    assert parse_source("import os\n", path="m.py").get("semantic_graph")
