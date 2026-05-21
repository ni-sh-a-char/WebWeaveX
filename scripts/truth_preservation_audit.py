#!/usr/bin/env python3
"""Truth preservation audit — scripts/truth_preservation_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "truth_preservation_audit"
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
        "truth": len(re.findall(r"truth|preserv|incomplet|honest", src, re.I)),
        "stabilize": len(re.findall(r"stabiliz|normalize|smooth|reinforc|echo", src, re.I)),
        "decay": len(re.findall(r"decay|collapse|entropy|instability", src, re.I)),
        "suppress": len(re.findall(r"suppress.*contradict|hide.*ambigu|collapse.*uncertain", src, re.I)),
        "contradict": len(re.findall(r"contradict|preserve_contradict", src, re.I)),
        "uncertainty": len(re.findall(r"uncertain", src, re.I)),
        "ambiguity": len(re.findall(r"ambigu", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("truth", "stabilize", "decay", "suppress", "contradict", "uncertainty", "ambiguity", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "truth_preservation": round(agg["truth"] / n, 3),
        "unsupported_stabilization": round(agg["stabilize"] / n, 3),
        "semantic_decay": round(agg["decay"] / n, 3),
        "suppression_pressure": round(agg["suppress"] / n, 3),
        "contradiction_visibility": round(agg["contradict"] / n, 3),
        "uncertainty_visibility": round(agg["uncertainty"] / n, 3),
        "ambiguity_visibility": round(agg["ambiguity"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "truth_preservation_matrix": {d: stats[d].get("truth_preservation", 0) for d in domains},
        "semantic_decay_matrix": {d: stats[d].get("semantic_decay", 0) for d in domains},
        "unsupported_stabilization_matrix": {d: stats[d].get("unsupported_stabilization", 0) for d in domains},
        "confidence_echo_matrix": {d: stats[d].get("unsupported_stabilization", 0) for d in domains},
        "ontology_self_reinforcement_matrix": stats.get("knowledge", {}),
        "topology_self_confirmation_matrix": stats.get("repository", {}),
        "semantic_coherence_pressure": {d: stats[d].get("unsupported_stabilization", 0) for d in domains},
        "contradiction_suppression_matrix": {d: stats[d].get("suppression_pressure", 0) for d in domains},
        "uncertainty_suppression_matrix": {d: stats[d].get("suppression_pressure", 0) for d in domains},
        "ambiguity_suppression_matrix": {d: stats[d].get("suppression_pressure", 0) for d in domains},
        "truth_boundary_matrix": stats.get("evidence", {}),
        "semantic_instability_matrix": {d: stats[d].get("semantic_decay", 0) for d in domains},
        "evidence_decay_matrix": stats.get("evidence", {}),
        "unsupported_normalization_matrix": {d: stats[d].get("unsupported_stabilization", 0) for d in domains},
        "reality_decay_matrix": {d: stats[d].get("semantic_decay", 0) for d in domains},
        "semantic_entropy_matrix": {d: stats[d].get("semantic_decay", 0) for d in domains},
        "cognitive_truthfulness_matrix": stats.get("evidence", {}),
        "epistemic_truthfulness_matrix": stats.get("evidence", {}),
        "semantic_truth_pressure": {d: stats[d].get("truth_preservation", 0) for d in domains},
        "unsupported_reinforcement_matrix": {d: stats[d].get("unsupported_stabilization", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
