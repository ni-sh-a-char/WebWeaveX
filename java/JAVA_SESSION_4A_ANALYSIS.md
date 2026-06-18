# JAVA_SESSION_4A_ANALYSIS

**Extraction subsystem — canonical-source identification (analysis only; no code).**

Per [`JAVA_BRANCH_POLICY.md`](../JAVA_BRANCH_POLICY.md): Python is the single source of
behavioural truth; nothing is ported from the Dart/JS symbols. This document is **Phase 1
(canonical source identification)** and a **Phase 4 feasibility summary** for the
Extraction layer. The detailed function inventory is in
[`JAVA_EXTRACTION_INVENTORY.md`](JAVA_EXTRACTION_INVENTORY.md); the dependency graph in
[`JAVA_EXTRACTION_DAG.md`](JAVA_EXTRACTION_DAG.md).

Canonical source materialized from `origin/python` @ `9625f4a` (WebWeaveX 2.1.0) into a
read-only worktree. All `file:line` references below are to that tree (`core/…`,
`webweavex/…`).

---

## 1. What "extraction" is in WebWeaveX

The public package (`webweavex/__init__.py`) exposes the extraction surface from several
**independent** canonical roots. Reading the Python canon, the surface splits into five
dependency classes — only the dependency class, not the name, determines portability:

| Class | Canonical root(s) | Public APIs | Blocking substrate |
| --- | --- | --- | --- |
| **A. Pure text/dict → IR** | `core/documents/*`, `core/ir/document_*`, `core/interaction/pagination_engine`, `core/adaptive/selector_healing_engine`, `core/archive`, `core/ingestion` | `extract_document_runtime`, `compile_document`, `extract_paginated_content`, `heal_selector`, `ingest_input` (+ internal `extract_archive`, `compile_media_ir`, `analyze_document`) | **none** — JDK-only, deterministic |
| **B. Filesystem walk → IR** | `core/repository/*`, `core/ir/repository_runtime_ir` | `extract_repository` | filesystem (`Path.rglob`); deterministic **but path-string/OS-separator sensitive** |
| **C. HTML-parser bound** | `core/extract/*` (lxml), `core/browser/html_semantic_extraction_engine`, `core/dom/dom_reconstruction_engine`, `core/extraction/semantic_content_extraction_engine` (`html.parser`) | `extract`, `extract_async`, `extract_docs`, `extract_repo`, `analyze` (source-mode), `stream_extract`, `extract_html_file`, `universal_extract` (html branch) | a **BeautifulSoup-parity Soup engine** — and **two** dialects (lxml + html.parser) |
| **D. Live I/O bound** | `core/fetch/http_fetcher` (network), `core/browser/playwright_runtime` (browser), `core/crawling/*` | `crawl`, `crawl_async`, `extract_web`, `extract_recursive`, `extract`/`extract_async` (URL path), `capture_dom_mutations`, `capture_websocket_frames`, `extract_infinite_scroll` | network / headless browser — cannot be parity-proven as a full API without stubs |
| **E. Binary-parser / platform bound** | `core/files/pdf_extraction_engine` (pypdf), `core/files/docx_extraction_engine` (python-docx), `core/multimodal/*`+`core/ocr` (Tesseract), `core/native/platform/*` (`sys.platform`) | `extract_native`, `run_native_cognition` (+ internal `extract_pdf_text`, `extract_docx_text`, and the `extract_multimodal` OCR boundary) | third-party binary parsers / host OS — non-deterministic across versions/platforms |

**Key structural fact (verified by full-tree grep):** the bs4/lxml dependency for the
`core/extract/*` family is confined to exactly **two leaf modules** —
`core/extract/html_extractor.py:7` (`BeautifulSoup(text, "lxml")`) and
`core/security/safe_parser.py:8` (`BeautifulSoup(text, "lxml")`). All other bs4 users
(`core/browser/*`, `core/dom/*`, `core/extraction/*`, `core/application/*`,
`core/semantic/*`) use `"html.parser"` and are **not reachable** from the `core/extract`
closure. The two dialects belong to disjoint clusters (C-extract vs C-browser).

---

## 2. Canonical source map (Phase 1)

Per-API source file, package, and the **top-level `core.*` packages** each pulls in
(transitive closure verified by reading the modules, not just the import line).

### Class A — pure (READY)

| Public API | Python source (`def`) | Transitive `core.*` packages |
| --- | --- | --- |
| `extract_document_runtime` | `core/documents/universal_document_extraction_engine.py:34` | `core.documents`, `core.knowledge`, `core.presentation`, `core.spreadsheets`, `core.ir` |
| `compile_document` → `compile_document_ir` | `webweavex/__init__.py:236` → `core/ir/document_ir.py:31` | `core.ir`, `core.documents` (semantic-IR + 6 discourse engines + ~13 regex engines), `core.evidence`, `core.semantic.semantic_uncertainty_engine` |
| `extract_paginated_content` | `core/interaction/pagination_engine.py:8` | `core.interaction` |
| `heal_selector` | `core/adaptive/selector_healing_engine.py:11` | `core.adaptive` (`selector_healing` + `semantic_anchor`) |
| `ingest_input` | `core/ingestion/universal_ingestion_engine.py` | `core.ingestion` (extension-map only) |
| *internal* `extract_archive` | `core/archive/archive_extraction_engine.py:10` | stdlib `zipfile` only |
| *internal* `analyze_document` | `core/documents/document_intelligence.py:9` | `core.documents` |
| *internal* `compile_media_ir` | `core/ir/media_ir.py:6` | `core.ir` |

### Class B — filesystem (READY-with-harness)

| Public API | Python source | Transitive `core.*` |
| --- | --- | --- |
| `extract_repository` | `core/repository/universal_repository_extraction_engine.py` | `core.repository` (11 engines) + `core.ir.repository_runtime_ir` — **self-contained**, no bs4/AST/network |

### Class C — Soup-bound (BLOCKED on a Soup engine)

| Public API | Python source | Soup dialect |
| --- | --- | --- |
| `extract`, `extract_async`, `extract_docs`, `extract_repo` | `core/extract/pipeline.py:63/84/105/109` | **lxml** (`html_extractor`, `safe_parser`) |
| `analyze` (source-mode) | `webweavex/__init__.py:171` | lxml (via `extract`) |
| `stream_extract` | `core/streaming/streaming_pipeline.py:7` → `extract()` | **lxml** (transitive — see §3) |
| `extract_html_file` / `universal_extract` (html branch) | `core/files/html_file_extraction_engine.py` | **html.parser** (×3 + `browser_ir`) |
| `extract_web` | `core/browser/universal_web_extraction_engine.py:144` | html.parser **+ Class D** |

The `core/extract/*` closure spans 20 top-level `core.*` packages
(`crypto, documents, execution_graph, extract, fetch, graph, intelligence, internet,
knowledge, llm, normalize, observability, parsers, performance, quality, repository,
schemas, security, serialize, universal`). All deep engines under those packages are
pure stdlib (`re`, `json`, `collections`); the only non-pure leaves are `fetch`
(network), `llm` (LLM/env), and the two bs4 modules.

### Class D — live I/O (PARTIAL core, network/browser boundary)

| Public API | Python source | Boundary leaf |
| --- | --- | --- |
| `crawl`, `crawl_async` | `core/crawling/crawler_engine.py:13` | `fetch_sync` (`requests.get`) |
| `extract_web` | `core/browser/universal_web_extraction_engine.py:144` | `render_page` (Playwright) line 319 |
| `extract_recursive` | `webweavex/__init__.py:187` | `_crawl` (network loop) |
| `capture_dom_mutations` | `core/streaming/dom_mutation_stream_engine.py:11` | live `MutationObserver` source |
| `capture_websocket_frames` | `core/streaming/websocket_runtime_engine.py:40` | live WebSocket source |
| `extract_infinite_scroll` | `core/interaction/infinite_scroll_engine.py:26` | live `page.evaluate` scroll |

### Class E — binary/platform (DEFERRED)

| Public API | Python source | Bound to |
| --- | --- | --- |
| `extract_native` | `core/native/native_runtime_orchestrator.py:207` | `sys.platform` (uia/ax/atspi) |
| `run_native_cognition` | `core/native/native_runtime_orchestrator.py:80` | `sys.platform` (+ electron CDP) |
| *internal* `extract_pdf_text` | `core/files/pdf_extraction_engine.py` | **pypdf** (version-unstable text) |
| *internal* `extract_docx_text` | `core/files/docx_extraction_engine.py` | **python-docx** |
| *internal* OCR boundary of `extract_multimodal` | `core/ocr/ocr_engine.py` | **Tesseract** binary |

`run_autonomous_extraction` (`core/distributed_extraction/autonomous_extraction_engine.py:14`),
`run_live_runtime` (`core/connectors/live_runtime_orchestrator.py:24`) and
`run_canonical_pipeline` (`core/kernel/runtime_pipeline.py:37`) are **pure schedulers /
aggregators over caller-supplied dicts** whose only non-pure edge is an *optional* fan-out
into Class C/D/E (native / web kind). Their cores are READY; they inherit a blocker only
when the optional branch is taken.

---

## 3. Two non-obvious dependency edges (reconciliation)

1. **`stream_extract` is NOT a pure snapshot transform.** It chunks text deterministically
   (`incremental_extract` → `parse_stream`) but then calls `extract(text)`
   (`core/extract/pipeline.py`). For a non-URL string the network is skipped (`fetch_raw`,
   §below), **but `_extract_core` still calls `extract_html` (bs4/lxml) and
   `safe_html_text` (bs4/lxml)**. So `stream_extract` is **Class C (Soup-bound)**, not a
   READY snapshot transform.

2. **Non-URL input is network-free.** `core/fetch/raw_fetcher.py:8` `fetch_raw(text)`
   wraps the string verbatim into a `FetchResponse(status_code=200, ok=True,
   source="raw")` — no socket. Therefore the *only* blocker on the raw-text `extract`
   path is the lxml Soup engine; the network is purely a URL-path concern.

3. **The `extract` family uses its own determinism stack, not the certified one.**
   `core/extract/enrichment_engine.py` fingerprints via `dumps_deterministic`
   (`core/serialize/deterministic_serializer.py`) + `fingerprint_v3` = `hex_fingerprint`
   = the `kaalka_encrypt_bytes` XOR/position cipher in `core/crypto/kaalka_engine.py` —
   **distinct** from the already-ported `stable_serialize` + `compute_kaalka_hash`
   (`sha256(stable_serialize)`). Porting the `extract` family therefore requires porting
   **two additional determinism primitives** beyond the Session-1 foundation. (The
   `core/documents/*` and `core/repository/*` Class-A/B families do **not** hash at
   all — their IRs are plain unhashed aggregate dicts, so they need neither stack.)

---

## 4. Feasibility summary (Phase 4 — full table in EXECUTION_PLAN §Feasibility)

| Verdict | APIs |
| --- | --- |
| **READY** (pure, parity-provable now, JDK-only) | `extract_document_runtime`, `compile_document`, `extract_paginated_content`, `heal_selector`, `ingest_input` (+ internal `extract_archive`, `analyze_document`, `compile_media_ir`); cores of `run_live_runtime`, `run_autonomous_extraction`, `replay_interactions` (output) |
| **READY-with-harness** (deterministic but path/separator-sensitive) | `extract_repository` |
| **BLOCKED — Soup engine** (deterministic once the engine exists) | `extract`, `extract_async`, `extract_docs`, `extract_repo`, `analyze` (source-mode), `stream_extract`, `extract_html_file`, `universal_extract` (html branch); transform-cores of `capture_dom_mutations`, `capture_websocket_frames` |
| **BLOCKED — network/browser** (Class D; full-API parity needs a stub → forbidden) | `crawl`, `crawl_async`, `extract_web`, `extract_recursive`, `extract`/`extract_async` (URL path), `extract_infinite_scroll` |
| **DEFERRED — permanent** (binary parser / `sys.platform`) | `extract_native`, `run_native_cognition`, internal `extract_pdf_text` (pypdf), `extract_docx_text` (python-docx), OCR boundary of `extract_multimodal` |

**Recommended next implementation slice:** the **Class-A pure document/interaction family**
(`extract_document_runtime` + `compile_document` + `extract_paginated_content` +
`heal_selector` + `ingest_input`), which is JDK-only, hashing-free, and needs **no new
substrate** — directly analogous to the certified Session-4 connector-runtime slice. This
advances preferred-order items #1–#3 (Extraction / Repository / Document) by their portable
subset while the Soup engine (the true multi-session blocker) is scoped separately. See
[`JAVA_SESSION_4A_EXECUTION_PLAN.md`](JAVA_SESSION_4A_EXECUTION_PLAN.md).

**Hard scope boundary for this session:** `extract` itself stays `⬜ Planned` until the
lxml Soup engine + `dumps_deterministic`/`fingerprint_v3` exist — no stub, no placeholder
(policy §5). The READY slice does **not** touch `core/extract/pipeline.py`.
