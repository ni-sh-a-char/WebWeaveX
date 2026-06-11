"""Phases 1-2: per-branch inventory + OSS audit with mandatory
classification. No deletions here — classification only.

Usage: python validation/release/build_inventory.py <branch> <out_prefix>
"""
import fnmatch
import json
import subprocess
import sys
from collections import Counter

BRANCH = sys.argv[1]
OUT = sys.argv[2]

# (pattern, classification, purpose) — first match wins. Audited per branch.
RULES = [
    # --- runtime source ---
    ("lib/**", "REQUIRED_RUNTIME", "dart library source"),
    ("src/**", "REQUIRED_RUNTIME", "typescript library source"),
    ("core/**", "REQUIRED_RUNTIME", "python core engine source"),
    ("webweavex/**", "REQUIRED_RUNTIME", "python public package"),
    ("bin/**", "REQUIRED_RUNTIME", "executables"),
    # --- build ---
    ("pubspec.yaml", "REQUIRED_BUILD", "dart package manifest"),
    ("pubspec.lock", "REQUIRED_BUILD", "dart lockfile"),
    ("analysis_options.yaml", "REQUIRED_BUILD", "dart analyzer config"),
    ("package.json", "REQUIRED_BUILD", "npm manifest"),
    ("package-lock.json", "REQUIRED_BUILD", "npm lockfile"),
    ("tsconfig*.json", "REQUIRED_BUILD", "typescript config"),
    ("eslint.config.js", "REQUIRED_BUILD", "lint config"),
    ("vitest.config.*", "REQUIRED_BUILD", "test runner config"),
    ("pyproject.toml", "REQUIRED_BUILD", "python build config"),
    ("setup.py", "REQUIRED_BUILD", "python build"),
    ("setup.cfg", "REQUIRED_BUILD", "python build"),
    ("MANIFEST.in", "REQUIRED_BUILD", "python sdist manifest"),
    ("requirements*.txt", "REQUIRED_BUILD", "python deps"),
    (".pubignore", "REQUIRED_BUILD", "pub package excludes"),
    (".npmignore", "REQUIRED_BUILD", "npm package excludes"),
    (".gitignore", "REQUIRED_BUILD", "vcs excludes"),
    (".gitattributes", "REQUIRED_BUILD", "vcs attributes"),
    (".github/**", "REQUIRED_BUILD", "CI workflows"),
    # --- testing ---
    ("test/**", "REQUIRED_TESTING", "test suite"),
    ("tests/**", "REQUIRED_TESTING", "test suite"),
    ("conftest.py", "REQUIRED_TESTING", "pytest config"),
    # --- certification harnesses (reproducibility) ---
    ("validation/parity/**", "REQUIRED_CERTIFICATION",
     "executed-Python parity vectors consumed by the test suite"),
    ("validation/semantic_ir/run_*.py", "REQUIRED_CERTIFICATION",
     "3-way harness runner"),
    ("validation/semantic_ir/run_*.mjs", "REQUIRED_CERTIFICATION",
     "3-way harness runner"),
    ("validation/semantic_ir/run_*.dart", "REQUIRED_CERTIFICATION",
     "3-way harness runner"),
    ("validation/semantic_ir/compare_results.py", "REQUIRED_CERTIFICATION",
     "3-way comparator"),
    ("validation/semantic_ir/fixtures.json", "REQUIRED_CERTIFICATION",
     "certified fixture set (667)"),
    ("validation/semantic_ir/gen_*.py", "REQUIRED_CERTIFICATION",
     "fixture provenance generators"),
    ("validation/semantic_ir/*_results.json", "GENERATED",
     "harness outputs — regenerated on every run"),
    ("validation/executable/*_results.json", "GENERATED",
     "harness outputs — regenerated on every run"),
    ("validation/executable/**", "REQUIRED_CERTIFICATION",
     "executable API harness"),
    ("validation/zero_trust_v2/mv_*.json", "GENERATED",
     "million-vector outputs — regenerated"),
    ("validation/zero_trust_v2/*.py", "REQUIRED_CERTIFICATION",
     "certification writers/runners"),
    ("validation/zero_trust_v2/mv_*.mjs", "REQUIRED_CERTIFICATION",
     "million-vector runner"),
    ("validation/zero_trust_v2/mv_*.dart", "REQUIRED_CERTIFICATION",
     "million-vector runner"),
    ("validation/zero_trust_v2/*.json", "REQUIRED_CERTIFICATION",
     "certification artifacts with repro commands"),
    ("final_certification.json", "REQUIRED_CERTIFICATION",
     "final verdict artifact"),
    ("FINAL_ZERO_TRUST_CERTIFICATION_V2.json", "LEGACY",
     "superseded by final_certification.json (historical FAIL evidence)"),
    ("PARITY_MANIFEST.json", "REQUIRED_CERTIFICATION",
     "single source of truth for API classification"),
    ("cross_language_verifier/corpus/**", "REQUIRED_CERTIFICATION",
     "1006-page real corpus (large; release branches keep manifest + "
     "fetch_corpus.py, drop pages — refetchable)"),
    ("cross_language_verifier/out_*.json", "GENERATED",
     "verifier run outputs"),
    ("cross_language_verifier/*_out.json", "GENERATED",
     "verifier run outputs"),
    ("cross_language_verifier/synth_*.json", "GENERATED",
     "synth outputs/inputs — regenerated from seeded generator"),
    ("cross_language_verifier/vectors.json", "GENERATED",
     "seeded generator output"),
    ("cross_language_verifier/bench_*_out.json", "GENERATED",
     "benchmark outputs"),
    ("cross_language_verifier/*.py", "REQUIRED_CERTIFICATION",
     "verifier harness"),
    ("cross_language_verifier/*.mjs", "REQUIRED_CERTIFICATION",
     "verifier harness"),
    ("cross_language_verifier/*.dart", "REQUIRED_CERTIFICATION",
     "verifier harness"),
    ("cross_language_verifier/*.json", "REQUIRED_CERTIFICATION",
     "verifier certification artifacts"),
    ("cross_language_verifier/README.md", "REQUIRED_DOCUMENTATION",
     "verifier protocol"),
    ("cross_language_verifier/*.txt", "TEMPORARY", "spot-check leftovers"),
    ("tools/**", "REQUIRED_CERTIFICATION",
     "matrix/manifest/report generators (reproducibility)"),
    # --- documentation ---
    ("README.md", "REQUIRED_DOCUMENTATION", "front page"),
    ("LICENSE", "REQUIRED_DOCUMENTATION", "license"),
    ("CHANGELOG.md", "REQUIRED_DOCUMENTATION", "changelog"),
    ("CONTRIBUTING.md", "REQUIRED_CONTRIBUTOR", "contributor guide"),
    ("CODE_OF_CONDUCT.md", "REQUIRED_CONTRIBUTOR", "conduct"),
    ("GOVERNANCE.md", "REQUIRED_CONTRIBUTOR", "governance"),
    ("MAINTAINERS.md", "REQUIRED_CONTRIBUTOR", "maintainers"),
    ("CODEOWNERS", "REQUIRED_CONTRIBUTOR", "code owners"),
    ("SECURITY.md", "REQUIRED_CONTRIBUTOR", "security policy"),
    ("SUPPORT.md", "REQUIRED_CONTRIBUTOR", "support policy"),
    ("RELEASE.md", "REQUIRED_CONTRIBUTOR", "release process"),
    ("AUTHORS", "REQUIRED_CONTRIBUTOR", "authors"),
    ("NOTICE", "REQUIRED_DOCUMENTATION", "notices"),
    ("CITATION.cff", "REQUIRED_DOCUMENTATION", "citation"),
    ("AI_AGENT_GUIDE.md", "REQUIRED_AGENT", "agent onboarding"),
    ("API_REFERENCE.md", "REQUIRED_DOCUMENTATION", "api reference"),
    ("ARCHITECTURE.md", "REQUIRED_DOCUMENTATION", "architecture"),
    ("CERTIFICATION.md", "REQUIRED_DOCUMENTATION", "certification guide"),
    ("ROADMAP.md", "REQUIRED_DOCUMENTATION", "roadmap"),
    ("docs/**", "REQUIRED_DOCUMENTATION", "extended docs"),
    ("example/**", "REQUIRED_EXAMPLE", "dart examples"),
    ("examples/**", "REQUIRED_EXAMPLE", "examples"),
    # --- dev-era reports (superseded by consolidated CERTIFICATION.md) ---
    ("PUBLIC_API_MATRIX.md", "GENERATED",
     "regenerated by tools/dart_parity_audit.py"),
    ("*_REPORT.md", "LEGACY", "dev-era report, superseded"),
    ("*_AUDIT.md", "LEGACY", "dev-era audit, superseded"),
    ("*_MATRIX.md", "LEGACY", "dev-era matrix, superseded"),
    ("FINAL_*.md", "LEGACY", "dev-era report, superseded"),
    ("SEMANTIC_IR_*.md", "LEGACY",
     "dev-era living progress docs, superseded by CERTIFICATION.md"),
    ("WEBWEAVEX_*.md", "LEGACY", "dev-era report"),
    ("PYTHON_RELEASE_READINESS_REPORT.md", "LEGACY", "dev-era report"),
    ("REPOSITORY_AUDIT.md", "LEGACY", "dev-era report"),
    ("coverage/**", "GENERATED", "coverage output"),
    (".vscode/**", "TEMPORARY", "editor config"),
    # --- refined after UNKNOWN investigation ---
    ("validation/**", "REQUIRED_CERTIFICATION",
     "family validators + executed-Python vectors (referenced by tests/CI)"),
    ("benchmarks/**", "REQUIRED_CERTIFICATION",
     "benchmark corpora + runners (performance reproducibility)"),
    ("specification/**", "REQUIRED_CERTIFICATION",
     "canonical cross-language vector specification"),
    ("contracts/**", "REQUIRED_RUNTIME", "contract schemas"),
    (".editorconfig", "REQUIRED_BUILD", "editor config"),
    (".prettierrc", "REQUIRED_BUILD", "format config"),
    ("tsup.config.ts", "REQUIRED_BUILD", "bundler config"),
    ("LANGUAGES.md", "LEGACY", "dev-era doc, superseded"),
    ("REPOSITORY_STATE_BEFORE_MIGRATION.md", "LEGACY", "dev-era snapshot"),
    ("TEST_INVENTORY.md", "LEGACY", "dev-era doc, superseded"),
    ("extractors/**", "LEGACY",
     "orphan package — zero references outside itself (verified by grep); "
     "superseded by core.extract facades"),
    ("scripts/**", "LEGACY",
     "dev-era one-shot audit/purification scripts, unreferenced by runtime"),
    ("ports/**", "REQUIRED_DOCUMENTATION", "porting spec"),
    ("specs/**", "REQUIRED_DOCUMENTATION", "subsystem specs"),
]



def classify(path):
    for pat, cls, why in RULES:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path.split('/')[-1],
                                                         pat):
            return cls, why
    return "UNKNOWN", "no rule matched — investigate"


files = subprocess.check_output(
    ['git', 'ls-tree', '-r', '-l', BRANCH], text=True).splitlines()
inv = []
for line in files:
    meta, path = line.split('\t', 1)
    size = int(meta.split()[3])
    cls, why = classify(path)
    inv.append({"path": path, "size": size, "classification": cls,
                "purpose": why})

counts = Counter(e["classification"] for e in inv)
total = sum(e["size"] for e in inv)
json.dump({"branch": BRANCH, "files": len(inv), "bytes": total,
           "classification_counts": dict(counts), "entries": inv},
          open(f"{OUT}_inventory.json", "w"), indent=1)

audit = {
    "branch": BRANCH,
    "unknown": [e["path"] for e in inv if e["classification"] == "UNKNOWN"],
    "legacy": [e["path"] for e in inv if e["classification"] == "LEGACY"],
    "generated": [e["path"] for e in inv
                  if e["classification"] == "GENERATED"],
    "temporary": [e["path"] for e in inv
                  if e["classification"] == "TEMPORARY"],
    "largest": sorted(inv, key=lambda e: -e["size"])[:15],
}
json.dump(audit, open(f"{OUT}_oss_audit.json", "w"), indent=1)
print(f"{BRANCH}: {len(inv)} files, {total/1e6:.1f} MB,",
      dict(counts))
print("UNKNOWN:", audit["unknown"][:10])
