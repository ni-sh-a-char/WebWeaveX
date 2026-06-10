# DART_RELEASE_GAP_REPORT.md

Gap between the current Dart runtime and first-class parity with Python (2.0.1) / JavaScript (128/128). Grounded in `PUBLIC_API_MATRIX.md`. No assumed parity.

## Release-quality gates — current state

| Gate | State |
|------|-------|
| `dart analyze` | ✅ 0 issues (strict-casts + strict-inference) |
| `dart format` | ✅ clean |
| `dart test` | ✅ 779 passing |
| Coverage | ✅ 97.23% (target 90%) |
| `dart pub publish --dry-run` | ✅ 0 warnings (benign version hint) |
| OSS files | ✅ all present |
| CI gates | ✅ `.github/workflows/dart.yml` runs format + analyze + test + coverage(≥90% gate) + parity + publish-dry-run on push/PR to `dart` |

The existing surface is already release-quality. The gap is **API breadth**, not packaging.

## Public-API gap

128 Python APIs: **94 Complete**, 26 Partial, 8 Deferred, **0 Missing** (was 16/80; +72 ported with proven cross-language hash parity across 12 runtime-cognition families).

### Phased close-out plan (parity-verified)

Each ported API must ship with: implementation + a passing parity test (Dart output deep-equals a Python-generated vector, or a structural/roundtrip test where I/O precludes a pure vector) + coverage + a matrix row flip. An API without a passing test stays Partial/Missing — never marked Complete.

| Phase | Families | APIs | Approach |
|------:|----------|-----:|----------|
| 1 (done) | core runtime: graph, IR core, kaalka, serialization, replay, reconstruction, validation | 16 | shipped + vector-tested (11/11 core) |
| 2 | memory-runtime, session, crypto-session, identity-save/load, adaptive-save/load, distributed-checkpoint | ~16 | kaalka encrypt→file; roundtrip + structural tests |
| 3 | causality, semantic, synchronization, evolution_runtime, workflows, execution, reconstruction-runtime, query, reasoning, kernel, ir-runtime, connectors-runtime | ~64 | faithful port of deterministic dict engines; Python-vector parity tests |
| 4 | browser/extract/crawl/stream pipeline | 15 (Partial) | bounded HTTP parity for offline/deterministic paths; live-render parity documented as host-provided |
| 5 | native, application, interaction (Playwright/DevTools), electron, desktop, accessibility, k8s/container/ide | 17 (Deferred) | honest limitation docs + best-available bounded stub where meaningful |

## Honest limitations (never faked)

- **Deferred (17):** `extract_native`, `run_native_cognition`, `save/load_native_runtime`, `run_application_cognition`, `execute_runtime_objective`, `save/load_application_memory`, `heal_selector`, `recover_modal_runtime`, `replay_interactions`, `extract_infinite_scroll`, `extract_paginated_content`, `capture_websocket_frames`, `capture_dom_mutations`, `extract_ide_runtime`, `extract_container_runtime`. These require desktop/OS automation, Electron IPC, Chrome DevTools/Playwright, or accessibility trees that Dart cannot drive in-process without an external host. Python achieves them via Playwright + OS bridges. Dart parity is deferred and documented, not stubbed-as-complete.
- **Partial (15):** the extraction/crawl pipeline. Dart ships a bounded HTTP fetcher (`render_page`); full DOM-rendered parity needs a browser engine supplied by the host environment. Deterministic/offline code paths reach parity; live rendering does not.
- **`normalization.dart`** Node-subprocess NFKC fallback is unreachable when Node is on PATH (the one uncovered line); pure-Dart CRLF/volatile normalization is fully covered.

## Definition of done

Dart is a first-class WebWeaveX runtime when: every Complete API has implementation + test + docs; every Partial/Deferred API is explicitly classified here and in `PUBLIC_API_MATRIX.md` with the reason; gates stay green; CI is green. Full byte-parity for the deterministic families (Phases 2–3) is the active program; platform-limited families (Phases 4–5) are bounded + documented.
