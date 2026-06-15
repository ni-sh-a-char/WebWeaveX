#!/usr/bin/env python3
"""Java-branch structural audit.

Classifies every git-tracked file into exactly one of six categories required by
the Java-branch cleanup mission, and assigns a cleanup disposition:

  Categories:
    required_java        - needed for the Maven build / Java parity governance
    shared_governance    - language-neutral repo governance (keep on every branch)
    legacy_dart          - Dart-ecosystem artifact (belongs on the `dart` branch)
    legacy_js            - JavaScript-ecosystem artifact (belongs on `javascript`)
    legacy_python        - Python/multi-language artifact (belongs on `python`)
    unknown              - could not be classified by rule

  Dispositions:
    keep      - stays on the Java branch as-is
    rewrite   - stays but must be rewritten Java-native (README only)
    relocate  - move under docs/archive/ (archival value, not Java-native)
    remove    - delete from the Java branch (preserved in git history + sibling branch)

Run from repo root:  python tools/audit_java_branch.py
Writes JAVA_BRANCH_AUDIT.json. Deterministic: no timestamps, sorted output.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- exact-path rules (highest priority) -----------------------------------
REQUIRED_JAVA_TOOLS = {
    "tools/gen_java_parity_matrix.py",
    "tools/gen_java_parity_vectors.py",
    "tools/gen_java_parity_vectors_s2.py",
    "tools/gen_java_parity_vectors_s3.py",
    "tools/validate_java_manifest.py",
    "tools/generate_parity_manifest.py",
    "tools/audit_java_branch.py",
}
REQUIRED_JAVA_WORKFLOWS = {
    ".github/workflows/java-build.yml",
    ".github/workflows/java-parity.yml",
    ".github/workflows/parity-regression.yml",
}
REQUIRED_JAVA_ROOT = {"PARITY_MANIFEST.json"}

SHARED_GOV_ROOT = {
    "LICENSE", "NOTICE", "AUTHORS", "CITATION.cff", ".gitignore",
    "CODE_OF_CONDUCT.md", "CONTRIBUTING.md", "GOVERNANCE.md", "MAINTAINERS.md",
    "CODEOWNERS", "SECURITY.md", "SUPPORT.md", "ROADMAP.md", "CHANGELOG.md",
    "RELEASE.md", "ARCHITECTURE.md", "API_REFERENCE.md", "AI_AGENT_GUIDE.md",
}
SHARED_GOV_GITHUB = {
    ".github/CODE_OF_CONDUCT.md", ".github/FUNDING.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/performance_issue.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
}

# Dart-specific build/config/release at repo root.
LEGACY_DART_ROOT = {
    "pubspec.yaml", ".pubignore", "analysis_options.yaml",
    "PUB_RELEASE_CHECKLIST.md", "CERTIFICATION.md",
}
LEGACY_JS_ROOT = {"NPM_RELEASE_CHECKLIST.md"}
LEGACY_PY_ROOT = {"PYPI_RELEASE_CHECKLIST.md"}

# Multi-language Python tooling inherited from the Dart/cert era — not used by the
# Java build or Java parity governance (those use the gen_java_* + validate_java_*
# scripts only, which import the canonical Python `core` package directly).
LEGACY_PY_TOOLS = {
    "tools/complete_proof_audit.py", "tools/cov_breakdown.py",
    "tools/dart_parity_audit.py", "tools/gen_api_reference.py",
    "tools/gen_executable_matrix.py", "tools/gen_proof_matrix.py",
    "tools/gen_semantic_ir_map.py", "tools/gen_semantic_ir_phaseplan.py",
    "tools/generate_reports.py", "tools/proof_coverage.py",
    "tools/three_way_parity.py",
}


def classify(path: str):
    """Return (category, disposition, ecosystem, rationale)."""
    p = path.replace("\\", "/")
    base = os.path.basename(p)
    ext = os.path.splitext(base)[1].lower()

    # 1. Required for the Java build / governance.
    if p.startswith("java/"):
        return ("required_java", "keep", "java",
                "Maven project source/tests/resources/reports")
    if p in REQUIRED_JAVA_TOOLS:
        return ("required_java", "keep", "java",
                "Java parity-vector generator / manifest validator")
    if p in REQUIRED_JAVA_WORKFLOWS:
        return ("required_java", "keep", "java", "Java CI workflow")
    if p in REQUIRED_JAVA_ROOT:
        return ("required_java", "keep", "shared",
                "single source of truth for cross-language API parity")

    # 2. Shared, language-neutral governance.
    if p in SHARED_GOV_ROOT or p in SHARED_GOV_GITHUB:
        if base == "README.md":
            return ("shared_governance", "rewrite", "shared", "root README")
        return ("shared_governance", "keep", "shared",
                "language-neutral repository governance / reference doc")
    if base == "README.md" and p == "README.md":
        return ("shared_governance", "rewrite", "shared",
                "root README — must become Java-native")

    # 3. Language-specific release checklists / CI at root.
    if p in LEGACY_DART_ROOT:
        return ("legacy_dart", "relocate", "dart",
                "Dart build/config/release/certification artifact")
    if p in LEGACY_JS_ROOT:
        return ("legacy_js", "relocate", "javascript", "npm release checklist")
    if p in LEGACY_PY_ROOT:
        return ("legacy_python", "relocate", "python", "PyPI release checklist")
    if p == ".github/workflows/dart.yml":
        return ("legacy_dart", "remove", "dart", "Dart CI workflow (runs on `dart` branch)")
    if p == ".github/workflows/ci.yml":
        return ("legacy_python", "remove", "python",
                "Python CI (pytest/wheel, runs on `python` branch)")

    # 4. Dart source tree, tests, examples.
    if p.startswith("lib/"):
        return ("legacy_dart", "remove", "dart", "Dart library source (lives on `dart` branch)")
    if p.startswith("test/"):
        return ("legacy_dart", "remove", "dart", "Dart test suite (lives on `dart` branch)")
    if p.startswith("example/"):
        return ("legacy_dart", "remove", "dart", "Dart example program")

    # 5. Multi-language parity / certification harness trees.
    if p.startswith(("validation/", "cross_language_verifier/")):
        if ext == ".dart":
            return ("legacy_dart", "remove", "dart", "Dart parity/cert harness")
        if ext in (".mjs", ".js"):
            return ("legacy_js", "remove", "javascript", "JS parity/cert harness")
        if ext == ".py":
            return ("legacy_python", "remove", "python", "Python parity/cert harness")
        # json / md / enc data outputs of the multi-language cert effort
        return ("legacy_python", "remove", "multi-language",
                "multi-language certification artifact (not consumed by Java)")

    # 6. Tooling.
    if p in LEGACY_PY_TOOLS:
        return ("legacy_python", "remove", "python",
                "Dart/cert-era Python tooling (not used by Java build/governance)")

    # 7. docs tree — cross-language reference documentation.
    if p.startswith("docs/"):
        return ("shared_governance", "keep", "shared",
                "cross-language reference / architecture documentation")

    # 8. Remaining root data files by extension.
    if ext == ".dart":
        return ("legacy_dart", "remove", "dart", "stray Dart file")
    if ext in (".mjs", ".js"):
        return ("legacy_js", "remove", "javascript", "stray JS file")
    if ext == ".json":
        return ("legacy_python", "remove", "multi-language",
                "root multi-language release/validation report (Dart/cert era)")

    return ("unknown", "review", "unknown", "unclassified — manual review required")


def main() -> None:
    files = subprocess.check_output(
        ["git", "ls-files"], cwd=ROOT, text=True
    ).splitlines()
    files = sorted(f for f in files if f.strip())

    entries = []
    for f in files:
        cat, disp, eco, why = classify(f)
        entries.append({
            "path": f, "category": cat, "disposition": disp,
            "ecosystem": eco, "rationale": why,
        })

    by_cat: dict[str, int] = {}
    by_disp: dict[str, int] = {}
    for e in entries:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + 1
        by_disp[e["disposition"]] = by_disp.get(e["disposition"], 0) + 1

    out = {
        "schema": "java-branch-audit/v1",
        "total_files": len(entries),
        "categories": dict(sorted(by_cat.items())),
        "dispositions": dict(sorted(by_disp.items())),
        "category_definitions": {
            "required_java": "needed for the Maven build or Java parity governance",
            "shared_governance": "language-neutral repo governance / reference docs",
            "legacy_dart": "Dart-ecosystem artifact (belongs on the `dart` branch)",
            "legacy_js": "JavaScript-ecosystem artifact (belongs on `javascript`)",
            "legacy_python": "Python / multi-language artifact (belongs on `python`)",
            "unknown": "could not be classified by rule",
        },
        "disposition_definitions": {
            "keep": "stays on the Java branch as-is",
            "rewrite": "stays but rewritten Java-native (README)",
            "relocate": "moved under docs/archive/ (archival value)",
            "remove": "deleted from the Java branch (preserved in git history + sibling branch)",
            "review": "manual review required",
        },
        "files": entries,
    }
    path = os.path.join(ROOT, "JAVA_BRANCH_AUDIT.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"audited {len(entries)} files -> JAVA_BRANCH_AUDIT.json")
    print("by category:", json.dumps(out["categories"]))
    print("by disposition:", json.dumps(out["dispositions"]))
    unknown = [e["path"] for e in entries if e["category"] == "unknown"]
    if unknown:
        print("UNKNOWN (review):")
        for u in unknown:
            print("  -", u)


if __name__ == "__main__":
    main()
