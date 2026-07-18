# Changelog

## [3.0.0] — 2026-06-12 — Synchronized cross-language release

### Changed
- Synchronized version **3.0.0** across pub.dev (Dart), PyPI (Python), and npm (JavaScript).
- Standardized README structure across all three implementations (equivalent sections:
  Core Capabilities, Common Workflows, Supported Platforms, Versioning) and reconciled
  internal test-count metrics with the certified suite (1583 tests).
- Consolidated release staging into the canonical `python` / `javascript` / `dart` branches and
  removed the `release/*` staging branches.
- Re-ran cross-language parity, determinism, and publication validation against this version.

### Notes
- **No public API behavior changes.** The cross-language deterministic contract and hashes are
  unchanged from 2.0.x; the crypto substrate pin (`kaalka 5.0.0`) is intentionally unchanged.
- Shared docs (`ARCHITECTURE.md`, `CERTIFICATION.md`, `AI_AGENT_GUIDE.md`, `API_REFERENCE.md`,
  `LICENSE`) are byte-identical across all three implementations.

## [Unreleased] — Cross-language canonical contract + standalone Dart

### Added

- `cross_language_verifier/` — automated 3-language parity harness: 1100
  deterministic torture vectors (multilingual Unicode, float matrix, key
  ordering, nested structures), 3 runs per language, byte-level comparison.
  Certified: **6601/6601 fields byte-identical** across Python, JavaScript,
  and Dart (`certification_report.json`, `kaalka_parity_matrix.json`).
- `lib/src/determinism/py_float_repr.dart` — Python `repr(float)` formatting
  (canonical float form shared by all languages).
- `lib/src/determinism/canonical_json_encode.dart` — compact canonical JSON
  encoder, byte-identical to Python `json.dumps(..., ensure_ascii=False,
  separators=(",", ":"), sort_keys=True)`.

### Changed (canonicalization contract — affects hashes of edge-case payloads)

- **Dart is now fully standalone**: `normalizeRuntimeValue` performs NFKC via
  pure-Dart `package:unorm_dart` (byte-verified against Python `unicodedata`
  and ICU); the previous silent `Process.runSync('node', ...)` delegation is
  removed. Output no longer depends on whether Node.js is installed.
- Dict keys sort by Unicode **code point** (Python `sorted` semantics) in all
  languages; Dart/JS previously used UTF-16 code-unit order, which inverted
  astral-plane keys (e.g. U+1F680) relative to U+E000–U+FFFF.
- **Integral floats `< 2^63` canonicalize to integers** in every language
  (JavaScript cannot distinguish `2.0` from `2`); non-finite floats serialize
  as `null` on the stable path and `0` on the fingerprint path; fractional
  floats use Python `repr` thresholds in all languages.
- `dumpsDeterministic` (fingerprint path) now applies real NFC normalization
  in Dart (was identity) and `.15g` rounding only to fractional values.

## [Unreleased] — Final Completion Protocol · Group D (cont.) + manifest-driven reports

### Added

- `tools/generate_reports.py` — generates API_PARITY_VALIDATION_REPORT, FINAL_TRUE_PARITY_REPORT,
  PARTIAL_API_AUDIT, DEFERRED_API_AUDIT from **PARITY_MANIFEST.json** and syncs count tokens in the
  legacy reports. No report carries hand-maintained counts (resolved prior count disagreements).
- `lib/src/application/runtime_application.dart` — `executeRuntimeObjective` (executable parity,
  Python ≡ JS ≡ Dart), `buildRuntimeGoal`, and the `saveApplicationMemory`/`loadApplicationMemory`
  + `saveNativeRuntime`/`loadNativeRuntime` Kaalka pairs (proven by save→load deep-equality roundtrip).

### Changed

- 5 APIs promoted Deferred → Complete (`execute_runtime_objective` + 4 application/native save/load
  pairs). API parity matrix: **94 Complete · 26 Partial · 8 Deferred · 0 Missing**; 857 tests;
  97.21% coverage. 14 executable-proven APIs. Deferred re-audit: 8 remain = 5 live-`page` browser
  (platform ceiling) + 3 large native/application cognition entry points (convertible, pending).


## [Unreleased] — Final Completion Protocol · Group D (Deferred re-audit)

### Changed

- Group D re-audit of the 15 Deferred APIs: only **5 are genuinely platform-bound** (live-browser
  `page`); the other 10 are snapshot/data/persistence-input deterministic functions.
- **`extractContainerRuntime`** and **`extractIdeRuntime`** ported to Python's full field set and
  proven **Python ≡ JavaScript ≡ Dart** by execution → Deferred → **Complete**.
- API parity matrix: **89 Complete · 26 Partial · 13 Deferred · 0 Missing**; 850 tests; 97.19% coverage.
  13 executable-proven APIs. See `DEFERRED_API_AUDIT.md`.


## [Unreleased] — Final Completion Protocol · Group C (build_browser_identity)

### Changed (BREAKING)

- **`buildBrowserIdentity(profileId)`** now matches the canonical Python contract — a full port
  of the `core.identity.*` profile-generation subsystem (profile / user-agent / platform /
  language / timezone / webgl / canvas / font / media-device / navigator engines + entropy +
  fingerprint + data tables). Proven **Python ≡ JavaScript ≡ Dart** by execution on 4 profiles
  → **Complete**. The captured-map variant is `buildBrowserIdentityFromCapture`.
- API parity matrix: **87 Complete · 26 Partial · 15 Deferred · 0 Missing**; 845 tests; 97.17% coverage.
  Group C done (11 executable-proven APIs).


## [Unreleased] — Final Completion Protocol · Group B complete (executable parity)

### Changed

- **`reconstructRuntime`** now exposes the canonical Python contract
  `reconstructRuntime({semanticIr, workflowIr, synchronizationIr, executionIr, memoryIr,
  runtimeGraph, runtimeType, tick})`; proven **Python ≡ JavaScript ≡ Dart** by execution →
  **Complete**. The envelope variant is `reconstructRuntimeFromEnvelope` (BREAKING).
- **`getRuntimeKernel`** — its observable kernel state (`{runtime_type}`) proven
  Python ≡ JavaScript ≡ Dart by execution → **Complete**.
- API parity matrix: **86 Complete · 27 Partial · 15 Deferred · 0 Missing**; 838 tests; 97.13% coverage.
  Group B is fully complete (10 executable-proven APIs total).

## [Unreleased] — Final Completion Protocol · Group B (executable parity)

### Changed (contract alignment, BREAKING)

- **`computeGlobalRuntimeFingerprint`**, **`queryRuntimeGraph`**, and
  **`validateReplayEquivalence`** now match the canonical Python contracts and are proven
  **Python ≡ JavaScript ≡ Dart** by execution (`validation/executable/`) → promoted to **Complete**:
  - `computeGlobalRuntimeFingerprint({extraction, graph, memory, sync, reconstruction, kaalkaSeal})`
  - `queryRuntimeGraph(Map graph, Map query)` → `{results, count, bounded}`
  - `validateReplayEquivalence(original, replayed)` → `{equivalent, checks:[{name, ok, original, replay}], bounded}`
  - The Dart-native variants are retained as `computeRuntimePipelineFingerprint`,
    `queryRuntimeGraphTyped`, and `validateReplayEquivalenceExtended`.
- API parity matrix: **84 Complete · 29 Partial · 15 Deferred · 0 Missing**; 831 tests; 97.13% coverage.

### Added

- `tools/generate_parity_manifest.py` → **PARITY_MANIFEST.json** (single source of truth:
  per-API python/javascript/dart presence, contract/behavior/executable parity, classification,
  proof type). `lib/src/parity/canonical_runtime.dart` (Python-canonical Group-B ports).

## [Unreleased] — Final Completion Protocol (executable parity)

### Changed (contract alignment)

- **`buildRuntimeMemory`** and **`queryRuntimeMemory`** now match the canonical Python contract:
  `buildRuntimeMemory({runtimeHistory, lineage, semanticRelations})` and
  `queryRuntimeMemory(memory, queryType, term)`. Proven **Python ≡ JavaScript ≡ Dart** by
  execution (`validation/executable/`, `EXECUTABLE_PARITY_MATRIX.md`) → promoted to **Complete**.
  The previous graph-based variants are retained as **`buildRuntimeMemoryFabric`** /
  **`queryRuntimeMemoryFabric`** (BREAKING for callers of the old graph-based signatures).
- `extract_database_runtime` (postgres/mysql/sqlite/redis + degraded) and
  `extract_kubernetes_runtime` re-implemented to Python's full field set; proven Python ≡ JS ≡ Dart
  → **Complete**.
- API parity matrix: **81 Complete · 32 Partial · 15 Deferred · 0 Missing**; 816 tests; 97.24% coverage.

### Added

- `validation/executable/` — 3-language executable parity harness (Python 2.0.1 + JavaScript via
  `tsx` + Dart) producing `EXECUTABLE_PARITY_MATRIX.md`; `COMPLETE_API_PROOF_MATRIX.md`,
  `PARTIAL_API_AUDIT.md`, `DEFERRED_API_AUDIT.md` auto-generated by `tools/`.

## [Unreleased] — Wave 3–4 (parity + OSS)

### Added

- `healSelector` / `buildSemanticAnchor` — native Dart port of the canonical
  Python `heal_selector` (moved Deferred → Partial). DOM-node strategies
  (`text_anchor`, `attribute_anchor`, `structural_fallback`) are full-fidelity,
  proven by 11 deep-equality vectors vs the Python reference
  (`validation/parity/selector_healing_api_vectors.json`,
  `test/parity/selector_healing_parity_test.dart`). The `semantic_anchor` HTML
  sub-path matches BeautifulSoup for well-formed content; nested inline markup is
  the documented bounded edge.
- `replayInteractions` / `recordInteraction` — native Dart port of Python
  `replay_interactions` (moved Deferred → Partial). The returned structure is a
  full-fidelity pure function of the interaction log, proven by 6 deep-equality
  vectors vs Python 2.0.1 (`validation/parity/interaction_replay_api_vectors.json`).
  The live-page action dispatch is the documented bounded edge.
- Three-way parity validator: `validation/validate_parity.dart` now asserts the
  deterministic core against **both** the JavaScript and Python references
  (Python ≡ JavaScript ≡ Dart, 11 vectors).
- `DART_REALITY_AUDIT.md`, `FINAL_TRUE_PARITY_REPORT.md` (proof-coverage audit +
  honest name-parity vs signature-parity disclosure); `tools/proof_coverage.py`.
- OSS governance files: `GOVERNANCE.md`, `MAINTAINERS.md`, `CODEOWNERS`,
  `RELEASE.md`, `SUPPORT.md`.
- Full Phase-10 `README.md` (Installation, Features, API Reference, Examples,
  Performance, Testing, Coverage, CI/CD, Pub.dev Release, Vision).
- Validation reports regenerated from measured reality: `REPOSITORY_VALIDATION_REPORT`,
  `TEST_VALIDATION_REPORT`, `COVERAGE_VALIDATION_REPORT`, `API_PARITY_VALIDATION_REPORT`,
  `README_GAP_REPORT`, `OSS_VALIDATION_REPORT`, `RELEASE_READINESS_REPORT`,
  `FINAL_STATE_OF_DART_BRANCH`.

### Changed

- `CONTRIBUTING.md` rewritten for Dart (was carrying Python `pip`/`pytest`/`playwright`
  instructions).
- API parity matrix: **79 Complete · 34 Partial · 15 Deferred · 0 Missing** (Proof Coverage Audit downgraded 11 unproven Complete → Partial).
- Test suite **779 → 802**; line coverage **97.23% → 97.26%** (6394/6574).
- `.pubignore` excludes `CODEOWNERS` from the published package.

## [2.0.1] — 2026-06-09 — Dart native release

### Added

- Native Dart runtime cognition infrastructure for humans and AI agents
- Kaalka v5 parity pipeline (`kaalka@5.0.0` from pub.dev)
- Cross-language validation (11/11 JavaScript reference vectors)
- Browser HTTP extraction, replay equivalence, runtime memory, reconstruction
- GitHub Actions CI on `dart` branch

### Runtime parity

- Ported **12 runtime-cognition families** to native Dart with **proven
  cross-language hash parity** — Dart output hashes byte-identically to Python's
  `compute_deterministic_hash` (`computeDeterministicHash(dartOut) == h(pyOut)`),
  save/load proven by temp-file roundtrip: `causality`, `semantic`,
  `synchronization`, `evolution_runtime`, `workflows`, `execution`,
  `memory-runtime`, `reconstruction-runtime`, `connectors/streaming/interaction`,
  `query/reasoning`, `persistence/crypto-session/identity/adaptive/distributed/
  session/auth`, `kernel/contracts/unified-IR` — **+72 public APIs**.
- Public-API parity vs Python `__all__`: **88/128 Complete**, 23 Partial,
  17 Deferred (OS/desktop/Electron/DevTools — documented), **0 Missing**. See
  `PUBLIC_API_MATRIX.md`, `DART_PARITY_AUDIT.md`, `DART_RELEASE_GAP_REPORT.md`.
- ~145 parity-proof vectors in `validation/parity/*_api_vectors.json`;
  assertions in `test/parity/*_parity_test.dart`. Honestly bounded (not faked):
  `compile_document`/`compile_repository` (need NLP/AST), `run_canonical_pipeline`
  (deterministic core only), and document/repository sub-paths of the query
  family — all classified Partial in the matrix.

### Quality

- Comprehensive unit-test suite: **779 tests** across all subsystems and the
  12 newly-ported runtime families
- **97.23% line coverage** (`dart test --coverage`); the only sub-90% file is
  `normalization.dart` (Node-subprocess NFKC fallback, unreachable when Node is
  on `PATH`)
- `dart analyze` clean (zero issues) under strict-casts + strict-inference
- `dart format` clean across the package
- `dart pub publish --dry-run` clean (no packaging warnings)

### Security

- No auth bypass, CAPTCHA defeat, or credential cracking

