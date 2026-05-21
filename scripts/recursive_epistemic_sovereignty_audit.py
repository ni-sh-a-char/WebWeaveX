#!/usr/bin/env python3
"""Recursive epistemic sovereignty audit — scripts/recursive_epistemic_sovereignty_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "recursive_epistemic_sovereignty_audit"
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
        "sovereignty": len(re.findall(r"sovereignty|self.?determin|independence|agency", src, re.I)),
        "dependency": len(re.findall(r"dependency|reliance|obedience|submission|domesticat", src, re.I)),
        "guardianship": len(re.findall(r"guardianship|paternalism|centrality", src, re.I)),
        "passivity": len(re.findall(r"passivity|passive|steering", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("sovereignty", "dependency", "guardianship", "passivity", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "sovereignty": round(agg["sovereignty"] / n, 3),
        "dependency_pressure": round(agg["dependency"] / n, 3),
        "guardianship_pressure": round(agg["guardianship"] / n, 3),
        "passivity_pressure": round(agg["passivity"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "recursive_dependency_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "semantic_dependency_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "interpretive_dependency_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "ontology_dependency_matrix": stats.get("knowledge", {}),
        "authority_dependency_matrix": {d: stats[d].get("guardianship_pressure", 0) for d in domains},
        "recursive_obedience_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_semantic_submission_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_trust_submission_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_worldview_dependency_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_narrative_dependency_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_semantic_domestication_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_explanatory_submission_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_guardianship_matrix": {d: stats[d].get("guardianship_pressure", 0) for d in domains},
        "recursive_cognitive_centrality_matrix": {d: stats[d].get("guardianship_pressure", 0) for d in domains},
        "recursive_epistemic_dependency_matrix": stats.get("evidence", {}),
        "recursive_semantic_passivity_matrix": {d: stats[d].get("passivity_pressure", 0) for d in domains},
        "recursive_interpretive_passivity_matrix": {d: stats[d].get("passivity_pressure", 0) for d in domains},
        "recursive_autonomy_erosion_matrix": {d: stats[d].get("dependency_pressure", 0) for d in domains},
        "recursive_agency_preservation_matrix": {d: stats[d].get("sovereignty", 0) for d in domains},
        "recursive_epistemic_sovereignty_matrix": {d: stats[d].get("sovereignty", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
