# JAVA_EXTRACTION_ROADMAP

**Phase 6 — extraction APIs by blocker type, separating import-time from behavioral blockers**
(Session-6 runtime-tracing methodology). Code-derived; no documentation assumptions.

## Classification

| API | clean / blocked | blocker type | implementable now? |
| --- | --- | --- | --- |
| `extract_database/api/runtime_streams/telemetry/container/ide/kubernetes_runtime` | **clean** | — | **done** (7) |
| `extract_document_runtime`, `extract_paginated_content` | **clean** | — | **done** |
| `extract_repository` | clean | filesystem (path-string) | **yes** (needs path-canon harness) |
| `extract_infinite_scroll` | clean | live-source (transform clean) | **yes** (fixture-driven) |
| `capture_dom_mutations`, `capture_websocket_frames` | clean | live-source (transform clean) | **yes** (snapshot transform) |
| `extract` / `extract_async` / `extract_docs` / `extract_repo` | blocked | **behavioral** lxml/bs4 parse + network + LLM | no (real Soup engine needed) |
| `stream_extract` | blocked | **behavioral** bs4 (via `extract()`) | no |
| `extract_web` | blocked | **behavioral** Playwright + html.parser | no |
| `crawl` / `crawl_async` / `extract_recursive` | blocked | **behavioral** network | no |
| `universal_extract` | blocked | **behavioral** PDF/DOCX/OCR/bs4 | no |
| `extract_multimodal` | blocked | **behavioral** Tesseract OCR | no (graceful-degrade only) |
| `extract_native` | blocked | **behavioral** `sys.platform` | permanent-deferred |
| `compile_document`, `compile_repository`, `query_documents` | blocked | **import-time only** (bs4 never executed — S6) | **yes if** bs4 import is decoupled upstream |

## Import-time vs behavioral (the key split)

- **Import-time-only blockers** (bs4 loaded but never run): `compile_document`,
  `compile_repository`, `query_documents`, and the ~26 semantic/memory/modal APIs. These are
  *behaviorally clean* (proven by runtime trace). They become immediately implementable the
  moment the upstream `core.semantic`/`core.evidence` eager bs4 import is made lazy — **no Java
  Soup engine required**.
- **Behavioral blockers** (parser/OCR/browser/network actually executed): the true HTML/web
  extraction surface (`extract*`, `extract_web`, `crawl*`, `stream_extract`, `universal_extract`,
  `extract_multimodal`). These need real substrate (lxml+html.parser Soup engine; or boundary
  injection for network/OCR/browser) and are multi-session.

## Implementable-now extraction (no upstream change)

1. `extract_repository` (path-canon harness) — repository extraction.
2. `extract_infinite_scroll`, `capture_dom_mutations`, `capture_websocket_frames` —
   transform-cores against fixture snapshots (live source documented as deferred).

These 4 are the immediate extraction wins. The larger HTML surface waits on the Soup engine; the
document/repository-IR surface waits on the upstream bs4-decouple (highest leverage). See
[`JAVA_BLOCKER_HIERARCHY.md`](JAVA_BLOCKER_HIERARCHY.md) and
[`JAVA_EXTRACTION_REALITY.md`](JAVA_EXTRACTION_REALITY.md).
