# FINAL ZERO-TRUST CERTIFICATION

Date: 2026-06-12 · All claims below are recomputed from executed code in this
certification run. No prior report, README, or generated artifact was trusted.
Harness: `cross_language_verifier/` (every script, vector, and report committed
or regenerable from committed generators).

## Repository version

| Branch | Commit | Package version |
| --- | --- | --- |
| dart (this branch) | see HEAD of this commit | webweavex 2.0.1 (pub) |
| python | d4c5800 | webweavex 2.0.1 (pyproject) |
| javascript | 3bad923 | webweavex 2.0.1 (npm) |

Dependency under mandate: **kaalka 5.0.0** — PyPI, npm, pub.dev (published packages, no fork).

## Executed evidence

| Phase | Scope | Result |
| --- | --- | --- |
| 1–2 Inventory/API parity | recomputed from source (AST/exports), not from reports | Python public surface = 128 APIs (manifest count independently confirmed); all 126 non-version APIs present in JS; **22 absent in Dart** (= 14 Partial + 8 Deferred, exactly as PARITY_MANIFEST claims; zero bookkeeping disagreement) — `api_parity_matrix.json` |
| 3–4, 15 Function/implementation/cross-product | 201 vectors × 20 files, executed live per language | Python live **201/201**, JavaScript live **201/201**, Dart asserts identical hashes via 1288-test suite — `function_parity_matrix.json`, `cross_product_matrix.json` |
| 5 Real execution harness | no mocks; all results from live runs | `cross_language_verifier/` runners + comparators |
| 6 Kaalka | embedded byte bridges vs PUBLISHED packages | PyPI **1400/1400**, npm **1400/1400**, pub.dev **30/30** designed vectors + `_proc` source identity; 0 mismatches — `kaalka_certification_report.json` |
| 7–9 Serialization/Hash/Unicode | **10,000 vectors** (Latin, Hindi, Arabic, Chinese, Japanese, Korean, Thai, Hebrew, emoji+ZWJ/ZWNJ, astral, combining, bidi, zero-width, controls; float matrix; key ordering; nested; 9k seeded structures) × 6 fields × 3 languages × 3 runs | **60,001/60,001 byte-identical**, all roundtrips pass, per-language determinism 3/3 — `parity_report.json`, `certification_report.json` |
| 10 Extraction engines | 14 malformed/torture cases + identical bytes | Python==JavaScript **14/14** — `extraction_certification.json` |
| 11 Real internet | **130 pages fetched once** (12 wiki languages incl. RTL/CJK/Indic/Thai, MDN, GitHub, W3C, RFC, news, docs) | Python==JavaScript **130/130 byte-identical**; **Dart: FAIL-BY-ABSENCE** — `real_world_parity_report.json` |
| 12 Semantic IR | 405 fixtures, single hashing authority | three-way **405/405** — `semantic_ir_certification.json` |
| 13 Performance | identical workload, same host | within ~4× band (JS fastest); no pathology — `performance_report.json` |
| 14 OSS readiness | dry-runs executed | pub: 0 warnings/1 hint; npm: builds clean but **publishes empty without `npm run build` (no prepublishOnly guard)**; PyPI metadata present — `oss_readiness_report.json` |

Test suites (executed this run): Dart **1288/1288** · JavaScript vitest **399/399 (238 files)** · Python targeted **82 pass** (13 Kaalka cross-language + 69 serializer/normalization; full Python suite requires browser dependencies).

## Mismatches found by this certification — all root-caused and fixed

1. **JS `callKw` wrong parameter-order lists** (`buildRuntimeTimeline`, `trackRuntimeMutations`) — every keyword argument silently dropped; timelines always empty. Fixed with direct calls. (10 vectors recovered.)
2. **PySoup `find_all(true)`** matched tags literally named "true" instead of all tags — semantic anchors never found. Fixed.
3. **U+FEFF trailing-strip divergence** — ECMAScript `\s` includes U+FEFF, Python's does not; JS+Dart normalization stripped it. Fixed with explicit Python whitespace class in both.
4. **Dart `utf8.decode` BOM strip** — decrypt round-trips lost a leading U+FEFF (36/10,000 vectors); Python/Node preserve it. Fixed via `utf8DecodeParity` in 4 call sites.
5. **JS HTML entity table mojibake-corrupted and incomplete** (16 names, `ldquo`/`rdquo` double-encoded) — replaced with full 2125-entry HTML5 table generated from Python `html.entities.html5`.
6. **PySoup tokenizer divergences from html.parser/bs4** (5 distinct bugs): whitespace-only node collapse (ASCII-spaces rule), literal `<` as data + buffer coalescing, unquoted-attribute trailing slash, whole-document `toLowerCase()` index shift (U+0130), `>` inside quoted attribute values.
7. **PySoup `get_text` over-inclusion** — bs4 excludes `template`/`rt`/`rp` strings (exact-type filter); JS included them (furigana, React templates leaked into text).
8. **JS strip family used ECMAScript whitespace** — `strip`/`lstrip`/`rstrip`/`get_text(strip)` now use Python semantics.
9. **Semantic-IR JS runner's hash shim** emulated the pre-contract float behavior — superseded by single-hashing-authority comparison (no engine bug).

After fixes, every executed comparison above is green. All fixes carry regression coverage via the committed verifier vectors + suites.

## Remaining issues (documented blockers — not closable in this run)

1. **Dart has no HTML extraction engine.** 22 of Python's 128 public APIs (extraction/crawl/cognition family: 14 Partial + 8 Deferred per manifest) are unimplemented or unexported in Dart. Phases 10–11 are therefore **FAIL for Dart**. Closing this requires porting the bs4-equivalent subsystem and the ~3,611-line semantic-IR recompute engine (multi-session work already planned in `SEMANTIC_IR_PHASE_PLAN.md`).
2. **npm publish footgun**: `files: ["dist", ...]` with no `prepublishOnly` build guard — a raw `npm publish` ships an empty package.
3. Python full test suite not executed (needs Playwright/browser deps); core serializer/crypto/parity subsets pass.
4. Performance phase is informative micro-benchmarking only (no memory/throughput SLA defined to certify against).

## VERDICT

```
Python == JavaScript : PASS  (every implemented capability tested, incl. real-internet extraction)
Python == Dart       : PASS  (every capability implemented in Dart: deterministic core, Kaalka,
                              serialization, unicode, hashing, semantic IR, API vector corpus)
Dart extraction      : FAIL-BY-ABSENCE (not implemented — documented blocker above)

FINAL: FAIL — NOT CERTIFIED as "Dart = Python = JavaScript for every implemented
capability", because the extraction-engine capability implemented in Python and
JavaScript has no Dart implementation. Every capability that EXISTS in all three
languages is byte-identical under 70,000+ executed comparisons with zero
unresolved mismatches.
```

Root cause of FAIL: absence, not divergence. The path to PASS is the planned
Dart extraction + semantic-IR port; no other open parity defect remains.

---

## ADDENDUM — Extraction-gap closure run (commits: dart 6419e58, javascript fb09003)

The blocker above is now substantially closed with executed evidence
(`cross_language_verifier/extraction_certification.json`,
`dart_extraction_gap_report.json`):

```
Extraction engines   : PASS 3-WAY — Python == JavaScript == Dart byte-identical on
                       10,000 synthetic HTML torture documents (10000/10000),
                       14 malformed-HTML cases (14/14), and
                       1,006 real internet pages fetched once (1006/1006).
```

- Dart gained a bs4-parity soup engine (`lib/src/soup/`) certified at
  html.parser-internals depth (including the two-pass failed-`&#` raw-dump
  buffering behavior, parse-time string-container typing, cp1252
  invalid-charref mapping, semicolonless entity resolution).
- Both JS and Dart parsers were upgraded to full Python `html.unescape` +
  bs4 text-tokenization semantics; JS re-certified (vitest 399/399), Dart
  re-certified (1288/1288), prior 130-page certification re-run green.
- 6 missing extraction APIs implemented and hash-verified vs live Python:
  `extract_semantic_html`, `extract_semantic_content`, `ingest_input`,
  `extract_multimodal`, `extract_paginated_content`, `recover_modal_runtime`.
- Remaining Dart API gap: 13 portable APIs (the `extract`/`universal_extract`/
  `stream_extract` orchestrator family and 7 smaller engines — porting was
  interrupted by an external session-usage limit that terminated 5 of 6
  parallel port agents; their partial output was quarantined per the
  no-partial-ports rule) and 6 platform-bound APIs (live browser / OS-coupled,
  unportable by design). Per-API module lists, signatures, sizes, and blocking
  statuses: `dart_extraction_gap_report.json`.

Updated verdict: unchanged in kind (FAIL-BY-ABSENCE for the remaining 13
portable APIs), but the extraction ENGINE capability — the core of
"Extract Anything" — is now certified byte-identical in all three languages
at 11,020 executed extraction comparisons with zero unresolved mismatches.
