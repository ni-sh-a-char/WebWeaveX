#!/usr/bin/env python3
"""Semantic kernel deepening audit — scripts/semantic_kernel_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "semantic_kernel_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def scan(name: str) -> dict:
    base = CORE / name
    if not base.exists():
        return {"exists": False, "depth_score": 0.0}
    files = [p for p in base.rglob("*.py") if not any(s in str(p) for s in SKIP)]
    src = ""
    for p in files[:250]:
        src += p.read_text(encoding="utf-8", errors="ignore")
    n = max(1, len(files))
    return {
        "exists": True,
        "files": len(files),
        "execution_refs": round(len(re.findall(r"runtime|execution|async|event_caus|lifecycle", src, re.I)) / n, 3),
        "memory_refs": round(len(re.findall(r"memory|continuity|diff|evolution|history", src, re.I)) / n, 3),
        "discourse_refs": round(len(re.findall(r"discourse|rhetorical|argument|tutorial|narrative", src, re.I)) / n, 3),
        "parser_refs": round(len(re.findall(r"parse_source|parser_grounding|ParserRegistry", src)) / n, 3),
        "heuristic_refs": round(len(re.findall(r"re\.(findall|search)", src)) / n, 3),
        "depth_score": round(min(1.0, len(files) / 50), 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    repo = scan("repository")
    docs = scan("documents")
    runtime = scan("runtime")
    memory = scan("memory")
    query = scan("query")
    reasoning = scan("reasoning")
    internet = scan("internet")
    knowledge = scan("knowledge")
    ir = scan("ir")

    def depth(d: dict) -> float:
        return d.get("depth_score", 0) if d.get("exists") else 0

    artifacts = {
        "execution_semantics_depth": repo,
        "runtime_cognition_depth": runtime,
        "semantic_memory_depth": memory if memory.get("exists") else runtime,
        "semantic_continuity_depth": memory if memory.get("exists") else runtime,
        "semantic_diff_depth": runtime,
        "semantic_state_reasoning_depth": runtime,
        "document_discourse_depth": docs,
        "rhetorical_reasoning_depth": docs,
        "argument_semantics_depth": docs,
        "tutorial_semantics_depth": docs,
        "internet_corroboration_depth": internet,
        "semantic_lineage_depth": {"ir": ir, "knowledge": knowledge},
        "ontology_evolution_depth": knowledge,
        "parser_dominance_depth": {"parsers": scan("parsers"), "repository": repo},
        "heuristic_residue_depth": {"documents": docs.get("heuristic_refs", 0), "repository": repo.get("heuristic_refs", 0)},
        "semantic_runtime_scalability": {"corpora": len(list((ROOT / "benchmarks" / "corpora").glob("*/cases.json"))) if (ROOT / "benchmarks" / "corpora").exists() else 0},
        "semantic_runtime_boundedness": {"runtime": runtime, "memory": memory},
        "semantic_runtime_consistency": {"ir": ir},
        "semantic_runtime_safety": {"adversarial_tests": len(list((ROOT / "tests" / "adversarial_semantics").glob("*.py"))) if (ROOT / "tests" / "adversarial_semantics").exists() else 0},
        "semantic_runtime_validation": {"benchmarks": (ROOT / "benchmarks" / "benchmark_results.json").exists()},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": {"repository": repo, "documents": docs, "runtime": runtime, "memory": memory, "reasoning": reasoning}}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
