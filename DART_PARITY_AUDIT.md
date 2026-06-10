# DART_PARITY_AUDIT.md

**Audited:** `dart` branch (worktree) · **Reference:** `python` (PyPI 2.0.1) + `javascript` (certified 128/128)
**Method:** measured, not assumed. `tools/dart_parity_audit.py` parses the real Python `webweavex.__all__` and the real Dart `lib/` symbols; cross-language byte parity is proven by executed vector tests (`test/parity/`), never by inspection.

---

## 1. Module inventory

| Layer | Dart `lib/src` packages | Status |
|-------|--------------------------|--------|
| crypto | `kaalka_runtime`, `kaalka_v5_proc`, `time_key`, `hashing` | present |
| determinism | `normalization`, `normalization_core`, `dom_stabilization`, `fingerprint`, `stable_serialize` | present |
| graph | `runtime_graph`, `runtime_graph_replay`, `runtime_graph_reconstruction` | present |
| kernel | `runtime_pipeline`, `replay_pipeline`, `reconstruction_pipeline` | present |
| memory | `runtime_memory`, `runtime_memory_graph`, `memory_lineage`, `memory_replay`, `query_memory` | present |
| replay | `replay_runtime`, `replay_graph`, `replay_memory`, `replay_dom`, `replay_fingerprint`, `replay_equivalence` | present |
| reconstruction | `reconstruct_runtime/graph/memory/replay/browser` | present |
| browser | `extract_web`, `render_page`, `runtime_session`, `authenticated_runtime`, `browser_identity`, `capture_runtime`, `runtime_continuation`, `runtime_snapshot`, `spa_stabilizer` | present (bounded HTTP) |
| connectors | `connectors_impl`, `postgres_connector` | present |
| distributed / orchestration / semantic | `distributed_extraction_orchestrator`, `orchestration_engine`, `semantic_memory` | present |

47 source files, 740 instrumented lines.

## 2. Public API inventory

Measured by `tools/dart_parity_audit.py` → `PUBLIC_API_MATRIX.md`.

- Python public APIs (`__all__`): **128**

## 3. Missing-parity inventory

| Status | Count | Notes |
|--------|------:|-------|
| ✅ Complete | 89 | name-mapped + cross-language proof-verified (see COMPLETE_API_PROOF_MATRIX.md) |
| 🟡 Partial | 26 | bounded Dart impl; full parity needs live network/browser/NLP/AST (incl. `heal_selector`, `replay_interactions`) |
| ⚪ Deferred | 13 | needs OS/desktop/Electron/DevTools — not in-process in Dart |
| ❌ Missing | 0 | — |

### Families ported with PROVEN cross-language hash parity

Each ported API's Dart output hashes identically to Python's `compute_deterministic_hash` of the same call (`computeDeterministicHash(dartOut) == h(pyOut)`); save/load proven by temp-file roundtrip. Vectors in `validation/parity/*_api_vectors.json`, assertions in `test/parity/*_parity_test.dart`.

| Family | APIs | Proof |
|--------|-----:|-------|
| causality | 5 | 8 hash vectors + roundtrip |
| semantic | 5 | 8 hash vectors + roundtrip (non-empty-HTML UI/table path documented gap) |
| synchronization | 6 | 11 hash vectors + roundtrip |
| evolution_runtime | 6 | 10 hash vectors + roundtrip |
| workflows | 7 | 16 hash vectors + roundtrip |
| execution | 6 | 25 hash vectors |
| memory-runtime | 5 | 10 hash vectors + roundtrip |
| reconstruction-runtime | 5 | 17 hash vectors + roundtrip |
| persistence / crypto-session / identity / adaptive / distributed / session / auth | 14 | 12 hash vectors + roundtrips |
| connectors / streaming / interaction | 6 | 18 hash vectors |
| query / reasoning | 8 | 17 hash vectors (graph/knowledge/topology/dict paths) |
| kernel / contracts / unified-IR | compileUnifiedRuntimeIr, UniversalInput, RuntimeKernel, getRuntimeKernel | 18 hash vectors |

The 26 Partial include 11 downgraded by the Proof Coverage Audit, plus: `heal_selector` (DOM-node strategies proven; nested-HTML bounded), `replay_interactions` (return structure proven; live-page dispatch bounded), `compile_document`/`compile_repository` (need an NLP/AST IR compiler — UnsupportedError stub), `run_canonical_pipeline` (deterministic kernel core proven; full pipeline drives network/extraction phases), `reason_semantically`/`query_documents`/`query_repository`/`query_semantics`/`analyze` (primary/result-dict path proven; document/repository/network sub-paths not yet portable), plus the bounded extract/crawl/stream pipeline. See `PUBLIC_API_MATRIX.md`.

## 4. Test inventory

- **802 tests** across crypto, determinism, graph, replay, memory, reconstruction, kernel, browser, connectors, selector-healing, and 12 ported runtime families.
- **97.26% line coverage** (`dart test --coverage`, 6394/6574 lines); only `normalization.dart` (Node NFKC fallback, unreachable when Node on PATH) is below 90%.
- Cross-language parity vectors: `validation/parity/*_vectors.json` (crypto/graph core, 11/11) + `validation/parity/*_api_vectors.json` (~145 runtime-API hash vectors).

## 5. Documentation inventory

README, CHANGELOG, ROADMAP, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, NOTICE, AUTHORS, CITATION.cff all present. `docs/` contains architecture, kaalka, replay, security, validation, and archive trees. API reference: `docs/api/`.

## 6. CI inventory

`.github/workflows/ci.yml`, `.github/workflows/dart.yml`. Gates needed: analyze, test, coverage, publish dry-run (see `DART_RELEASE_GAP_REPORT.md`).

## 7. Pub inventory

- `pubspec.yaml` — name `webweavex`, version `2.0.0`, Apache-2.0, topics + funding set.
- `dart analyze` → 0 issues · `dart format` → clean · `dart pub publish --dry-run` → 0 warnings (benign version hint only).
- Published pub.dev version: `0.1.1` (this tree is unpublished `2.0.0`, aligned to cross-language versioning).

## Verification commands

```bash
dart analyze
dart test
dart test --coverage=coverage && dart pub global run coverage:format_coverage \
  --lcov --in=coverage --out=coverage/lcov.info --report-on=lib \
  --packages=.dart_tool/package_config.json
dart pub publish --dry-run
python tools/dart_parity_audit.py   # regenerates PUBLIC_API_MATRIX.md
```
