#!/usr/bin/env python3
"""Cognitive anti-capture audit — scripts/cognitive_anti_capture_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "cognitive_anti_capture_audit"
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
        "capture": len(re.findall(r"capture|monopoly|hegemony|dominance|authoritarian", src, re.I)),
        "autonomy": len(re.findall(r"autonomy|freedom|anti.?capture|decentral", src, re.I)),
        "competition": len(re.findall(r"competition|plurality|alternative", src, re.I)),
        "trust": len(re.findall(r"trust.*monopoly|trust.*absolut", src, re.I)),
        "governance": len(re.findall(r"governance|centraliz|hierarchy", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("capture", "autonomy", "competition", "trust", "governance", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "capture_pressure": round(agg["capture"] / n, 3),
        "autonomy": round(agg["autonomy"] / n, 3),
        "competition": round(agg["competition"] / n, 3),
        "governance_pressure": round(agg["governance"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "semantic_capture_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "ontology_capture_matrix": stats.get("knowledge", {}),
        "authority_capture_matrix": {d: stats[d].get("governance_pressure", 0) for d in domains},
        "interpretive_capture_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_consensus_capture_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_narrative_capture_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_worldview_capture_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_semantic_hierarchy_matrix": {d: stats[d].get("governance_pressure", 0) for d in domains},
        "recursive_trust_monopoly_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_evidence_monopoly_matrix": stats.get("evidence", {}),
        "recursive_lineage_monopoly_matrix": stats.get("evidence", {}),
        "recursive_semantic_empire_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_ontology_dominance_matrix": stats.get("knowledge", {}),
        "recursive_explanatory_monopoly_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_semantic_authoritarianism_matrix": {d: stats[d].get("governance_pressure", 0) for d in domains},
        "recursive_cognitive_centralization_matrix": {d: stats[d].get("governance_pressure", 0) for d in domains},
        "recursive_semantic_governance_matrix": {d: stats[d].get("governance_pressure", 0) for d in domains},
        "recursive_capture_pressure_matrix": {d: stats[d].get("capture_pressure", 0) for d in domains},
        "recursive_semantic_autonomy_matrix": {d: stats[d].get("autonomy", 0) for d in domains},
        "recursive_cognitive_freedom_matrix": {d: stats[d].get("autonomy", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
