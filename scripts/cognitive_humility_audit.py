#!/usr/bin/env python3
"""Cognitive humility audit — scripts/cognitive_humility_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "cognitive_humility_audit"
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
        "humility": len(re.findall(r"humility|self_limitation|cannot_determine|noninferable", src, re.I)),
        "certainty": len(re.findall(r"certainty|overconfident|0\.9[0-9]|assert.*true", src, re.I)),
        "recovery": len(re.findall(r"recover.*confidence|restore.*confidence|boost.*confidence", src, re.I)),
        "speculation": len(re.findall(r"speculat|optimistic|possibly_true", src, re.I)),
        "uncertainty": len(re.findall(r"uncertain|uncertainty", src, re.I)),
        "ambiguity": len(re.findall(r"ambigu", src, re.I)),
        "fragility": len(re.findall(r"fragility|fragile", src, re.I)),
        "restraint": len(re.findall(r"restraint|noninference|suppressed", src, re.I)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("humility", "certainty", "recovery", "speculation", "uncertainty", "ambiguity", "fragility", "restraint", "parser", "regex")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "humility_density": round(agg["humility"] / n, 3),
        "certainty_pressure": round(agg["certainty"] / n, 3),
        "confidence_recovery": round(agg["recovery"] / n, 3),
        "speculation_density": round(agg["speculation"] / n, 3),
        "uncertainty_visibility": round(agg["uncertainty"] / n, 3),
        "ambiguity_visibility": round(agg["ambiguity"] / n, 3),
        "fragility_visibility": round(agg["fragility"] / n, 3),
        "restraint_quality": round(agg["restraint"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}

    artifacts = {
        "semantic_certainty_pressure": {d: stats[d].get("certainty_pressure", 0) for d in domains},
        "unsupported_certainty_matrix": stats.get("evidence", {}),
        "confidence_recovery_paths": {d: stats[d].get("confidence_recovery", 0) for d in domains},
        "semantic_overconfidence_matrix": {d: stats[d].get("certainty_pressure", 0) for d in domains},
        "ontology_certainty_pressure": stats.get("knowledge", {}),
        "topology_certainty_pressure": stats.get("repository", {}),
        "semantic_speculation_matrix": {d: stats[d].get("speculation_density", 0) for d in domains},
        "unsupported_confidence_paths": stats.get("evidence", {}),
        "fragility_visibility_matrix": {d: stats[d].get("fragility_visibility", 0) for d in domains},
        "uncertainty_visibility_matrix": {d: stats[d].get("uncertainty_visibility", 0) for d in domains},
        "ambiguity_visibility_matrix": {d: stats[d].get("ambiguity_visibility", 0) for d in domains},
        "noninferable_scope_matrix": {d: stats[d].get("humility_density", 0) for d in domains},
        "semantic_humility_matrix": {d: stats[d].get("humility_density", 0) for d in domains},
        "epistemic_restraint_quality": {d: stats[d].get("restraint_quality", 0) for d in domains},
        "semantic_self_limitation_matrix": {d: stats[d].get("humility_density", 0) for d in domains},
        "unsupported_confidence_escalation": {d: stats[d].get("confidence_recovery", 0) for d in domains},
        "semantic_fragility_pressure": {d: stats[d].get("fragility_visibility", 0) for d in domains},
        "semantic_overassertion_matrix": {d: stats[d].get("certainty_pressure", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
