# JAVA_EXTRACTION_INVENTORY

**Phase 2 — every extraction-related function, documented from the Python canon.**

Source: `origin/python` @ `9625f4a` (2.1.0). Columns: **Det.** = deterministic
(✅ pure / 🟡 deterministic-with-caveat / ❌ non-deterministic); **Hash** = which
serialization/fingerprint stack it touches; **G/M/Rp/Rc** = graph / memory / replay /
reconstruction subsystem dependency.

Legend for *Hash*: `—` none; `stable` = certified `stable_serialize`+`compute_kaalka_hash`
(already in Java); `extract-stack` = `dumps_deterministic`+`fingerprint_v3`/`kaalka_engine`
(NOT yet in Java); `sha256` = plain `hashlib.sha256`; `kaalka-payload` =
`compute_kaalka_hash_payload` (certified, in Java).

---

## A. Public manifest APIs

### `extract_document_runtime`  — Class A, READY
- **Path:** `core/documents/universal_document_extraction_engine.py:34`
- **Purpose:** Compile a plain-text (+ optional slides/workbook) document into a document
  runtime IR (structure, hierarchy, citations, references, tables, slides, worksheets,
  knowledge graph).
- **In:** `text: str`, `slides: Optional[List[Dict]]=None`, `workbook: Optional[Dict]=None`
- **Out:** dict — keys `structure, hierarchy, citations, references, tables, slides,
  worksheets, knowledge_graph, document_ir` (`document_ir` = `compile_document_runtime_ir`,
  shape `{"ir":"document_runtime", …, "bounded":True}`).
- **Det.:** ✅ pure stdlib (`re`, `splitlines`, `enumerate`); no I/O/time/random.
- **Hash:** — (IR is an unhashed aggregate).
- **Deps:** `core.documents.{document_structure,document_hierarchy,citation_extraction,
  reference_extraction,document_table}`, `core.knowledge.document_knowledge_graph`,
  `core.presentation`, `core.spreadsheets`, `core.ir.document_runtime_ir`.
- **G/M/Rp/Rc:** none (knowledge graph is a local linear `next_section` dict, not `core.graph`).

### `compile_document`  — Class A, READY (large)
- **Path:** `webweavex/__init__.py:236` → `core/ir/document_ir.py:31` (`compile_document_ir`)
- **Purpose:** Build the epistemic Document IR (concepts/claims/arguments/rhetorical_units/
  semantic_graph/lineage/confidence) from text.
- **In:** `text: str`  **Out:** `DocumentIR` mapped onto `empty_document_ir()` shape.
- **Det.:** ✅ pure (regex/heuristic discourse engines + `core.evidence`).
- **Hash:** — (uses `core.ir._base.merge_evidence` = `sorted(set)`; no kaalka).
- **Deps:** `core/documents/document_semantic_ir_engine.py:13` → 6 discourse engines
  (`rhetorical_parser, argument_dependency, concept_progression, tutorial_prerequisite,
  coreference_graph, document_dependency_graph`) → ~13 further `core.documents.*` regex
  engines → `core.evidence` (epistemic engine, grep-verified free of NLP/ML libs and
  non-determinism) + `core.semantic.semantic_uncertainty_engine`.
- **G/M/Rp/Rc:** none.
- **Note:** Largest READY surface (~20 engines). Mechanical but bulk — split across ≥2 slices.

### `extract_paginated_content`  — Class A, READY
- **Path:** `core/interaction/pagination_engine.py:8`
- **Purpose:** Walk "next" links up to `MAX_PAGES=100`, recording `{url, order}`, with
  cycle prevention.
- **In:** `page` (object exposing `_test_url`/`url`/`click`/`_test_paginate`), `next_selector`
- **Out:** `{pages:[{url,order}], visited_count, loop_prevented, bounded}`
- **Det.:** ✅ pure traversal over fixture attributes (`page.click` try/except-guarded,
  only called if present). This is why the manifest marks it **Complete**.
- **Hash/Deps/G-M-Rp-Rc:** — / `core.interaction` / none.

### `heal_selector`  — Class A, READY  *(manifest Partial — see governance audit)*
- **Path:** `core/adaptive/selector_healing_engine.py:11`
- **Purpose:** Produce a healed CSS/text/attribute selector from DOM nodes + a semantic
  anchor, with ranked fallback candidates.
- **In:** `selector: str`, `dom_nodes: List[Dict]`, `html: str`
- **Out:** `{original, healed_selector, strategy, candidates, bounded}`
- **Det.:** ✅ pure regex + sorted-attribute scan + `build_semantic_anchor`
  (`core/adaptive/semantic_anchor_engine.py:11`); **no I/O** (the `semantic_anchor` bs4
  use is on the *caller-supplied* `html` string, deterministic given the string — but it
  is `html.parser`, so a tiny Soup edge exists; see Risks R-7).
- **Hash/Deps/G-M-Rp-Rc:** — / `core.adaptive` / none.

### `ingest_input`  — Class A, READY
- **Path:** `core/ingestion/universal_ingestion_engine.py`
- **Purpose:** Detect input type by **file extension** (+ URL prefix) → dispatch key.
- **In:** `path: str`  **Out:** `{input_type, …}` (keys: pdf/docx/pptx/xlsx/csv/json/xml/
  html/markdown/text/repository/archive/image/url/unknown).
- **Det.:** ✅ pure string ops — `Path(path).suffix.lower()` against a static map +
  `startswith("http")`. **No filesystem stat, no magic bytes, no mimetypes.**
- **Hash/Deps/G-M-Rp-Rc:** — / `core.ingestion` / none.

### `extract_repository`  — Class B, READY-with-harness
- **Path:** `core/repository/universal_repository_extraction_engine.py`
- **Purpose:** Walk a repo path → languages/graph/services/dependencies/apis/flows/infra/
  deployments/build-systems + `repository_ir`.
- **In:** `path: str`  **Out:** 11-key dict + `repository_ir`
  (`{"ir":"repository_runtime", …, "bounded":True}`).
- **Det.:** 🟡 deterministic **per machine** — every engine sorts output by string key —
  **but** `repository_ingestion_engine.py:66/75` embeds `str(file)`/`str(root)` (absolute
  path **and** OS separator `\` vs `/`) and `file.stat().st_size`. → byte-exact
  cross-platform parity needs a canonicalization harness (Risk R-2). Also `MAX_FILES=100000`
  truncates **before** the sort (Risk R-3).
- **Hash:** — (IR unhashed).
- **Deps:** 11 `core.repository.*` engines + `core.ir.repository_runtime_ir` — fully
  self-contained; no bs4/AST/network/time/random.
- **G/M/Rp/Rc:** none (file/topology graphs are local node/edge dicts).
- **Tables to port byte-exact:** `SUPPORTED_CODE_EXTENSIONS` (9), `SKIP_DIR_NAMES` (7),
  `EXTENSION_LANGUAGE_MAP` (9), `SERVICE_FILES` (8), `INFRA_FILES` (9), `BUILD_FILES` (8),
  `ROUTE_PATTERNS` (3 regex, .py only), `IMPORT_RE` (MULTILINE). `primary_language` =
  `Counter.most_common(1)` (tie-break = file-sorted insertion order — Risk R-4).

### `extract`, `extract_async`, `extract_docs`, `extract_repo`  — Class C, BLOCKED (Soup+lxml)
- **Path:** `core/extract/pipeline.py:63 / 84 / 105 / 109` (`extract_docs`/`extract_repo`
  are thin wrappers → `extract`).
- **Purpose:** Fetch (or wrap raw text) → `_extract_core` → enrich into the full extraction
  envelope.
- **In:** `str | Dict` (`{source, llm}`)  **Out:** large nested dict (`content, code,
  dependencies, relationships, metadata{fetch,llm}, raw_text, source_url, fingerprint, …`).
- **Det.:** 🟡 deterministic core, ❌ at entry: `fetch_sync`/`fetch_async` (network) on URL,
  `groq_complete` (LLM/env) when `llm=="groq"`. Non-URL + no-LLM = deterministic **but
  Soup-bound**.
- **Hash:** `extract-stack` (`dumps_deterministic` + `fingerprint_v3`/`kaalka_engine`) at
  `enrichment_engine.py:440/443`; `sha256` content_hash in `metadata_extractor`.
- **Deps:** 20 `core.*` packages (see ANALYSIS §2-C). bs4/lxml via `html_extractor` +
  `safe_parser`.
- **G/M/Rp/Rc:** pure in-result graph builders only; does **not** touch kernel/replay/IR.

### `analyze`  — Class C (source-mode) / READY (graph-mode), PARTIAL
- **Path:** `webweavex/__init__.py:171`
- **Purpose:** If given `(nodes, edges)` → `analyze_graph` (pure, READY). If given a source
  → runs `extract` then `analyze_graph` on the extracted graph (inherits Class-C/D).
- **In:** `input_data`, `edges=None`  **Out:** graph-analysis dict.
- **Det.:** ✅ graph-mode (`core/intelligence/graph_analyzer.py`); 🟡 source-mode.
- **Hash/Deps:** — / `core.intelligence` (graph-mode) ; + `core.extract` (source-mode).

### `extract_recursive`  — Class D, BLOCKED (network)
- **Path:** `webweavex/__init__.py:187` — `_crawl(url)` then `extract(url)`; merges
  `metadata.crawl`. Inherently network (crawl loop + URL extract).

### `crawl`, `crawl_async`  — Class D, BLOCKED (network), pure core
- **Path:** `core/crawling/crawler_engine.py:13`; `crawl_async` = `asyncio.to_thread(_crawl)`
  (`__init__.py:183`).
- **Purpose:** BFS crawl with deterministic queue/budget/dedup/domain-policy.
- **In:** `seed_url, max_depth, max_pages, same_domain_only`  **Out:** `{visited, queued,
  discovered, depth_map}` (all sorted).
- **Det.:** 🟡 only `fetch_sync` (line 26, `requests.get`) is non-deterministic; queue/
  budget/`canonical_url`/`allow_url`/`discover_links` are pure.
- **Deps:** `core.crawling.{queue,dedup,domain_policy,crawl_budget,traversal}` + `core.fetch`.

### `stream_extract`  — Class C, BLOCKED (Soup, transitive)
- **Path:** `core/streaming/streaming_pipeline.py:7`
- **Purpose:** Chunk text incrementally → `extract(text)`; annotate `metadata.streaming`.
- **In:** `input_data` (str)  **Out:** `extract()` dict + `metadata.streaming{chunk_count,
  chunk_order}`.
- **Det.:** 🟡 chunking pure; `extract()` skips network on non-URL **but still invokes
  bs4/lxml** → Soup-bound (reconciliation, ANALYSIS §3.1).
- **Deps:** `core.streaming` + transitively all of `core.extract`.

### `universal_extract`  — dispatcher, mixed
- **Path:** `webweavex/universal_extract.py:30`
- **Purpose:** `ingest_input` → branch by type. **pdf**→pypdf (E), **docx**→python-docx (E),
  **image**→OCR (E), **archive**→zipfile (A, READY), **html**→`extract_html_file`
  (C, html.parser), **repository**→`extract_repository` (B), else `{"unsupported":True}`.
- **Det.:** per-branch (see component verdicts). Router itself pure.

### `extract_web`  — Class C+D, PARTIAL (browser + html.parser)
- **Path:** `core/browser/universal_web_extraction_engine.py:144`
- **Purpose:** Master browser orchestrator → ~25 sub-runtimes (streaming/identity/adaptive/
  distributed/application/causality/semantic/workflow/sync/evolution/live/memory/execution/
  reconstruction); ~60-key dict incl. `browser_ir, *_ir, *_persisted,
  global_runtime_fingerprint`.
- **Det.:** 🟡 deterministic **except** `render_page` (Playwright, line 319) — short-circuits
  `{"available":False}` when Playwright absent (line 331). Everything downstream of
  `runtime["html"]` is pure but html.parser-bound.
- **Hash:** `kaalka-payload` + `compute_global_runtime_fingerprint` (certified, in Java).
- **G/M/Rp/Rc:** all four (build_runtime_graph, memory stores, replay, reconstruction).

### `extract_infinite_scroll`  — Class D, BLOCKED (live browser source), transform portable
- **Path:** `core/interaction/infinite_scroll_engine.py:26`
- **Purpose:** Scroll until DOM hash stable (2 rounds) up to `MAX_SCROLLS=100`; record
  per-scroll `dom_hash`.
- **In:** `page`  **Out:** `{scrolls, chunks:[{scroll,dom_hash}], stopped_on_stable_dom,
  bounded}`.
- **Det.:** 🟡 transform deterministic over a fixture page (`compute_kaalka_hash`); live
  driver is `page.evaluate(scrollTo)` (line 35).  **Hash:** `stable`.

### `capture_dom_mutations`  — Class D, BLOCKED (source), transform portable
- **Path:** `core/streaming/dom_mutation_stream_engine.py:11`
- **Purpose:** Map `page._test_dom_mutations` → normalized stream events + DOM hash.
- **Out:** `{mutations, events, dom_hash, bounded}`.  **Det.:** 🟡 pure map over snapshot;
  live source = `MutationObserver`.  **Hash:** `stable`.

### `capture_websocket_frames`  — Class D, BLOCKED (source), transform portable
- **Path:** `core/streaming/websocket_runtime_engine.py:40` (+ `track_websocket_connections:14`)
- **Out:** `{events, bounded}` / `{connections, bounded}`.  **Det.:** 🟡 pure map+sort over
  snapshot; live source = WebSocket.  **Hash:** `stable`.

### `replay_interactions`  — Class A (output), READY-output  *(manifest Partial)*
- **Path:** `core/interaction/interaction_replay_engine.py:42`
- **Purpose:** Replay an interaction log against a page; record a normalized replay log
  (cap `MAX_REPLAY_ACTIONS=1000`).
- **Out:** `{replay:[{step,action,replayed}], bounded}` — deterministic regardless of page
  (handlers mutate the page but their effects are not in the output).

### `run_autonomous_extraction`  — Class A core, PARTIAL
- **Path:** `core/distributed_extraction/autonomous_extraction_engine.py:14`
- **Purpose:** Distributed worker/queue scheduler + checkpointing over `tasks` dicts;
  optional fan-out (native/causal/semantic/workflow/sync/evolution/live/memory/execution/
  reconstruction).
- **Det.:** ✅ base scheduler pure over `tasks`/`workers`/`checkpoint`; only the optional
  `native_extraction=True` branch (line 87) pulls Class-E `extract_native`.
- **Hash:** `stable` (encrypted checkpoint store).  **G/M/Rp/Rc:** graph + checkpoint persistence.

### `run_live_runtime`  — Class A, READY  *(manifest Partial)*
- **Path:** `core/connectors/live_runtime_orchestrator.py:24`
- **Purpose:** Aggregate the already-ported connector-runtime family (database/api/streams/
  filesystem/containers/kubernetes/cicd/telemetry/ide) → topology graph + memory + IR.
- **Det.:** ✅ fully pure over `snapshot` (no sockets).  **Out:** 15-key dict incl. `graph,
  sync_state, memory, replay, live_ir, bounded`.  **Hash:** `stable`.

### `run_canonical_pipeline`  — mixed, PARTIAL
- **Path:** `core/kernel/runtime_pipeline.py:37`
- **Purpose:** `UniversalInput → ingestion → kind detection → extract → kernel phases →
  unified graph + deterministic hash`.
- **Det.:** 🟡 deterministic for `document`/`repository`/`text`/`multimodal` kinds; `web`
  kind → `extract_web` (browser). Kernel/graph/`_hash_payload`
  (`sha256(json.dumps(sort_keys=True))`, line 15) deterministic.
- **Hash:** `sha256`.  **G/M/Rp/Rc:** graph (unified runtime graph) + kernel.

### `extract_native`, `run_native_cognition`  — Class E, DEFERRED (permanent)
- **Path:** `core/native/native_runtime_orchestrator.py:207` / `:80`
- **Purpose:** Native desktop/electron/terminal/vm/remote extraction & cognition over a
  snapshot.
- **Det.:** ❌ core pure over `snapshot`, **but** `run_native_cognition` branches on
  `sys.platform` (lines 94–108: `windows_uia`/`macos_ax`/`linux_atspi`) and on
  `runtime=="electron"` → `extract_electron_cdp` (line 124). Output is host-dependent →
  cannot be parity-proven across hosts.  **Hash:** `stable`.

---

## B. Internal (non-manifest) functions on the extraction paths

| Function | Path | Det. | Notes |
| --- | --- | --- | --- |
| `extract_archive` | `core/archive/archive_extraction_engine.py:10` | ✅ | stdlib `zipfile.namelist()` (archive order, sliced) → Java `java.util.zip` |
| `analyze_document` | `core/documents/document_intelligence.py:9` | ✅ | 3 pure text engines (section/structure/reference) |
| `compile_media_ir` | `core/ir/media_ir.py:6` | ✅ | trivial `{"ir":"media","content":payload}` |
| `compile_document_runtime_ir` | `core/ir/document_runtime_ir.py` | ✅ | unhashed aggregate IR |
| `extract_html` | `core/extract/html_extractor.py:7` | ✅(parser-bound) | **bs4/lxml** — `get_text(" ",strip=True)`, `sorted({hrefs})`, `pre`/`code` blocks, title |
| `safe_html_text` | `core/security/safe_parser.py:8` | ✅(parser-bound) | **bs4/lxml** — strip script/style → text |
| `enrich_extraction` | `core/extract/enrichment_engine.py` | ✅(444 lines) | the multi-session bulk; `dumps_deterministic` + `fingerprint_v3` |
| `normalize_output` / `_sort_value` | `core/normalize/normalize_output.py` | ✅ | recursive sort via `json.dumps(sort_keys=True)` key; NFC; int-float coercion |
| `dumps_deterministic` / `_stable` | `core/serialize/deterministic_serializer.py` | ✅ | integral-float→int before `.15g` (explicit cross-lang contract) — **new primitive** |
| `fingerprint_v3` / `kaalka_encrypt_bytes` | `core/crypto/kaalka_engine.py` | ✅ | XOR/position cipher — **new primitive**, ≠ `compute_kaalka_hash` |
| `fetch_raw` | `core/fetch/raw_fetcher.py:8` | ✅ | wraps text, no network |
| `fetch_sync`/`fetch_async` | `core/fetch/http_fetcher.py` | ❌ | `requests`/`httpx`, retries on 429 |
| `groq_complete` | `core/llm/groq_adapter.py` | ❌ | `os.getenv(GROQ_API_KEY)` + live API (temp 0 but external) |
| `is_safe_url` | `core/security/url_validator.py` | ✅ | SSRF/scheme/private-IP check (`urllib.parse`, `ipaddress`) |
| `extract_pdf_text` | `core/files/pdf_extraction_engine.py` | ❌ | **pypdf** — version-unstable text layout |
| `extract_docx_text` | `core/files/docx_extraction_engine.py` | 🟡 | **python-docx** — lib-fixed only |
| `extract_html_file` | `core/files/html_file_extraction_engine.py` | ✅(parser-bound) | **bs4/html.parser** ×3 + `compile_browser_ir` (`kaalka-payload`) |

---

## C. Counts

- **READY now (JDK-only, parity-provable):** 5 public (`extract_document_runtime`,
  `compile_document`, `extract_paginated_content`, `heal_selector`, `ingest_input`) +
  `run_live_runtime` + cores of `run_autonomous_extraction`/`replay_interactions` +
  3 internal (`extract_archive`, `analyze_document`, `compile_media_ir`).
- **READY-with-harness:** 1 (`extract_repository`).
- **BLOCKED on Soup engine:** 8 public + 2 transform-cores.
- **BLOCKED on network/browser:** 6 public.
- **DEFERRED permanent:** 2 public (`extract_native`, `run_native_cognition`) + 3 internal
  binary-parser boundaries (pdf/docx/OCR).
