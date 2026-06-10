# DEFERRED_API_AUDIT.md

> Audit of every API classified **Deferred** (15) on the `dart` branch, 2026-06-10.
> Deferred = the Python behaviour requires an external capability that the Dart VM cannot host
> in-process. Portability is **C** (external runtime) for all rows. Source of truth:
> `origin/python` 2.0.1 vs `lib/`.

## Summary

| Group | Count | External capability required |
|-------|------:|------------------------------|
| Live-browser DevTools / Playwright | 5 | a driven Chromium/DevTools session |
| Native application / Electron cognition | 4 | a running desktop/Electron app + OS automation |
| Native OS runtime | 4 | OS-level process/native introspection |
| Container / IDE | 2 | Docker daemon / a live IDE instance |

All 15 share the same structural blocker: Python reaches these via Playwright/Puppeteer, Electron,
OS automation, the Docker API, or IDE protocols **in-process**. Dart has no in-process equivalent;
a faithful port would require shelling out to an external runtime, which breaks the "no import-time
side effects / deterministic, bounded" contract. JavaScript reaches 126/126 precisely because Node
can host these drivers in-process.

---

## Group 1 — Live-browser DevTools / Playwright (5)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `extract_infinite_scroll` | needs a live page to scroll and observe lazy-loaded DOM | **C** | N/A in-process | driven browser (Playwright/Puppeteer) |
| `extract_paginated_content` | needs live navigation across pages | **C** | N/A | driven browser |
| `capture_websocket_frames` | needs CDP/DevTools network domain to observe frames | **C** | N/A | Chrome DevTools Protocol |
| `capture_dom_mutations` | needs a live `MutationObserver` on a real page (Dart impl returns empty without a page) | **C** | N/A | live page runtime |
| `recover_modal_runtime` | needs a live `page` object with `.click` to dismiss modals | **C** | N/A | driven browser page |

## Group 2 — Native application / Electron cognition (4)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `run_application_cognition` | drives a running desktop/Electron application | **C** | N/A | Electron/desktop automation |
| `execute_runtime_objective` | executes objectives against a live app runtime | **C** | N/A | live app runtime |
| `save_application_memory` | persists state captured from a live app session | **C** | N/A | depends on the live capture above |
| `load_application_memory` | restores into a live app session | **C** | N/A | live app runtime |

## Group 3 — Native OS runtime (4)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `extract_native` | introspects native OS processes/windows | **C** | N/A | OS-level native automation |
| `run_native_cognition` | runs cognition over a native OS runtime | **C** | N/A | native OS access |
| `save_native_runtime` | persists native runtime capture | **C** | N/A | depends on native capture |
| `load_native_runtime` | restores native runtime | **C** | N/A | native OS access |

## Group 4 — Container / IDE (2)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `extract_container_runtime` | inspects a live container via the Docker API | **C** | N/A | Docker daemon/API |
| `extract_ide_runtime` | inspects a live IDE instance | **C** | N/A | IDE extension/protocol |

---

## Note on save/load pairs

`save_application_memory` / `load_application_memory` (and the native save/load pairs) are Deferred
**not** because persistence is hard in Dart — Kaalka persistence is already Complete elsewhere — but
because the *data they persist* originates from a live application/native capture that cannot be
produced in-process. If a caller supplies a pre-captured snapshot, a bounded deterministic path
could be added (portability would shift to **B**), mirroring the `heal_selector` /
`replay_interactions` pattern; that has not been implemented.

## Verdict

All 15 Deferred APIs are correctly classified: each requires a live external runtime the Dart VM
cannot host in-process. None can become Complete without shelling out to an external driver, which
the deterministic/bounded contract forbids. This is the genuine platform ceiling.
