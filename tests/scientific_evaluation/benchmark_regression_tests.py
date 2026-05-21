import json
from pathlib import Path

from benchmarks.run_empirical_semantic_benchmarks import main


def test_benchmarks_run_with_hard_negatives():
    main()
    results = json.loads((Path(__file__).resolve().parents[2] / "benchmarks" / "benchmark_results.json").read_text(encoding="utf-8"))
    names = {r.get("corpus") for r in results}
    assert "graph_cycles" in names
    assert "ontology_conflicts" in names
    accuracies = [r.get("accuracy", 1) for r in results if r.get("cases")]
    assert min(accuracies) < 1.0 or len(accuracies) > 10
