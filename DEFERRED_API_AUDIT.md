# DEFERRED_API_AUDIT.md

> **Generated from `PARITY_MANIFEST.json`** by `tools/generate_reports.py`.
> 13 Deferred = 5 genuinely platform-bound + 8 snapshot/data-input convertible candidates.

## Class 1 — Genuinely platform-bound (live browser `page`)

| API | Reason |
|-----|--------|
| `capture_dom_mutations` | reads MutationObserver state from a live page |
| `capture_websocket_frames` | reads CDP/DevTools frames from a live page |
| `extract_infinite_scroll` | scrolls a live page (Playwright/DevTools) |
| `extract_paginated_content` | navigates a live page |
| `recover_modal_runtime` | calls page.click(...) on a live page |

**Verdict:** remain Deferred — the Dart VM cannot host a driven browser in-process.

## Class 2 — Convertible (snapshot / data / persistence input)

| API | Disposition |
|-----|-------------|
| `execute_runtime_objective` | graph-input convertible (portability-A; not yet executable-proven) |
| `extract_native` | snapshot-input convertible (portability-A; not yet executable-proven) |
| `load_application_memory` | Kaalka persistence; convertible (not yet executable-proven) |
| `load_native_runtime` | Kaalka persistence; convertible (not yet executable-proven) |
| `run_application_cognition` | html+data-input convertible (portability-A; not yet executable-proven) |
| `run_native_cognition` | snapshot-input convertible (portability-A; not yet executable-proven) |
| `save_application_memory` | Kaalka persistence; convertible (not yet executable-proven) |
| `save_native_runtime` | Kaalka persistence; convertible (not yet executable-proven) |

**Verdict:** these are portability-A (not platform-bound). They remain Deferred only until executable-proven, then are promoted to Complete (same pattern as `extract_container_runtime` / `extract_ide_runtime`).
