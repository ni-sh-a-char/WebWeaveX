#!/usr/bin/env python3
"""Cognitive realism audit — scripts/cognitive_realism_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "cognitive_realism_audit"
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
    parser = len(re.findall(r"parse_source|ParserRegistry|parser_basis|parser_evidence", src))
    regex = len(re.findall(r"re\.(findall|search|match)", src))
    provenance = len(re.findall(r"lineage|evidence|grounding|provenance|confidence_basis", src, re.I))
    dependency = len(re.findall(r"depend|prereq|explains|introduces|extends", src, re.I))
    topology = len(re.findall(r"topology|boundary|deployment|orchestr", src, re.I))
    discourse = len(re.findall(r"discourse|narrative|tutorial|explanation", src, re.I))
    structure_cog = 1 if "structure_cognition" in src else 0
    return {
        "parser": parser,
        "regex": regex,
        "provenance": provenance,
        "dependency": dependency,
        "topology": topology,
        "discourse": discourse,
        "structure_cognition": structure_cog,
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("parser", "regex", "provenance", "dependency", "topology", "discourse", "structure_cognition")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "parser_dominance": round(agg["parser"] / denom, 3),
        "provenance_saturation": round(min(1.0, agg["provenance"] / (n * 4)), 3),
        "semantic_dependency_quality": round(agg["dependency"] / n, 3),
        "discourse_quality": round(agg["discourse"] / n, 3),
        "topology_realism": round(agg["topology"] / n, 3),
        "structure_cognition_adoption": round(agg["structure_cognition"] / n, 3),
        "heuristic_density": round(agg["regex"] / denom, 3),
        "semantic_fidelity": round((agg["parser"] + agg["structure_cognition"] * 3) / (denom + 3), 3),
    }


def heuristic_paths() -> list:
    out = []
    for d in ("repository", "documents", "internet", "knowledge", "graph"):
        for p in iter_py(CORE / d):
            s = analyze(p)
            if s["regex"] > 0 and s["parser"] == 0:
                out.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return sorted(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}
    gaps = heuristic_paths()

    artifacts = {
        "cognitive_realism_matrix": {d: stats[d].get("semantic_fidelity", 0) for d in domains},
        "semantic_dependency_matrix": {d: stats[d].get("semantic_dependency_quality", 0) for d in domains},
        "semantic_explanation_matrix": {d: stats[d].get("discourse_quality", 0) for d in domains},
        "semantic_flow_matrix": stats.get("documents", {}),
        "semantic_hierarchy_matrix": stats.get("documents", {}),
        "semantic_lineage_integrity": {d: stats[d].get("provenance_saturation", 0) for d in domains},
        "parser_dominance_matrix": {d: stats[d].get("parser_dominance", 0) for d in domains},
        "heuristic_semantic_density": {d: stats[d].get("heuristic_density", 0) for d in domains},
        "provenance_saturation_matrix": {d: stats[d].get("provenance_saturation", 0) for d in domains},
        "semantic_fidelity_matrix": {d: stats[d].get("semantic_fidelity", 0) for d in domains},
        "semantic_realism_gaps": {"heuristic_only_paths": gaps[:150], "count": len(gaps)},
        "topology_realism_matrix": stats.get("repository", {}),
        "repository_realism_matrix": stats.get("repository", {}),
        "document_realism_matrix": stats.get("documents", {}),
        "internet_realism_matrix": stats.get("internet", {}),
        "ontology_realism_matrix": stats.get("knowledge", {}),
        "contradiction_realism_matrix": stats.get("semantic", {}),
        "semantic_reconciliation_matrix": stats.get("evidence", {}),
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats, "gap_count": len(gaps)}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
