#!/usr/bin/env python3
"""Semantic execution realization audit — scripts/semantic_execution_realization_audit/*.json"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "core"
OUT = ROOT / "scripts" / "semantic_execution_realization_audit"
SKIP = {"webweavex-1.1.1", "__pycache__", ".pytest_cache"}


def scan(name: str) -> dict:
    base = CORE / name
    if not base.exists():
        return {"exists": False, "files": 0}
    files = [p for p in base.rglob("*.py") if not any(s in str(p) for s in SKIP)]
    src = ""
    for p in files[:300]:
        src += p.read_text(encoding="utf-8", errors="ignore")
    n = max(1, len(files))
    return {
        "exists": True,
        "files": len(files),
        "execution_refs": round(len(re.findall(r"runtime|execution|transition|state_machine|causality", src, re.I)) / n, 3),
        "parser_refs": round(len(re.findall(r"parse_source|parser_grounding|ParserRegistry", src)) / n, 3),
        "memory_refs": round(len(re.findall(r"checkpoint|continuity|replay|snapshot|temporal", src, re.I)) / n, 3),
        "heuristic_refs": round(len(re.findall(r"re\.(findall|search)", src)) / n, 3),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    runtime = scan("runtime")
    memory = scan("memory")
    repo = scan("repository")
    docs = scan("documents")
    query = scan("query")
    integrations = scan("integrations")

    artifacts = {
        "runtime_execution_depth": runtime,
        "semantic_runtime_coverage": runtime,
        "repository_execution_grounding": repo,
        "document_discourse_grounding": docs,
        "semantic_memory_depth": memory,
        "runtime_scheduler_depth": runtime,
        "semantic_state_transition_depth": runtime,
        "semantic_continuity_depth": memory,
        "runtime_orchestration_depth": runtime,
        "runtime_evidence_density": {"runtime": runtime.get("parser_refs", 0), "repository": repo.get("parser_refs", 0)},
        "heuristic_runtime_residue": {"repository": repo.get("heuristic_refs", 0), "documents": docs.get("heuristic_refs", 0)},
        "parser_runtime_grounding": {"parsers": scan("parsers"), "repository": repo},
        "semantic_runtime_validation": {"benchmarks": (ROOT / "benchmarks" / "benchmark_results.json").exists()},
        "runtime_reasoning_coverage": scan("reasoning"),
        "semantic_query_depth": query,
        "semantic_execution_gaps": {
            "runtime_files": runtime.get("files", 0),
            "memory_files": memory.get("files", 0),
            "target_runtime_modules": 10,
        },
    }
    for name, data in artifacts.items():
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    summary = {"domains": {"runtime": runtime, "memory": memory, "repository": repo, "documents": docs}}
    (OUT / "audit_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
