#!/usr/bin/env python3
"""Reality alignment audit — scripts/reality_alignment_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "reality_alignment_audit"
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
        "reality": len(re.findall(r"reality|alignment|evidence_bound|parser_basis", src, re.I)),
        "drift": len(re.findall(r"drift|momentum|continuity|hallucin", src, re.I)),
        "stability": len(re.findall(r"stability|stable|instability", src, re.I)),
        "boundary": len(re.findall(r"boundary|bounded|constraint", src, re.I)),
        "illusion": len(re.findall(r"illusion|inflate|0\.9[0-9]|overconfident", src, re.I)),
        "coherence": len(re.findall(r"coherence|narrative|speculative", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis|ground", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("reality", "drift", "stability", "boundary", "illusion", "coherence", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "reality_alignment": round(agg["reality"] / n, 3),
        "semantic_drift": round(agg["drift"] / n, 3),
        "stability": round(agg["stability"] / n, 3),
        "boundary": round(agg["boundary"] / n, 3),
        "confidence_illusion": round(agg["illusion"] / n, 3),
        "speculative_coherence": round(agg["coherence"] / n, 3),
        "parser_reality_gap": round(1.0 - min(1.0, agg["parser"] / max(1, n * 2)), 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "reality_alignment_matrix": {d: stats[d].get("reality_alignment", 0) for d in domains},
        "semantic_drift_matrix": {d: stats[d].get("semantic_drift", 0) for d in domains},
        "ontology_drift_matrix": stats.get("knowledge", {}),
        "topology_drift_matrix": stats.get("repository", {}),
        "confidence_illusion_matrix": {d: stats[d].get("confidence_illusion", 0) for d in domains},
        "unsupported_continuity_matrix": {d: stats[d].get("semantic_drift", 0) for d in domains},
        "semantic_momentum_matrix": {d: stats[d].get("semantic_drift", 0) for d in domains},
        "narrative_hallucination_matrix": {d: stats[d].get("speculative_coherence", 0) for d in domains},
        "speculative_coherence_matrix": {d: stats[d].get("speculative_coherence", 0) for d in domains},
        "semantic_boundary_pressure": {d: stats[d].get("boundary", 0) for d in domains},
        "parser_reality_gap_matrix": {d: stats[d].get("parser_reality_gap", 0) for d in domains},
        "evidence_boundary_matrix": stats.get("evidence", {}),
        "reality_constraint_matrix": {d: stats[d].get("boundary", 0) for d in domains},
        "epistemic_boundary_matrix": stats.get("evidence", {}),
        "semantic_stability_matrix": {d: stats[d].get("stability", 0) for d in domains},
        "cognitive_stability_matrix": stats.get("evidence", {}),
        "ontology_stability_matrix": stats.get("knowledge", {}),
        "topology_stability_matrix": stats.get("repository", {}),
        "semantic_drift_pressure": {d: stats[d].get("semantic_drift", 0) for d in domains},
        "unsupported_expansion_pressure": {d: stats[d].get("speculative_coherence", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
