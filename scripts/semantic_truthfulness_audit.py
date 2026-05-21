#!/usr/bin/env python3
"""Semantic truthfulness audit — scripts/semantic_truthfulness_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "semantic_truthfulness_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}

INTEGRITY_KEYS = (
    "observed",
    "parsed",
    "inferred",
    "reconciled",
    "contradicted",
    "derived",
    "ambiguities",
)
EXPLAIN_KEYS = ("why", "parser_basis", "graph_basis", "semantic_basis", "confidence_basis")


def iter_py(base: Path):
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def analyze_file(p: Path) -> dict:
    src = p.read_text(encoding="utf-8", errors="ignore")
    parser_hits = len(re.findall(r"parse_source|ParserRegistry|structure_cognition", src))
    regex_hits = len(re.findall(r"re\.(findall|search|match)", src))
    integrity_hits = sum(1 for k in INTEGRITY_KEYS if f'"{k}"' in src or f"'{k}'" in src)
    explain_hits = sum(1 for k in EXPLAIN_KEYS if k in src)
    provenance_hits = len(re.findall(r"evidence|lineage|grounding|provenance", src, re.I))
    contradict_hits = len(re.findall(r"contradict|preserve_contradict|collapsed", src, re.I))
    ambig_hits = len(re.findall(r"ambigu|uncertain|weak_evidence", src, re.I))
    return {
        "parser_hits": parser_hits,
        "regex_hits": regex_hits,
        "integrity_hits": integrity_hits,
        "explain_hits": explain_hits,
        "provenance_hits": provenance_hits,
        "contradict_hits": contradict_hits,
        "ambig_hits": ambig_hits,
        "uses_structure_cognition": "structure_cognition" in src,
    }


def domain_metrics(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0, "parser_grounded_ratio": 0.0, "heuristic_only_ratio": 0.0}
    agg = {k: 0 for k in ("parser_hits", "regex_hits", "integrity_hits", "explain_hits", "provenance_hits", "contradict_hits", "ambig_hits")}
    cognition_files = 0
    for p in files:
        s = analyze_file(p)
        for k in agg:
            agg[k] += s[k]
        if s["uses_structure_cognition"]:
            cognition_files += 1
    n = len(files)
    denom = max(1, agg["parser_hits"] + agg["regex_hits"])
    return {
        "files": n,
        "parser_grounded_ratio": round(agg["parser_hits"] / denom, 3),
        "evidence_grounded_ratio": round(agg["provenance_hits"] / (n * 5), 3),
        "heuristic_only_ratio": round(agg["regex_hits"] / denom, 3),
        "provenance_coverage": round(min(1.0, agg["provenance_hits"] / (n * 3)), 3),
        "explainability_coverage": round(min(1.0, agg["explain_hits"] / max(1, n)), 3),
        "integrity_coverage": round(min(1.0, agg["integrity_hits"] / (len(INTEGRITY_KEYS))), 3),
        "contradiction_preservation": round(agg["contradict_hits"] / n, 3),
        "ambiguity_preservation": round(agg["ambig_hits"] / n, 3),
        "structure_cognition_files": cognition_files,
        "semantic_truthfulness": round((agg["parser_hits"] + agg["integrity_hits"]) / (denom + len(INTEGRITY_KEYS)), 3),
        "semantic_realism": round(1.0 - (agg["regex_hits"] / denom) * 0.5, 3),
    }


def hallucination_risk(name: str) -> float:
    m = domain_metrics(name)
    return round(m["heuristic_only_ratio"] * (1.0 - m["provenance_coverage"]), 3)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain_metrics(d) for d in domains}

    heuristic_paths = []
    for d in domains:
        for p in iter_py(CORE / d):
            s = analyze_file(p)
            if s["regex_hits"] > 0 and s["parser_hits"] == 0:
                heuristic_paths.append(str(p.relative_to(ROOT)).replace("\\", "/"))

    artifacts = {
        "semantic_truthfulness_matrix": {d: stats[d]["semantic_truthfulness"] for d in domains},
        "semantic_realism_matrix": {d: stats[d]["semantic_realism"] for d in domains},
        "semantic_hallucination_risk": {d: hallucination_risk(d) for d in domains},
        "semantic_provenance_coverage": {d: stats[d]["provenance_coverage"] for d in domains},
        "ontology_provenance_coverage": stats.get("knowledge", {}),
        "contradiction_preservation_coverage": {d: stats[d]["contradiction_preservation"] for d in domains},
        "ambiguity_preservation_coverage": {d: stats[d]["ambiguity_preservation"] for d in domains},
        "semantic_explainability_coverage": {d: stats[d]["explainability_coverage"] for d in domains},
        "parser_grounding_coverage": {d: stats[d]["parser_grounded_ratio"] for d in domains},
        "heuristic_semantic_paths": {"paths": sorted(heuristic_paths)[:200], "count": len(heuristic_paths)},
        "evidence_density_matrix": {d: stats[d]["evidence_grounded_ratio"] for d in domains},
        "semantic_confidence_integrity": {
            "canonical_engine": (CORE / "evidence" / "semantic_confidence_engine.py").exists(),
            "conservatism_engine": (CORE / "evidence" / "semantic_conservatism_engine.py").exists(),
        },
        "semantic_lineage_coverage": {d: stats[d].get("provenance_coverage", 0) for d in domains},
        "semantic_fidelity_matrix": {
            d: round((stats[d]["parser_grounded_ratio"] + stats[d]["integrity_coverage"]) / 2, 3)
            for d in domains
        },
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats, "heuristic_path_count": len(heuristic_paths)}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
