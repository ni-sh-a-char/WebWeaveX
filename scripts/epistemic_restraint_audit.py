#!/usr/bin/env python3
"""Epistemic restraint audit — scripts/epistemic_restraint_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "epistemic_restraint_audit"
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
        "restraint": len(re.findall(r"restraint|noninference|suppressed|confidence_cap|refusal", src, re.I)),
        "overreach": len(re.findall(r"overreach|overexpansion|optimistic", src, re.I)),
        "unsupported": len(re.findall(r"unsupported|insufficient|suppress", src, re.I)),
        "contradict": len(re.findall(r"contradict|contradiction_pressure", src, re.I)),
        "conservatism": len(re.findall(r"conservatism|restraint|cannot_conclude", src, re.I)),
        "fragility": len(re.findall(r"fragility|fragile", src, re.I)),
        "inflation": len(re.findall(r"inflate|0\.9|overconfident", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("restraint", "overreach", "unsupported", "contradict", "conservatism", "fragility", "inflation", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "semantic_restraint": round(agg["restraint"] / n, 3),
        "semantic_overreach": round(agg["overreach"] / n, 3),
        "unsupported_density": round(agg["unsupported"] / n, 3),
        "contradiction_suppression": round(agg["contradict"] / n, 3),
        "semantic_conservatism": round(agg["conservatism"] / n, 3),
        "fragility_pressure": round(agg["fragility"] / n, 3),
        "confidence_overexpansion": round(agg["inflation"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "semantic_overreach_density": {d: stats[d].get("semantic_overreach", 0) for d in domains},
        "unsupported_reconciliation_matrix": stats.get("evidence", {}),
        "ontology_overexpansion_matrix": stats.get("knowledge", {}),
        "topology_overexpansion_matrix": stats.get("repository", {}),
        "confidence_overexpansion_matrix": {d: stats[d].get("confidence_overexpansion", 0) for d in domains},
        "semantic_bridge_overreach": stats.get("graph", {}),
        "semantic_expansion_pressure": {d: stats[d].get("semantic_overreach", 0) for d in domains},
        "unsupported_semantic_links": stats.get("graph", {}),
        "unsupported_entity_merges": stats.get("knowledge", {}),
        "unsupported_topology_propagation": stats.get("repository", {}),
        "unsupported_ontology_propagation": stats.get("knowledge", {}),
        "semantic_restraint_matrix": {d: stats[d].get("semantic_restraint", 0) for d in domains},
        "semantic_conservatism_matrix": {d: stats[d].get("semantic_conservatism", 0) for d in domains},
        "inference_expansion_matrix": {d: stats[d].get("semantic_overreach", 0) for d in domains},
        "semantic_noninference_matrix": {d: stats[d].get("semantic_restraint", 0) for d in domains},
        "confidence_cap_matrix": {d: stats[d].get("fragility_pressure", 0) for d in domains},
        "fragility_pressure_matrix": {d: stats[d].get("fragility_pressure", 0) for d in domains},
        "heuristic_expansion_residue": {d: stats[d].get("heuristic_residue", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
