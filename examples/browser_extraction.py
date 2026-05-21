"""WebWeaveX v2.0.0 — Browser extraction example."""

from webweavex import extract_web

if __name__ == "__main__":
    result = extract_web(
        "https://example.com",
        semantic_runtime=False,
        federated_memory=False,
    )
    print("nodes:", len(result.get("unified_runtime_graph", {}).get("nodes", [])))
    print("bounded:", result.get("bounded"))
