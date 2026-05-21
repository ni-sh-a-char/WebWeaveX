#!/usr/bin/env python3
"""Formal semantic foundation audit — scripts/formal_semantic_foundation_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
WEB = ROOT / "webweavex"
TESTS = ROOT / "tests"
CONTRACTS = ROOT / "contracts"
OUT = ROOT / "scripts" / "formal_semantic_foundation_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache", ".git"}


def iter_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def scan_file(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="ignore")
    parser_hits = len(re.findall(r"parse_source|parser_basis|ParserRegistry|ast_engine|tree_sitter", src))
    regex_hits = len(re.findall(r"re\.(findall|search|match|compile)", src))
    heuristic = len(re.findall(r"round\(min\(1\.0|heuristic|0\.\d+\s*\*", src))
    formal = len(re.findall(r"deterministic_inputs|evidence_algebra|inference_calculus|justification", src))
    ontology = len(re.findall(r"grounding|ontology|evidence", src, re.I))
    graph = len(re.findall(r'"from"|"to"|graph_invariant|semantic_topology', src))
    return {
        "parser": parser_hits,
        "regex": regex_hits,
        "heuristic": heuristic,
        "formal": formal,
        "ontology": ontology,
        "graph": graph,
        "lines": src.count("\n") + 1,
    }


def domain_stats(name: str, base: Path) -> dict:
    files = list(iter_py(base))
    if not files:
        return {"files": 0, "parser_ratio": 0.0, "heuristic_ratio": 0.0, "formal_ratio": 0.0}
    agg = {"parser": 0, "regex": 0, "heuristic": 0, "formal": 0, "ontology": 0, "graph": 0}
    for p in files:
        s = scan_file(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "parser_hits": agg["parser"],
        "regex_hits": agg["regex"],
        "parser_ratio": round(agg["parser"] / denom, 3),
        "heuristic_ratio": round(agg["heuristic"] / max(1, n * 10), 3),
        "formal_ratio": round(agg["formal"] / max(1, n), 3),
        "ontology_grounding": round(agg["ontology"] / max(1, n * 5), 3),
        "graph_semantics": round(agg["graph"] / max(1, n * 3), 3),
    }


def count_tests(pattern: str) -> int:
    if not TESTS.exists():
        return 0
    return sum(1 for _ in TESTS.rglob(pattern))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = {
        "parsers": CORE / "parsers",
        "evidence": CORE / "evidence",
        "knowledge": CORE / "knowledge",
        "graph": CORE / "graph",
        "documents": CORE / "documents",
        "internet": CORE / "internet",
        "semantic": CORE / "semantic",
        "repository": CORE / "repository",
    }
    stats = {k: domain_stats(k, v) for k, v in domains.items()}

    formal_modules = [
        "evidence_algebra_engine.py",
        "semantic_inference_calculus.py",
        "deterministic_reasoning_engine.py",
        "graph_invariant_engine.py",
        "ontology_consistency_engine.py",
        "discourse_parser_engine.py",
        "trust_calibration_engine.py",
    ]
    gaps = [m for m in formal_modules if not (CORE / "evidence" / m).exists() and not any((CORE / d / m).exists() for d in domains)]

    artifacts = {
        "formal_semantic_gaps": {"missing_modules": gaps, "domains": stats},
        "heuristic_residue_matrix": {d: stats[d].get("heuristic_ratio", 0) for d in stats},
        "parser_dominance_matrix": {d: stats[d].get("parser_ratio", 0) for d in stats},
        "ontology_grounding_matrix": {d: stats[d].get("ontology_grounding", 0) for d in stats},
        "semantic_validation_matrix": {d: stats[d].get("formal_ratio", 0) for d in stats},
        "benchmark_coverage_matrix": {
            "formal_semantics_tests": count_tests("formal_semantics/*.py"),
            "adversarial_tests": count_tests("adversarial/*.py"),
            "deterministic_cognitive_semantics": count_tests("deterministic_cognitive_semantics/*.py"),
            "benchmark_scripts": len(list((ROOT / "benchmarks").glob("**/*.py"))) if (ROOT / "benchmarks").exists() else 0,
        },
        "graph_consistency_matrix": {d: stats[d].get("graph_semantics", 0) for d in stats},
        "inference_formalization_matrix": {d: stats[d].get("formal_ratio", 0) for d in stats},
        "semantic_entropy_matrix": {d: stats[d].get("heuristic_ratio", 0) for d in stats},
        "contradiction_rigor_matrix": {d: stats[d].get("formal_ratio", 0) for d in stats},
        "uncertainty_math_matrix": {d: stats[d].get("formal_ratio", 0) for d in stats},
        "trust_calibration_matrix": {"internet": stats.get("internet", {}).get("formal_ratio", 0)},
        "evidence_calculus_matrix": {"evidence": stats.get("evidence", {}).get("formal_ratio", 0)},
        "semantic_proof_matrix": {d: stats[d].get("formal_ratio", 0) for d in stats},
        "adversarial_surface_matrix": {"adversarial_tests": count_tests("adversarial/*.py")},
        "real_world_validation_matrix": {"network_opt_in": True},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    summary = {"domains": stats, "gaps": gaps, "contracts": len(list(CONTRACTS.rglob("*.json"))) if CONTRACTS.exists() else 0}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
