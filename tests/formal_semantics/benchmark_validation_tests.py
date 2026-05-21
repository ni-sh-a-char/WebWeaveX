import json
from pathlib import Path

from benchmarks.run_formal_benchmarks import run_dataset


def test_benchmarks_execute():
    r = run_dataset("contradiction_detection")
    assert r["f1"] >= 0.5
    results_path = Path(__file__).resolve().parents[2] / "benchmarks" / "formal_benchmark_results.json"
    if results_path.exists():
        data = json.loads(results_path.read_text(encoding="utf-8"))
        assert len(data) >= 1
