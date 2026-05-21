import json
from pathlib import Path

from benchmarks.run_empirical_semantic_benchmarks import main, run_corpus
from tests.scientific_validation.scientific_helpers import assert_measurable


def test_empirical_benchmarks_not_perfect_inflation():
    root = Path(__file__).resolve().parents[2]
    r = run_corpus(root / "benchmarks" / "corpora" / "ontology_resolution")
    assert_measurable(r)
    assert r["cases"] >= 1
    main()
    results_path = root / "benchmarks" / "benchmark_results.json"
    assert results_path.exists()
    results = json.loads(results_path.read_text(encoding="utf-8"))
    assert len(results) >= 10
    assert any(c.get("accuracy", 0) < 1.0 for c in results if c.get("cases"))
