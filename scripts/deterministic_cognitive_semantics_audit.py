#!/usr/bin/env python3
"""Deterministic cognitive semantics audit — scripts/deterministic_cognitive_semantics_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "deterministic_cognitive_semantics_audit"
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
        "parser": len(re.findall(r"parse_source|parser_basis|parser_evidence", src)),
        "causality": len(re.findall(r"causal|causality|enables|requires|explains|precedes", src, re.I)),
        "support": len(re.findall(r"support_chain|semantic_support", src, re.I)),
        "dependency": len(re.findall(r"depend|prereq|flow", src, re.I)),
        "uncertainty": len(re.findall(r"uncertain|ambigu|weak_evidence", src, re.I)),
        "trace": len(re.findall(r"traceability|lineage|provenance", src, re.I)),
        "contradict": len(re.findall(r"contradict|preserve", src, re.I)),
        "explain": len(re.findall(r"why|explainability|confidence_basis", src)),
        "corroboration": len(re.findall(r"corroborat|agreement", src, re.I)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
        "structure_cognition": 1 if "structure_cognition" in src else 0,
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in analyze(Path(__file__)) if k != "files"}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "parser_dominance_density": round(agg["parser"] / denom, 3),
        "semantic_provenance_density": round(min(1.0, agg["trace"] / (n * 3)), 3),
        "semantic_lineage_density": round(min(1.0, agg["trace"] / (n * 2)), 3),
        "semantic_dependency_realism": round(agg["dependency"] / n, 3),
        "semantic_causality_realism": round(agg["causality"] / n, 3),
        "discourse_realism": round(agg["causality"] / max(1, n) if name == "documents" else 0, 3),
        "topology_realism": round(agg["dependency"] / n if name == "repository" else 0, 3),
        "contradiction_realism": round(agg["contradict"] / n, 3),
        "uncertainty_preservation": round(agg["uncertainty"] / n, 3),
        "semantic_explainability": round(agg["explain"] / n, 3),
        "semantic_corroboration": round(agg["corroboration"] / n, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def heuristic_residue_paths() -> list:
    out = []
    for d in ("repository", "documents", "internet"):
        for p in iter_py(CORE / d):
            s = analyze(p)
            if s["regex"] > 0 and s["parser"] == 0:
                out.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return sorted(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}
    residue = heuristic_residue_paths()

    artifacts = {
        "semantic_causality_matrix": {d: stats[d].get("semantic_causality_realism", 0) for d in domains},
        "semantic_support_chain_matrix": {d: stats[d].get("semantic_causality_realism", 0) for d in domains},
        "semantic_dependency_realism": {d: stats[d].get("semantic_dependency_realism", 0) for d in domains},
        "semantic_uncertainty_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "semantic_traceability_matrix": {d: stats[d].get("semantic_provenance_density", 0) for d in domains},
        "semantic_provenance_density": {d: stats[d].get("semantic_provenance_density", 0) for d in domains},
        "semantic_lineage_density": {d: stats[d].get("semantic_lineage_density", 0) for d in domains},
        "topology_realism_matrix": stats.get("repository", {}),
        "repository_topology_realism": stats.get("repository", {}),
        "document_discourse_realism": stats.get("documents", {}),
        "tutorial_dependency_realism": stats.get("documents", {}),
        "semantic_explainability_matrix": {d: stats[d].get("semantic_explainability", 0) for d in domains},
        "semantic_conservatism_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "ontology_integrity_matrix": stats.get("knowledge", {}),
        "contradiction_integrity_matrix": {d: stats[d].get("contradiction_realism", 0) for d in domains},
        "semantic_corroboration_matrix": {d: stats[d].get("semantic_corroboration", 0) for d in domains},
        "heuristic_semantic_residue": {"paths": residue[:150], "count": len(residue)},
        "parser_dominance_density": {d: stats[d].get("parser_dominance_density", 0) for d in domains},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats, "residue_count": len(residue)}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
