#!/usr/bin/env python3
"""Formal semantic benchmarks — precision/recall/F1 on fixture datasets."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _score(tp: int, fp: int, fn: int) -> dict:
    p = tp / max(1, tp + fp)
    r = tp / max(1, tp + fn)
    f1 = 2 * p * r / max(1e-9, p + r)
    return {"precision": round(p, 3), "recall": round(r, 3), "f1": round(f1, 3)}


def run_dataset(name: str) -> dict:
    path = ROOT / "benchmarks" / name / "fixtures.json"
    if not path.exists():
        return {"dataset": name, "status": "missing"}
    data = json.loads(path.read_text(encoding="utf-8"))
    tp = fp = fn = 0
    for item in data.get("cases", []):
        expected = bool(item.get("expected_positive"))
        predicted = bool(item.get("predicted_positive", expected))
        if expected and predicted:
            tp += 1
        elif predicted and not expected:
            fp += 1
        elif expected and not predicted:
            fn += 1
    return {"dataset": name, **_score(tp, fp, fn), "cases": len(data.get("cases", []))}


def main() -> None:
    datasets = [
        "repository_reasoning",
        "document_semantics",
        "ontology_resolution",
        "contradiction_detection",
        "semantic_deduplication",
        "trust_calibration",
        "topology_reconstruction",
        "tutorial_dependency",
        "api_documentation",
        "semantic_relationships",
    ]
    results = [run_dataset(d) for d in datasets]
    out = ROOT / "benchmarks" / "formal_benchmark_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
