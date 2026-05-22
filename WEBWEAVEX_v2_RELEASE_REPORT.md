# WEBWEAVEX v2 RELEASE REPORT

**Version:** 2.0.0  
**Date:** 2026-05-22  
**Status:** Production release candidate

## 1. Extraction domains

| Domain | API | Validated |
|--------|-----|-----------|
| Browser | `extract_web`, `run_canonical_pipeline` | Live Playwright |
| Repository | `extract_repository` | AST + topology |
| Documents | `extract_document_runtime` | MD/HTML/PDF fixtures |
| Multimodal | `extract_multimodal` | PNG pipeline |
| Streaming | `extract_web(stream_runtime=True)` | WS/SSE/mutations |
| Electron | `extract_native(runtime="electron")` | CDP + storage + IPC |
| Native | `extract_native` | Platform probes + fallback |
| Connectors | `extract_*_runtime` | SQLite/API/K8s snapshots |

## 2. Runtime systems

- **Canonical pipeline:** `core/kernel/runtime_pipeline.py`
- **Determinism:** `compute_global_runtime_fingerprint()`, DOM/SPA stabilization
- **Replay:** `validate_replay_equivalence()`
- **Memory:** `stable_memory_hash()`, sorted merge
- **Execution:** allowlisted sandbox
- **Reconstruction:** hash-stable `runtime_id`

## 3. Security

- Kaalka-only persistence (`core.crypto.kaalka_runtime_engine`)
- No eval/exec in `core/execution/` (audited)
- Encrypted sessions via `save_encrypted_session`

## 4. Determinism

- Kaalka ciphertext stable across repeated encrypt
- Same HTML → same SPA fingerprint
- Reconstruction inputs → identical `runtime_id`
- Sorted runtime graphs

## 5. Enterprise readiness

| Gate | Result |
|------|--------|
| Tests | **717 passed** |
| Coverage | **72%** (90% roadmap) |
| `import webweavex` | **2.0.0** instant |
| Wheel | `webweavex-2.0.0-py3-none-any.whl` |

## 6. Remaining limitations

- Coverage below 90% target without full connector cluster integration tests
- Live dynamic SPAs may differ across separate network fetches
- Native UIA/AX/AT-SPI need optional OS packages for full live capture

## Reports

See `FINAL_*` reports at repository root and `validation/` scripts for reproducible audits.
