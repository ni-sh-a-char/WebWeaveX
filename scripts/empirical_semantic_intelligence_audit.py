#!/usr/bin/env python3
"""Empirical semantic intelligence audit — scripts/empirical_semantic_intelligence_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
BENCH = ROOT / "benchmarks"
TESTS = ROOT / "tests"
OUT = ROOT / "scripts" / "empirical_semantic_intelligence_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def iter_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def scan(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="ignore")
    return {
        "parser": len(re.findall(r"parse_source|ParserRegistry|parser_grounding|tree_sitter", src)),
        "regex": len(re.findall(r"re\.(findall|search|match)", src)),
        "empirical": len(re.findall(r"precision|recall|f1|calibration|benchmark", src, re.I)),
        "heuristic": len(re.findall(r"round\(min\(1\.0", src)),
    }


def domain(name: str) -> dict:
    base = CORE / name
    files = list(iter_py(base))
    if not files:
        return {"files": 0}
    agg = {"parser": 0, "regex": 0, "empirical": 0, "heuristic": 0}
    for p in files:
        s = scan(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "parser_ratio": round(agg["parser"] / denom, 3),
        "heuristic_ratio": round(agg["heuristic"] / max(1, n * 5), 3),
        "empirical_ratio": round(agg["empirical"] / max(1, n), 3),
    }


def corpus_count() -> int:
    corpora = BENCH / "corpora"
    if not corpora.exists():
        return 0
    return sum(1 for p in corpora.rglob("cases.json") if p.is_file())


def test_count(sub: str) -> int:
    d = TESTS / sub
    return len(list(d.glob("*.py"))) - (1 if (d / "__init__.py").exists() else 0) if d.exists() else 0


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = {d: domain(d) for d in ("parsers", "evidence", "knowledge", "graph", "documents", "internet", "repository")}
    corpora_n = corpus_count()

    artifacts = {
        "semantic_benchmark_coverage": {"corpora": corpora_n, "formal_fixtures": len(list(BENCH.glob("*/fixtures.json")))},
        "parser_grounding_coverage": {d: domains[d].get("parser_ratio", 0) for d in domains},
        "ontology_validation_coverage": {"knowledge": domains.get("knowledge", {})},
        "graph_reasoning_accuracy": {"graph": domains.get("graph", {})},
        "trust_calibration_quality": {"internet": domains.get("internet", {})},
        "contradiction_detection_quality": {"evidence": domains.get("evidence", {})},
        "discourse_reconstruction_quality": {"documents": domains.get("documents", {})},
        "semantic_relation_accuracy": {"semantic": domain("semantic")},
        "repository_reasoning_accuracy": {"repository": domains.get("repository", {})},
        "tutorial_dependency_accuracy": {"documents": domains.get("documents", {})},
        "semantic_entropy_validation": {"evidence": domains.get("evidence", {})},
        "semantic_consistency_validation": {"evidence": domains.get("evidence", {})},
        "adversarial_semantic_surface": {
            "adversarial": test_count("adversarial"),
            "adversarial_semantics": test_count("adversarial_semantics"),
        },
        "real_world_validation_matrix": {"opt_in_env": "WEBWEAVEX_RUN_NETWORK_TESTS"},
        "heuristic_residue_matrix": {d: domains[d].get("heuristic_ratio", 0) for d in domains},
        "formal_inference_coverage": {d: domains[d].get("empirical_ratio", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": domains, "corpora": corpora_n, "scientific_tests": test_count("scientific_validation")}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
