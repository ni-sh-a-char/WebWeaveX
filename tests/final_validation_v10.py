"""Final V10 validation checks."""

from core.crypto.kaalka_engine import hex_fingerprint
from core.extract.pipeline import extract
from core.execution_graph import build_execution_graph


def run_validation() -> dict:
    out = extract("https://openai.com")
    graph = build_execution_graph({"components": [{"name": "a", "role": "core"}], "relationships": []})
    fp1 = hex_fingerprint(out)
    fp2 = hex_fingerprint(out)
    return {
        "extraction_works": isinstance(out, dict),
        "graph_stable": isinstance(graph.get("nodes"), list),
        "fingerprint_stable": fp1 == fp2,
        "schema_stable": sorted(out.keys()) == sorted(["content", "code", "dependencies", "metadata", "relationships", "raw_text", "source_url", "fingerprint"]),
    }


if __name__ == "__main__":
    print(run_validation())

