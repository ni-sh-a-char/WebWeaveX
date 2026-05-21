#!/usr/bin/env python3
"""Epistemic civilization stability audit — scripts/epistemic_civilization_stability_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "epistemic_civilization_stability_audit"
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
        "plurality": len(re.findall(r"plurality|diversity|plural|alternative|decentral", src, re.I)),
        "monoculture": len(re.findall(r"monoculture|orthodoxy|hardening|uniform|convergence", src, re.I)),
        "openness": len(re.findall(r"openness|anti.?closure|anti.?dogma|interpretive", src, re.I)),
        "consensus": len(re.findall(r"consensus|worldview|homogen", src, re.I)),
        "contradict": len(re.findall(r"contradict|preserve", src, re.I)),
        "entropy": len(re.findall(r"entropy|instability", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("plurality", "monoculture", "openness", "consensus", "contradict", "entropy", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "plurality": round(agg["plurality"] / n, 3),
        "monoculture_pressure": round(agg["monoculture"] / n, 3),
        "epistemic_openness": round(agg["openness"] / n, 3),
        "consensus_pressure": round(agg["consensus"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "semantic_monoculture_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "ontology_hardening_matrix": stats.get("knowledge", {}),
        "recursive_consensus_matrix": {d: stats[d].get("consensus_pressure", 0) for d in domains},
        "recursive_worldview_lock_matrix": {d: stats[d].get("consensus_pressure", 0) for d in domains},
        "recursive_interpretive_closure_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "recursive_semantic_orthodoxy_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "recursive_plurality_decay_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_evidence_homogenization_matrix": stats.get("evidence", {}),
        "recursive_lineage_homogenization_matrix": stats.get("evidence", {}),
        "recursive_interpretive_suppression_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "recursive_semantic_centralization_matrix": {d: stats[d].get("consensus_pressure", 0) for d in domains},
        "recursive_semantic_uniformity_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "recursive_alternative_suppression_matrix": {d: stats[d].get("monoculture_pressure", 0) for d in domains},
        "recursive_explanatory_diversity_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_semantic_decentralization_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_epistemic_openness_matrix": {d: stats[d].get("epistemic_openness", 0) for d in domains},
        "recursive_truth_plurality_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_reality_diversity_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_semantic_diversity_matrix": {d: stats[d].get("plurality", 0) for d in domains},
        "recursive_cognitive_pluralism_matrix": {d: stats[d].get("plurality", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
