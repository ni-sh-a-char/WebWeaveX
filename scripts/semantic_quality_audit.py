#!/usr/bin/env python3
"""Semantic quality audit — emits scripts/semantic_quality_audit/*.json"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "semantic_quality_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}
DOMAINS = ("parsers", "repository", "documents", "internet", "knowledge", "graph", "extract")


def iter_domain_py(domain: str):
    base = CORE / domain
    if not base.exists():
        return
    for p in base.rglob("*.py"):
        if any(s in str(p) for s in SKIP):
            continue
        yield p


def classify_file(path: Path) -> dict:
    src = path.read_text(encoding="utf-8", errors="ignore")
    parser_hits = len(re.findall(r"parse_source|parse_ast|ParserRegistry|ast\.parse|tree_sitter", src))
    regex_hits = len(re.findall(r"re\.(findall|search|match|compile)", src))
    heuristic_hits = len(re.findall(r"heuristic|text_fallback|keyword", src, re.I))
    evidence_hits = len(re.findall(r"\"evidence\"|evidence=", src))
    return {
        "parser_signals": parser_hits,
        "regex_signals": regex_hits,
        "heuristic_signals": heuristic_hits,
        "evidence_signals": evidence_hits,
        "lines": src.count("\n") + 1,
    }


def domain_summary(domain: str) -> dict:
    files = list(iter_domain_py(domain))
    total_parser = total_regex = total_evidence = total_files = 0
    shallow = []
    grounded = []
    for p in files:
        rel = str(p.relative_to(CORE)).replace("\\", "/")
        stats = classify_file(p)
        total_files += 1
        total_parser += stats["parser_signals"]
        total_regex += stats["regex_signals"]
        total_evidence += stats["evidence_signals"]
        if stats["regex_signals"] > 0 and stats["parser_signals"] == 0:
            shallow.append(rel)
        if stats["parser_signals"] > 0 and stats["evidence_signals"] > 0:
            grounded.append(rel)
    denom = max(1, total_parser + total_regex)
    return {
        "files": total_files,
        "parser_backed_ratio": round(total_parser / denom, 3),
        "heuristic_fallback_ratio": round(total_regex / denom, 3),
        "evidence_grounding_ratio": round(total_evidence / max(1, total_files), 3),
        "shallow_modules": shallow[:40],
        "grounded_modules": grounded[:40],
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summaries = {d: domain_summary(d) for d in DOMAINS}
    all_parser = sum(s["parser_backed_ratio"] for s in summaries.values())
    all_regex = sum(s["heuristic_fallback_ratio"] for s in summaries.values())

    artifacts = {
        "parser_grounding_quality": summaries.get("parsers", {}),
        "semantic_reconstruction_quality": {
            "repository": summaries.get("repository", {}),
            "documents": summaries.get("documents", {}),
            "aggregate_parser_ratio": round(all_parser / len(DOMAINS), 3),
        },
        "evidence_grounding_quality": {
            d: summaries[d].get("evidence_grounding_ratio", 0) for d in DOMAINS
        },
        "repository_cognition_quality": summaries.get("repository", {}),
        "document_cognition_quality": summaries.get("documents", {}),
        "internet_intelligence_quality": summaries.get("internet", {}),
        "ontology_quality": summaries.get("knowledge", {}),
        "graph_reasoning_quality": summaries.get("graph", {}),
        "extraction_fidelity_quality": summaries.get("extract", {}),
    }

    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

    summary = {
        "domains": summaries,
        "global_parser_backed_ratio": round(all_parser / len(DOMAINS), 3),
        "global_heuristic_ratio": round(all_regex / len(DOMAINS), 3),
    }
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
