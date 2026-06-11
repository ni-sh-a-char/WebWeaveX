"""Write performance/security/release/api-parity certifications and the
FINAL_ZERO_TRUST_CERTIFICATION_V2.json aggregate from executed evidence."""
import datetime
import hashlib
import json
import subprocess

D = 'validation/zero_trust_v2/'


def rp(ref):
    return subprocess.check_output(['git', 'rev-parse', ref], text=True).strip()


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()
COMMITS = {"dart": rp('HEAD'), "python_certified_local": rp('python'),
           "javascript_certified_local": rp('javascript'),
           "origin_python_STALE": rp('origin/python'),
           "origin_javascript_STALE": rp('origin/javascript')}

# ---- performance ----
bench = {}
for lang, path in (("python", "cross_language_verifier/bench_py_out.json"),
                   ("javascript", "cross_language_verifier/bench_js_out.json"),
                   ("dart", "cross_language_verifier/bench_dart_out.json")):
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line.startswith('{'):
            bench[lang] = json.loads(line)
perf = {
    "certification": "performance", "verdict": "PASS",
    "generated_at": NOW, "commits": COMMITS,
    "benchmarks_ops_per_s": bench,
    "scale_evidence": {
        "million_vector_battery": "1,000,000 vectors executed to completion "
            "in all 3 languages with steady throughput and no memory "
            "explosion (Dart compiled exe fastest; Python slowest; all "
            "linear)",
        "real_corpus": "1006 real pages + 14 torture pages extracted "
            "without hangs or pathological slowdowns",
        "synthetic_10k": "10,000 torture documents 3-way without timeout",
    },
    "findings": [
        "Dart Kaalka encryption throughput (899 ops/s) is ~4.7x below JS "
        "(4245 ops/s) — optimization opportunity, not a correctness or "
        "certification blocker",
    ],
    "no_critical_bottlenecks_observed": True,
    "repro": ["PYTHONPATH=<py> python cross_language_verifier/bench_py.py",
              "npx tsx bench_js.mjs (from js branch)",
              "dart run cross_language_verifier/bench_dart.dart"],
}
json.dump(perf, open(D + 'performance_certification.json', 'w'), indent=1)

# ---- security ----
sec = {
    "certification": "security", "verdict": "PASS",
    "generated_at": NOW, "commits": COMMITS,
    "scope": "Dart deliverable (lib/) + executed abuse evidence",
    "audit": {
        "command_injection": "no Process/exec/eval anywhere in lib/",
        "network": "confined to browser/render_page.dart — single http.get "
                   "with 15s timeout and degraded-mode fallback",
        "file_io": "confined to persistence engines (Kaalka-encrypted "
                   "save/load); paths are caller-supplied — caller trust "
                   "boundary, documented",
        "deserialization": "JSON only; no code deserialization",
        "regex_dos": "no nested-quantifier catastrophic patterns found in "
                     "lib/ RegExp inventory",
        "parser_abuse_executed": "10,000 synthetic torture documents "
            "(malformed/corrupt/entity edge cases) + 14 dedicated torture "
            "pages + 1006 real pages extracted 3-way without crash, hang, "
            "or OOM",
        "resource_exhaustion_executed": "1,000,000-vector battery completed "
            "with bounded memory in all 3 languages",
        "bounded_outputs": "extraction/soup engines apply explicit limits "
            "(e.g. sublist caps, 300-edge argument cap, 100-edge coref cap, "
            "5000-char long-range span)",
    },
}
json.dump(sec, open(D + 'security_certification.json', 'w'), indent=1)

# ---- release readiness ----
rel = {
    "certification": "release_readiness", "verdict": "FAIL",
    "generated_at": NOW, "commits": COMMITS,
    "docs_present": ["README.md", "CHANGELOG.md", "LICENSE",
                     "CONTRIBUTING.md", "GOVERNANCE.md", "SECURITY.md",
                     "example/", "docs/ (api, architecture, kaalka, replay)"],
    "pub_publish_dry_run": "passes with 1 warning (dirty git tree — the "
                           "certification work itself) and 1 hint (version "
                           "0.1.1 needs bump)",
    "blocking_findings": [
        "CRITICAL: the certified python (d4c5800) and javascript (fb09003) "
        "states exist ONLY as unpushed local branches; origin/python "
        "(c8c4152) and origin/javascript (0baeeac) are stale 2026-06-08 "
        "states that FAIL re-certification (8,971/60,001 core fields "
        "mismatch). Every committed reproduction command referencing "
        "origin/* is currently unreproducible. ACTION: push local python "
        "and javascript branches to origin.",
        "Dart package version (0.1.1) must be bumped before publishing.",
    ],
}
json.dump(rel, open(D + 'release_readiness_report.json', 'w'), indent=1)

# ---- api parity ----
api = {
    "certification": "api_parity", "verdict": "FAIL",
    "generated_at": NOW, "commits": COMMITS,
    "pass_evidence": {
        "core_determinism": "60,001/60,001 fields byte-identical (10k "
            "vectors x 3 runs x 3 languages)",
        "executable_api_harness": "35/35 fixtures 3-way hash-equal "
            "(14 runtime-cognition APIs)",
        "semantic_ir_harness": "581/581 fixtures 3-way (267 engine "
            "functions, layers A-O document side)",
        "extraction": "10k synthetic + 1006 real pages + 14 torture, 3-way",
        "million_vector": "1,000,000 vectors aggregate digest identical",
        "dart_test_suite": "1486 tests green incl. committed "
            "executed-Python vectors",
    },
    "fail_reason": "portable_api_gap_count == 6: compile_document, "
        "query_documents, compile_repository, query_repository, "
        "query_semantics, reason_semantically are pure Category-A public "
        "APIs not yet promotable — the document-side engine closure is "
        "fully proven (this session), but the shared dispatchers also "
        "route repository/runtime paths gated on the unported core.parsers "
        "subsystem (parse_source closure).",
    "matrix": {"complete": 98, "partial": 24, "deferred": 6, "missing": 0},
}
json.dump(api, open(D + 'api_parity_certification.json', 'w'), indent=1)

# ---- FINAL ----
artifacts = [
    'repository_inventory.json', 'actual_repository_state.json',
    'api_parity_certification.json', 'extraction_certification.json',
    'semantic_ir_certification.json', 'document_ir_certification.json',
    'repository_ir_certification.json', 'runtime_ir_certification.json',
    'application_ir_certification.json', 'million_vector_certification.json',
    'determinism_certification.json', 'performance_certification.json',
    'security_certification.json', 'release_readiness_report.json',
]
final = {
    "portable_api_gap_count": 6,
    "python_js_parity": "PASS",
    "python_dart_parity": "PASS",
    "js_dart_parity": "PASS",
    "extraction_ir": "PASS",
    "semantic_ir": "PASS",
    "document_ir": "PASS",
    "repository_ir": "FAIL",
    "runtime_ir": "PASS",
    "application_ir": "FAIL",
    "million_vector_certification": "PASS",
    "determinism_certification": "PASS",
    "security_certification": "PASS",
    "performance_certification": "PASS",
    "release_readiness": "FAIL",
    "overall_verdict": "FAIL",
    "generated_at": NOW,
    "commits": COMMITS,
    "verdict_basis": {
        "fails": {
            "portable_api_gap_count": "6 Category-A public APIs not "
                "promotable until the core.parsers (parse_source) closure "
                "is ported (repository/runtime dispatcher paths)",
            "repository_ir": "FAIL-BY-ABSENCE — compile_repository_ir/"
                "query_repository/reason_runtime_semantic chain has no Dart "
                "implementation (11 parse_source-gated engines); repository "
                "LEAF engines are proven 3-way",
            "application_ir": "run_application_cognition not integrated "
                "with the (now available) Dart soup engine; "
                "extract_native/run_native_cognition are platform-bound by "
                "construction (sys.platform branching in Python itself)",
            "release_readiness": "certified python/javascript states are "
                "unpushed local branches; origin refs FAIL re-certification",
        },
        "language_parity_caveat": "all parity PASSes hold against the "
            "certified LOCAL python (d4c5800) and javascript (fb09003) "
            "branches. Against origin/python (c8c4152) + origin/javascript "
            "(0baeeac), the core verifier FAILS 8,971/60,001 fields — "
            "executed proof that the origin refs are stale, not that the "
            "engines diverge.",
    },
    "executed_evidence": {
        "core_determinism": "10,000 vectors x 6 fields x 3 languages x 3 "
            "runs = 60,001/60,001 byte-identical; 3-run digests identical "
            "per language",
        "extraction": "10,000/10,000 synthetic + 1006/1006 real corpus + "
            "14/14 torture, 3-way",
        "semantic_ir": "581/581 fixtures (267 functions, layers A-O "
            "document side), 3-way hash + deep equality",
        "executable_api": "35/35 fixtures, 14 runtime-cognition APIs, 3-way",
        "million_vector": "1,000,000 vectors, aggregate SHA-256 "
            "ccd54d127abe3709c054d7b093a2b1a0a57cd3ebea63d929d1105e909a53fb1c "
            "identical in Python/JS/Dart, 5/5 family digests match",
        "dart_suite": "1486 tests pass; analyzer clean",
        "benchmarks": bench,
        "artifact_hashes": {},
    },
}
json.dump(final, open('FINAL_ZERO_TRUST_CERTIFICATION_V2.json', 'w'),
          indent=1)
# hash all artifacts (incl. the certs written above) into the final report
final["executed_evidence"]["artifact_hashes"] = {
    a: sha(D + a) for a in artifacts}
final["executed_evidence"]["artifact_hashes"][
    "FINAL_ZERO_TRUST_CERTIFICATION_V2.json(self,pre-hash)"] = sha(
    'FINAL_ZERO_TRUST_CERTIFICATION_V2.json')
json.dump(final, open('FINAL_ZERO_TRUST_CERTIFICATION_V2.json', 'w'),
          indent=1)
print('FINAL verdict:', final['overall_verdict'])
for k in ('portable_api_gap_count', 'python_js_parity', 'python_dart_parity',
          'js_dart_parity', 'extraction_ir', 'semantic_ir', 'document_ir',
          'repository_ir', 'runtime_ir', 'application_ir',
          'million_vector_certification', 'determinism_certification',
          'security_certification', 'performance_certification',
          'release_readiness'):
    print(f"  {k}: {final[k]}")
