#!/usr/bin/env python3
"""Absolute semantic realization audit — scripts/absolute_semantic_audit/*.json"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "absolute_semantic_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
DOMAINS = ("parsers", "repository", "documents", "internet", "knowledge", "graph", "extract", "evidence", "semantic")


def iter_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def classify(path: Path) -> dict:
    src = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "parser": len(re.findall(r"parse_source|parse_ast|ParserRegistry|ast\.parse|tree_sitter", src)),
        "regex": len(re.findall(r"re\.(findall|search|match|compile)", src)),
        "heuristic": len(re.findall(r"heuristic|text_fallback|keyword", src, re.I)),
        "evidence": len(re.findall(r"\"evidence\"|provenance|grounding|lineage|confidence_basis", src)),
        "provenance": len(re.findall(r"observed|inferred|reconciled|provenance_engine", src)),
    }


def domain_stats(domain: str) -> dict:
    files = list(iter_py(CORE / domain))
    tp = tr = te = tf = 0
    shallow, grounded = [], []
    for p in files:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        s = classify(p)
        tp += s["parser"]
        tr += s["regex"]
        te += s["evidence"]
        tf += s["provenance"]
        if s["regex"] > 0 and s["parser"] == 0:
            shallow.append(rel)
        if s["parser"] > 0 and (s["evidence"] > 0 or s["provenance"] > 0):
            grounded.append(rel)
    d = max(1, tp + tr)
    return {
        "files": len(files),
        "parser_backed_ratio": round(tp / d, 3),
        "heuristic_fallback_ratio": round(tr / d, 3),
        "evidence_density": round(te / max(1, len(files)), 3),
        "provenance_density": round(tf / max(1, len(files)), 3),
        "shallow_modules": shallow[:30],
        "grounded_modules": grounded[:30],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    stats = {d: domain_stats(d) for d in DOMAINS}
    gaps = []
    for d, s in stats.items():
        if s.get("heuristic_fallback_ratio", 0) > 0.5:
            gaps.append({"domain": d, "issue": "high_heuristic_ratio", "ratio": s["heuristic_fallback_ratio"]})
        if not (CORE / d).exists() and d in ("evidence", "semantic"):
            gaps.append({"domain": d, "issue": "package_missing"})

    artifacts = {
        "semantic_grounding_matrix": {d: stats[d].get("evidence_density", 0) for d in DOMAINS},
        "parser_grounding_matrix": {d: stats[d].get("parser_backed_ratio", 0) for d in DOMAINS},
        "evidence_lineage_matrix": {d: stats[d].get("provenance_density", 0) for d in DOMAINS},
        "repository_cognition_depth": stats.get("repository", {}),
        "document_cognition_depth": stats.get("documents", {}),
        "internet_intelligence_depth": stats.get("internet", {}),
        "ontology_depth_matrix": stats.get("knowledge", {}),
        "graph_reasoning_depth": stats.get("graph", {}),
        "semantic_reconstruction_quality": {
            "repository": stats.get("repository", {}).get("parser_backed_ratio", 0),
            "documents": stats.get("documents", {}).get("parser_backed_ratio", 0),
        },
        "heuristic_fallback_matrix": {d: stats[d].get("heuristic_fallback_ratio", 0) for d in DOMAINS},
        "semantic_confidence_matrix": {"evidence_package": (CORE / "evidence").exists()},
        "semantic_provenance_matrix": {"evidence_modules": stats.get("evidence", {}).get("files", 0)},
        "semantic_lineage_matrix": {"semantic_modules": stats.get("semantic", {}).get("files", 0)},
        "semantic_gap_analysis": gaps,
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats, "gaps": len(gaps)}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
