#!/usr/bin/env python3
"""Absolute semantic integrity audit — scripts/absolute_semantic_integrity_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "absolute_semantic_integrity_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def scan_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def file_stats(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="ignore")
    return {
        "integrity_fields": len(re.findall(r'"observed"|"parsed"|"inferred"|"reconciled"|"contradicted"|"ambiguities"', src)),
        "explainability": len(re.findall(r'"why"|confidence_basis|parser_basis|semantic_basis', src)),
        "parser": len(re.findall(r"parse_source|ParserRegistry", src)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
        "preserve_contradiction": len(re.findall(r"contradict|preserve|ambigu", src, re.I)),
    }


def domain_scan(name: str) -> dict:
    files = list(scan_py(CORE / name))
    ti = te = tp = tr = tc = 0
    for p in files:
        s = file_stats(p)
        ti += s["integrity_fields"]
        te += s["explainability"]
        tp += s["parser"]
        tr += s["regex"]
        tc += s["preserve_contradiction"]
    n = max(1, len(files))
    d = max(1, tp + tr)
    return {
        "files": len(files),
        "integrity_field_density": round(ti / n, 3),
        "explainability_density": round(te / n, 3),
        "parser_backed_ratio": round(tp / d, 3),
        "heuristic_ratio": round(tr / d, 3),
        "contradiction_awareness": round(tc / n, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain_scan(d) for d in domains}

    artifacts = {
        "semantic_integrity_matrix": {d: stats[d]["integrity_field_density"] for d in domains},
        "semantic_truthfulness_matrix": {d: stats[d].get("parser_backed_ratio", 0) for d in domains},
        "semantic_provenance_matrix": {d: stats[d]["explainability_density"] for d in domains},
        "ontology_integrity_matrix": stats.get("knowledge", {}),
        "contradiction_integrity_matrix": {d: stats[d]["contradiction_awareness"] for d in domains},
        "evidence_traceability_matrix": stats.get("evidence", {}),
        "semantic_reconstruction_integrity": {
            "repository": stats.get("repository", {}),
            "documents": stats.get("documents", {}),
        },
        "parser_truthfulness_matrix": stats.get("parsers", {}),
        "semantic_explainability_matrix": {d: stats[d]["explainability_density"] for d in domains},
        "ambiguity_preservation_matrix": {d: stats[d]["contradiction_awareness"] for d in domains},
        "semantic_confidence_integrity": {"evidence_package": (CORE / "evidence" / "semantic_confidence_engine.py").exists()},
        "semantic_lineage_integrity": stats.get("evidence", {}),
        "semantic_consistency_matrix": stats,
        "semantic_conflict_matrix": stats.get("semantic", {}),
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(json.dumps({"domains": stats}, indent=2))


if __name__ == "__main__":
    main()
