import json
from pathlib import Path

import jsonschema


def test_graph_schema():
    schema = json.loads(
        (Path(__file__).resolve().parents[2] / "contracts" / "schemas" / "graph.schema.json").read_text(encoding="utf-8-sig")
    )
    jsonschema.validate({"nodes": [{"id": "a", "kind": "n"}], "edges": [{"from": "a", "to": "b"}], "max_edges": 5}, schema)
