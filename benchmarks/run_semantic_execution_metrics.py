#!/usr/bin/env python3
"""Generate semantic execution metric reports (Phase 10)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from benchmarks.run_empirical_semantic_benchmarks import run_corpus, _score

CORPORA = [
    "github_real",
    "discourse_real",
    "runtime_real",
    "ontology_real",
    "topology_real",
]


def main() -> None:
    results = [run_corpus(ROOT / "benchmarks" / "corpora" / name) for name in CORPORA]
    scored = [r for r in results if r.get("f1") is not None]
    agg = _score([{"predicted": r.get("f1", 0) >= 0.5} for r in scored]) if scored else {"f1": 0, "cases": 0}

    reports = {
        "semantic_precision_report.json": {"precision": agg.get("precision", 0), "corpora": CORPORA},
        "semantic_recall_report.json": {"recall": agg.get("recall", 0), "corpora": CORPORA},
        "semantic_f1_report.json": {"f1": agg.get("f1", 0), "details": results},
        "runtime_reconstruction_report.json": next((r for r in results if r.get("corpus") == "runtime_real"), {}),
        "ontology_accuracy_report.json": next((r for r in results if r.get("corpus") == "ontology_real"), {}),
        "discourse_accuracy_report.json": next((r for r in results if r.get("corpus") == "discourse_real"), {}),
        "execution_reasoning_report.json": next((r for r in results if r.get("corpus") == "github_real"), {}),
        "semantic_memory_report.json": {"checkpoint_engine": "core.memory.semantic_checkpoint_engine"},
    }
    for name, data in reports.items():
        (ROOT / name).write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({k: v.get("f1", v) if isinstance(v, dict) else v for k, v in reports.items()}, indent=2))


if __name__ == "__main__":
    main()
