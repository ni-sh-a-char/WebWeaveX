#!/usr/bin/env python3
"""Civilizational epistemic openness audit — scripts/civilizational_epistemic_openness_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "civilizational_epistemic_openness_audit"
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
        "openness": len(re.findall(r"openness|divergence|explor|novelty|variance", src, re.I)),
        "attractor": len(re.findall(r"attractor|gravity|convergence|fixation|stabiliz", src, re.I)),
        "entropy": len(re.findall(r"entropy|phase.?space", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("openness", "attractor", "entropy", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "openness": round(agg["openness"] / n, 3),
        "convergence_pressure": round(agg["attractor"] / n, 3),
        "entropy_preservation": round(agg["entropy"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "semantic_attractor_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "epistemic_gravity_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "worldview_convergence_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "ontology_convergence_matrix": stats.get("knowledge", {}),
        "interpretive_convergence_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "explanatory_convergence_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "recursive_novelty_decay_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "semantic_phase_space_matrix": {d: stats[d].get("entropy_preservation", 0) for d in domains},
        "exploratory_capacity_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "semantic_divergence_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "ontology_divergence_matrix": stats.get("knowledge", {}),
        "explanatory_divergence_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "worldview_variance_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "recursive_exploration_matrix": {d: stats[d].get("openness", 0) for d in domains},
        "semantic_entropy_matrix": {d: stats[d].get("entropy_preservation", 0) for d in domains},
        "cognitive_gravity_well_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "recursive_stabilization_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "recursive_semantic_fixation_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "recursive_explanatory_fixation_matrix": {d: stats[d].get("convergence_pressure", 0) for d in domains},
        "civilizational_openness_matrix": {d: stats[d].get("openness", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
