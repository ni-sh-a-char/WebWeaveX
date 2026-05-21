#!/usr/bin/env python3
"""Cognitive integrity audit — scripts/cognitive_integrity_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "cognitive_integrity_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def iter_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def analyze(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="ignore")
    return {
        "honesty": len(re.findall(r"honesty|supported|unsupported|fragile|overreach", src, re.I)),
        "integrity": len(re.findall(r"integrity|inference_integrity|confidence_limit", src, re.I)),
        "unsupported": len(re.findall(r"unsupported|insufficient|missing_edge|no_evidence", src, re.I)),
        "fragility": len(re.findall(r"fragility|fragile|weak_evidence", src, re.I)),
        "inflation": len(re.findall(r"confidence.*0\.9|inflate|overconfident", src, re.I)),
        "uncertainty": len(re.findall(r"uncertain|ambigu", src, re.I)),
        "contradict": len(re.findall(r"contradict", src, re.I)),
        "trace": len(re.findall(r"traceability|lineage|provenance", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("honesty", "integrity", "unsupported", "fragility", "inflation", "uncertainty", "contradict", "trace", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "semantic_honesty": round(agg["honesty"] / n, 3),
        "inference_integrity": round(agg["integrity"] / n, 3),
        "unsupported_density": round(agg["unsupported"] / n, 3),
        "semantic_fragility": round(agg["fragility"] / n, 3),
        "confidence_inflation": round(agg["inflation"] / n, 3),
        "uncertainty_preservation": round(agg["uncertainty"] / n, 3),
        "contradiction_preservation": round(agg["contradict"] / n, 3),
        "provenance_completeness": round(min(1.0, agg["trace"] / (n * 2)), 3),
        "epistemic_conservatism": round(agg["unsupported"] / max(1, n), 3),
        "semantic_overreach": round(agg["regex"] / denom, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "unsupported_semantic_claims": {d: stats[d].get("unsupported_density", 0) for d in domains},
        "unsupported_topology_edges": stats.get("repository", {}),
        "unsupported_ontology_edges": stats.get("knowledge", {}),
        "confidence_inflation_matrix": {d: stats[d].get("confidence_inflation", 0) for d in domains},
        "semantic_fragility_matrix": {d: stats[d].get("semantic_fragility", 0) for d in domains},
        "semantic_honesty_matrix": {d: stats[d].get("semantic_honesty", 0) for d in domains},
        "inference_integrity_matrix": {d: stats[d].get("inference_integrity", 0) for d in domains},
        "epistemic_conservatism_matrix": {d: stats[d].get("epistemic_conservatism", 0) for d in domains},
        "semantic_uncertainty_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "semantic_ambiguity_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "semantic_contradiction_matrix": {d: stats[d].get("contradiction_preservation", 0) for d in domains},
        "semantic_incompleteness_matrix": {d: stats[d].get("unsupported_density", 0) for d in domains},
        "semantic_traceability_matrix": {d: stats[d].get("provenance_completeness", 0) for d in domains},
        "semantic_provenance_completeness": {d: stats[d].get("provenance_completeness", 0) for d in domains},
        "semantic_support_density": stats.get("evidence", {}),
        "semantic_weakness_density": {d: stats[d].get("unsupported_density", 0) for d in domains},
        "semantic_overreach_matrix": {d: stats[d].get("semantic_overreach", 0) for d in domains},
        "heuristic_residue_matrix": {d: stats[d].get("heuristic_residue", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
