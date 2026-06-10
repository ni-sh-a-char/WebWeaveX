# DEFERRED_API_AUDIT.md

> Group D re-audit (2026-06-10): every Deferred API re-evaluated against the question
> *"can the Python behavior become deterministic under a snapshot-input architecture?"*
> Source of truth: `origin/python` 2.0.1 signatures. Started at 15 Deferred → now **13**
> (`extract_container_runtime` + `extract_ide_runtime` converted to executable Complete).

## Summary

| Class | Count | Disposition |
|-------|------:|-------------|
| Genuinely platform-bound (takes a live `page`) | 5 | Remain **Deferred** |
| Snapshot/data/persistence-input (convertible) | 8 | **Deferred → Partial** candidates; conversion in progress |
| Converted this audit (executable Complete) | 2 | `extract_container_runtime`, `extract_ide_runtime` |

---

## Class 1 — Genuinely Deferred (live browser `page` required)

These take a live `page: Any` object and observe/drive it (DevTools/Playwright). Python's own
contract is the live page, not a snapshot — converting would diverge from the canonical contract.

| API | Python signature | Reason |
|-----|------------------|--------|
| `extract_infinite_scroll` | `(page)` | scrolls a live page, observes lazy DOM |
| `extract_paginated_content` | `(page, next_selector)` | navigates a live page |
| `capture_websocket_frames` | `(page)` | reads CDP/DevTools frames from a live page |
| `capture_dom_mutations` | `(page)` | reads `page._test_dom_mutations` from a live page |
| `recover_modal_runtime` | `(page, html='')` | calls `page.click(...)` on a live page |

**Verdict:** remain Deferred — the Dart VM cannot host a driven browser in-process. (JavaScript
reaches these via Playwright/Puppeteer in-process; Dart cannot.)

---

## Class 2 — Convertible (snapshot / data / persistence input)

These do **not** require a live runtime — their Python signatures accept a `snapshot`, provided
data, or are pure Kaalka persistence. They are **Deferred → Partial** candidates and conversion is
underway (same pattern as `extract_database_runtime` / `extract_kubernetes_runtime`).

| API | Python signature | Convertibility | Notes |
|-----|------------------|----------------|-------|
| `extract_native` | `(runtime, application, …, snapshot=None, …)` | **A** | large flag-heavy signature; snapshot-driven core is deterministic |
| `run_native_cognition` | `(runtime, application, snapshot=None, memory=None, …)` | **A** | snapshot + provided memory |
| `run_application_cognition` | `(url, html, interactions=None, memory=None, …)` | **A** | composes over provided `html` + data (no live page) |
| `execute_runtime_objective` | `(objective, workflow_graph, action_graph, navigation, …)` | **A** | pure composition over provided graphs |
| `save_application_memory` | `(path, memory, key)` | **A** | Kaalka persistence (deterministic save/load roundtrip) |
| `load_application_memory` | `(path, key)` | **A** | Kaalka persistence |
| `save_native_runtime` | `(path, runtime, key)` | **A** | Kaalka persistence |
| `load_native_runtime` | `(path, key)` | **A** | Kaalka persistence |

**Verdict:** these 8 were mis-classified Deferred — none is platform-bound. They are scheduled for
the same executable-parity port (port Python's exact output, execute Python/JS/Dart, prove hashes,
promote). Until each is proven, it remains Deferred (honest: not yet executable-proven).

---

## Converted this audit (Deferred → Complete, executable parity)

| API | Proof |
|-----|-------|
| `extract_container_runtime` | Python ≡ JavaScript ≡ Dart on 3 fixtures (docker/podman/unknown) — `connectors_snapshot_api_vectors.json` |
| `extract_ide_runtime` | Python ≡ JavaScript ≡ Dart on 2 fixtures (vscode/empty) |

Both are snapshot-input deterministic functions (`extract_container_runtime(runtime, snapshot)`,
`extract_ide_runtime(ide, snapshot)`) — ported to Python's full field set and proven by execution.

## Verdict

Only **5 of the original 15** Deferred APIs are genuinely platform-bound (live-browser page). The
other 10 are snapshot/data/persistence-input deterministic functions: 2 are now executable-Complete
and 8 remain convertible (Deferred until executable-proven). This is the honest platform ceiling —
the live-`page` browser-automation surface is the only true Dart-VM limitation here.
