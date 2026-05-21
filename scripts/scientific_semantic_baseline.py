#!/usr/bin/env python3
"""Scientific semantic baselines — scripts/scientific_semantic_baselines/*.json"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "scientific_semantic_baselines"
BENCH = ROOT / "benchmarks" / "benchmark_results.json"


def load_benchmarks() -> list:
    if BENCH.exists():
        return json.loads(BENCH.read_text(encoding="utf-8"))
    return []


def mean_accuracy(results: list, corpus_names: list) -> float:
    vals = [r.get("accuracy", 0) for r in results if r.get("corpus") in corpus_names and r.get("cases")]
    return round(sum(vals) / max(1, len(vals)), 3)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    results = load_benchmarks()

    artifacts = {
        "semantic_accuracy_baselines": {
            "mean_accuracy": mean_accuracy(results, ["semantic_relationships", "semantic_deduplication", "contradiction_detection"]),
            "corpora": [r for r in results if r.get("corpus") in ("semantic_relationships", "semantic_deduplication", "contradiction_detection")],
        },
        "repository_reasoning_baselines": {
            "mean_accuracy": mean_accuracy(results, ["repository_reasoning", "architecture_reasoning", "api_documentation"]),
            "corpora": [r for r in results if r.get("corpus") in ("repository_reasoning", "architecture_reasoning", "api_documentation")],
        },
        "document_discourse_baselines": {
            "mean_accuracy": mean_accuracy(results, ["document_discourse", "tutorial_dependencies"]),
            "corpora": [r for r in results if r.get("corpus") in ("document_discourse", "tutorial_dependencies")],
        },
        "ontology_validation_baselines": {
            "mean_accuracy": mean_accuracy(results, ["ontology_resolution"]),
            "corpora": [r for r in results if r.get("corpus") == "ontology_resolution"],
        },
        "graph_reasoning_baselines": {
            "mean_accuracy": mean_accuracy(results, ["topology_reconstruction", "causal_reasoning"]),
            "corpora": [r for r in results if r.get("corpus") in ("topology_reconstruction", "causal_reasoning")],
        },
        "trust_calibration_baselines": {
            "mean_accuracy": mean_accuracy(results, ["trust_calibration", "citation_lineage"]),
            "corpora": [r for r in results if r.get("corpus") in ("trust_calibration", "citation_lineage")],
        },
        "adversarial_baselines": {"tests": 5, "target_min": 10},
        "heuristic_residue_baselines": {
            "documents_regex_heavy": True,
            "repository_regex_fallback": True,
            "target_parser_ratio": 0.85,
        },
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"benchmark_runs": len(results), "artifacts": list(artifacts.keys())}
    (OUT / "baseline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
