# DEFERRED_API_AUDIT.md

> **Generated from `PARITY_MANIFEST.json`** by `tools/generate_reports.py`.
> 8 Deferred = 7 genuine platform ceiling + 1 bounded-HTML Partial candidate.

## Class 1 — Genuine platform ceiling (live browser `page` or OS-coupled)

| API | Reason |
|-----|--------|
| `capture_dom_mutations` | reads MutationObserver state from a live page |
| `capture_websocket_frames` | reads CDP/DevTools frames from a live page |
| `extract_infinite_scroll` | scrolls a live page (Playwright/DevTools) |
| `extract_native` | branches on sys.platform (Windows UIA / macOS AX / Linux AT-SPI) — OS-coupled, non-deterministic across platforms even in Python |
| `extract_paginated_content` | navigates a live page |
| `recover_modal_runtime` | calls page.click(...) on a live page |
| `run_native_cognition` | branches on sys.platform (UIA/AX/AT-SPI accessibility runtimes) + Electron CDP/IPC — OS-coupled even in Python |

**Verdict:** remain Deferred — genuine platform ceiling (driven browser, or OS-level accessibility runtimes branched on `sys.platform`). Not reproducible deterministically in the Dart VM; non-deterministic across platforms even in Python.

## Class 2 — Bounded-HTML Partial candidate

| API | Disposition |
|-----|-------------|
| `run_application_cognition` | pure over provided html but depends on a BeautifulSoup HTML-semantics subsystem — at best a bounded Partial (large port, not Complete) |

**Verdict:** `run_application_cognition` is pure over a provided `html` string (no live page, no OS coupling), but depends on a BeautifulSoup-based HTML-semantics subsystem (`extract_ui_semantics`, `build_form_runtime`, `build_dashboard_runtime`, …). Porting it yields at best a **bounded Partial** (matching BeautifulSoup only for well-formed HTML, like `heal_selector`'s semantic_anchor) — not executable Complete. Documented as the remaining bounded blocker.

## Group-D outcome

Of the original 15 Deferred: **4 converted to executable Complete** (`extract_container_runtime`, `extract_ide_runtime`, `execute_runtime_objective`, + the application/native save/load pairs as Kaalka roundtrips), **7 are a genuine platform ceiling** (5 live-`page` + 2 OS-coupled native), and **1 is a bounded-HTML Partial candidate**. This is the achievable Dart-platform ceiling.
