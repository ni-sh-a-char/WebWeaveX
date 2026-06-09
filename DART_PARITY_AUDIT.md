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
| ✅ Complete | 51 | name-mapped + test-exercised (35 added via hash-parity ports) |
| 🟡 Partial | 15 | bounded Dart impl; full parity needs live network/browser |
| ⚪ Deferred | 17 | needs OS/desktop/Electron/DevTools — not in-process in Dart |
| ❌ Missing | 45 | remaining runtime-cognition families, portable with vector parity |

### Families ported with PROVEN cross-language hash parity (this pass)

| Family | APIs | Proof |
|--------|-----:|-------|
| causality | 5 | 8 hash vectors byte-identical to Python + save/load roundtrip |
| semantic | 5 | 8 hash vectors + roundtrip (non-empty-HTML UI/table path documented gap) |
| synchronization | 6 | 11 hash vectors + roundtrip |
| evolution_runtime | 6 | 10 hash vectors + roundtrip |
| workflows | 7 | 16 hash vectors + roundtrip |
| execution | 6 | 25 hash vectors |

Each ported API's Dart output hashes identically to Python's `compute_deterministic_hash` of the same call (see `validation/parity/*_api_vectors.json` and `test/parity/*_parity_test.dart`). The remaining 45 Missing cluster into: reconstruction-runtime (5), memory-runtime (5), query (5), ir-runtime (5), connectors-runtime (5), kernel (3), crypto-session (3), session (2), identity (2), adaptive (2), distributed-checkpoint (2), reasoning (1), contracts (1), auth (1) — same portable pattern.

## 4. Test inventory

- **551 tests** across crypto, determinism, graph, replay, memory, reconstruction, kernel, browser, connectors, and the 6 newly-ported runtime families (101 parity + 161 engine-coverage tests added this pass).
- **96.93% line coverage** (`dart test --coverage`, 3880/4003 lines).
- Cross-language parity vectors: `validation/parity/*_vectors.json` (crypto/graph core, 11/11) + `validation/parity/*_api_vectors.json` (78 runtime-API hash vectors).

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
