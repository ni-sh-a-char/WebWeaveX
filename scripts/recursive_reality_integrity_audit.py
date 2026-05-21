#!/usr/bin/env python3
"""Recursive reality integrity audit — scripts/recursive_reality_integrity_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "recursive_reality_integrity_audit"
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
        "recursive": len(re.findall(r"recursive|depth|chain|merge", src, re.I)),
        "stabilize": len(re.findall(r"stabiliz|closure|lock.?in|normalize", src, re.I)),
        "echo": len(re.findall(r"echo|amplify|reinforc|accumul", src, re.I)),
        "collapse": len(re.findall(r"collapse.*uncertain|suppress.*ambigu|smooth.*contradict", src, re.I)),
        "entropy": len(re.findall(r"entropy|instability", src, re.I)),
        "drift": len(re.findall(r"drift|detach|lineage.*decay", src, re.I)),
        "truth": len(re.findall(r"truth|provenance|lineage", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("recursive", "stabilize", "echo", "collapse", "entropy", "drift", "truth", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "recursive_stabilization": round(agg["stabilize"] / n, 3),
        "recursive_closure": round(agg["stabilize"] / n, 3),
        "confidence_echo": round(agg["echo"] / n, 3),
        "entropy_suppression": round(agg["collapse"] / n, 3),
        "reality_drift": round(agg["drift"] / n, 3),
        "recursive_integrity": round(agg["truth"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "recursive_stabilization_matrix": {d: stats[d].get("recursive_stabilization", 0) for d in domains},
        "recursive_coherence_pressure": {d: stats[d].get("recursive_closure", 0) for d in domains},
        "recursive_confidence_echo_matrix": {d: stats[d].get("confidence_echo", 0) for d in domains},
        "recursive_entropy_suppression_matrix": {d: stats[d].get("entropy_suppression", 0) for d in domains},
        "recursive_uncertainty_collapse_matrix": {d: stats[d].get("entropy_suppression", 0) for d in domains},
        "recursive_ambiguity_collapse_matrix": {d: stats[d].get("entropy_suppression", 0) for d in domains},
        "recursive_contradiction_collapse_matrix": {d: stats[d].get("entropy_suppression", 0) for d in domains},
        "recursive_reality_drift_matrix": {d: stats[d].get("reality_drift", 0) for d in domains},
        "recursive_semantic_closure_matrix": {d: stats[d].get("recursive_closure", 0) for d in domains},
        "recursive_ontology_lock_matrix": stats.get("knowledge", {}),
        "recursive_topology_lock_matrix": stats.get("repository", {}),
        "recursive_truth_boundary_matrix": stats.get("evidence", {}),
        "recursive_inference_amplification_matrix": {d: stats[d].get("confidence_echo", 0) for d in domains},
        "recursive_self_confirmation_matrix": {d: stats[d].get("recursive_stabilization", 0) for d in domains},
        "recursive_lineage_decay_matrix": {d: stats[d].get("reality_drift", 0) for d in domains},
        "recursive_evidence_detachment_matrix": {d: stats[d].get("reality_drift", 0) for d in domains},
        "recursive_semantic_inflation_matrix": {d: stats[d].get("confidence_echo", 0) for d in domains},
        "recursive_cognitive_drift_matrix": {d: stats[d].get("reality_drift", 0) for d in domains},
        "recursive_truthfulness_matrix": {d: stats[d].get("recursive_integrity", 0) for d in domains},
        "recursive_integrity_matrix": {d: stats[d].get("recursive_integrity", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
