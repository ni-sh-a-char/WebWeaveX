#!/usr/bin/env python3
"""Deterministic epistemic audit — scripts/deterministic_epistemic_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "deterministic_epistemic_audit"
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
        "epistemic": len(re.findall(r"epistemic|sufficiency|incompleteness|reliability|weakness", src, re.I)),
        "uncertainty": len(re.findall(r"uncertain|ambigu|weak_evidence", src, re.I)),
        "contradict": len(re.findall(r"contradict|preserve", src, re.I)),
        "support": len(re.findall(r"support|corroborat", src, re.I)),
        "trace": len(re.findall(r"traceability|lineage|provenance", src, re.I)),
        "confidence": len(re.findall(r"confidence_basis|deterministic_inputs", src)),
        "unsupported": len(re.findall(r"unsupported|insufficient|missing_edge", src, re.I)),
        "regex": len(re.findall(r"re\.(findall|search)", src)),
        "parser": len(re.findall(r"parse_source|parser_basis", src)),
    }


def domain(name: str) -> dict:
    files = list(iter_py(CORE / name))
    if not files:
        return {"files": 0}
    agg = {k: 0 for k in ("epistemic", "uncertainty", "contradict", "support", "trace", "confidence", "unsupported", "regex", "parser")}
    for p in files:
        s = analyze(p)
        for k in agg:
            agg[k] += s[k]
    n = len(files)
    denom = max(1, agg["parser"] + agg["regex"])
    return {
        "files": n,
        "epistemic_density": round(agg["epistemic"] / n, 3),
        "uncertainty_preservation": round(agg["uncertainty"] / n, 3),
        "contradiction_preservation": round(agg["contradict"] / n, 3),
        "confidence_explainability": round(agg["confidence"] / n, 3),
        "traceability_density": round(min(1.0, agg["trace"] / (n * 2)), 3),
        "unsupported_inference_density": round(agg["unsupported"] / n, 3),
        "epistemic_grounding": round(agg["parser"] / denom, 3),
        "heuristic_residue": round(agg["regex"] / denom, 3),
    }


def residue_paths() -> list:
    out = []
    for d in ("repository", "documents", "internet"):
        for p in iter_py(CORE / d):
            s = analyze(p)
            if s["regex"] > 0 and s["parser"] == 0 and s["epistemic"] == 0:
                out.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return sorted(out)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domains = ("parsers", "evidence", "semantic", "repository", "documents", "internet", "knowledge", "graph")
    stats = {d: domain(d) for d in domains}
    residue = residue_paths()

    artifacts = {
        "epistemic_confidence_matrix": {d: stats[d].get("confidence_explainability", 0) for d in domains},
        "epistemic_uncertainty_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "epistemic_ambiguity_matrix": {d: stats[d].get("uncertainty_preservation", 0) for d in domains},
        "epistemic_contradiction_matrix": {d: stats[d].get("contradiction_preservation", 0) for d in domains},
        "epistemic_support_matrix": {d: stats[d].get("epistemic_density", 0) for d in domains},
        "epistemic_reliability_matrix": stats.get("evidence", {}),
        "epistemic_lineage_matrix": {d: stats[d].get("traceability_density", 0) for d in domains},
        "epistemic_traceability_matrix": {d: stats[d].get("traceability_density", 0) for d in domains},
        "epistemic_provenance_matrix": {d: stats[d].get("traceability_density", 0) for d in domains},
        "epistemic_gap_matrix": {d: stats[d].get("unsupported_inference_density", 0) for d in domains},
        "epistemic_incompleteness_matrix": {d: stats[d].get("unsupported_inference_density", 0) for d in domains},
        "epistemic_grounding_matrix": {d: stats[d].get("epistemic_grounding", 0) for d in domains},
        "semantic_certainty_matrix": {d: round(1.0 - stats[d].get("unsupported_inference_density", 0), 3) for d in domains},
        "semantic_weakness_matrix": {d: stats[d].get("unsupported_inference_density", 0) for d in domains},
        "confidence_explainability_matrix": {d: stats[d].get("confidence_explainability", 0) for d in domains},
        "unsupported_inference_matrix": {d: stats[d].get("unsupported_inference_density", 0) for d in domains},
        "heuristic_epistemic_residue": {"paths": residue[:150], "count": len(residue)},
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": stats, "residue_count": len(residue)}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
