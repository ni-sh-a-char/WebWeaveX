# JAVA_EXTRACTION_DAG

**Phase 3 — extraction dependency graph & optimal implementation order.**

Built from the Python canon (`origin/python` @ `9625f4a`). Arrows mean *depends on / is
gated by*. The graph is layered by **substrate**: a node is portable only once every
substrate below it exists in Java.

---

## 1. Substrate layers (bottom = already in Java)

```
L0  JDK-only foundation .......... DONE (Sessions 1–4)
     determinism: Normalization, CanonicalJson, StableSerialize, PyFloat
     crypto:      Hashing, Kaalka (compute_kaalka_hash, compute_kaalka_hash_payload)
     ir/graph/memory/query/replay/reconstruction primitives
        │
        ├─────────────────────────────────────────────┐
        ▼                                               ▼
L1a  Pure transform substrate (NO new substrate)   L1b  NEW determinism primitives
     — needs only L0                                     (needed ONLY by Class C extract)
        │                                                  dumps_deterministic
        │                                                  fingerprint_v3 / kaalka_engine (XOR)
        ▼                                                  │
L2   Class A / B engines                                  ▼
        │                                            L3  Soup engine (HARD, multi-session)
        ▼                                                  lxml-parity   +   html.parser-parity
   READY public APIs                                       │                       │
                                                           ▼                       ▼
                                                     Class C (extract*/stream)  Class C (html_file/extract_web DOM)
                                                           │
                                                           ▼
                                                     L4  Live-I/O boundary  (network / Playwright)
                                                           Class D  — NOT parity-provable (stub-free policy)
                                                     L5  Binary/platform boundary
                                                           Class E  — DEFERRED permanent
```

---

## 2. Node graph (per API)

### Leaf nodes (depend only on L0 — implementable immediately)

```
extract_document_runtime ─▶ [core.documents.{structure,hierarchy,citation,reference,table},
                              core.knowledge.document_knowledge_graph,
                              core.presentation, core.spreadsheets,
                              core.ir.document_runtime_ir]              (all pure)
compile_document ─▶ core.ir.document_ir ─▶ core.documents.document_semantic_ir
                     ─▶ {6 discourse engines} ─▶ {~13 regex engines}
                     ─▶ core.evidence (+ core.semantic.semantic_uncertainty)  (all pure)
extract_paginated_content ─▶ core.interaction.pagination_engine            (pure, fixture page)
heal_selector ─▶ core.adaptive.selector_healing ─▶ core.adaptive.semantic_anchor
                                                    (pure; tiny html.parser edge — Risk R-7)
ingest_input ─▶ core.ingestion.universal_ingestion  (pure extension map)
extract_archive ─▶ stdlib zipfile                   (pure)
analyze_document ─▶ core.documents.document_intelligence  (pure)
compile_media_ir ─▶ core.ir.media_ir                (pure)
run_live_runtime ─▶ core.connectors.* (DONE in Java) (pure aggregation)
replay_interactions(output) ─▶ core.interaction.interaction_replay  (pure record)
```

### Intermediate nodes (need L1b and/or L3)

```
extract / extract_async / extract_docs / extract_repo
   ─▶ core.extract.pipeline._extract_core
        ─▶ extract_html  ───────────────▶ [L3 lxml Soup]
        ─▶ safe_html_text ──────────────▶ [L3 lxml Soup]
        ─▶ enrich_extraction ──▶ dumps_deterministic ─▶ [L1b]
                              └─▶ fingerprint_v3 ─────▶ [L1b]
        ─▶ (entry) fetch_sync/async ────▶ [L4 network]   (URL path only)
        ─▶ (entry) groq_complete ───────▶ [L4 LLM/env]   (llm=="groq" only)
stream_extract ─▶ extract() ─▶ [L3 lxml Soup]  (transitive — Soup-bound even on raw text)
analyze(source-mode) ─▶ extract() ─▶ [L3 lxml Soup]
extract_html_file / universal_extract(html) ─▶ [L3 html.parser Soup] + compile_browser_ir(L0 kaalka-payload)
extract_repository ─▶ core.repository.* (pure) + FILESYSTEM(L?) + path-canon harness (Risk R-2)
```

### Root nodes (need L4/L5 — not certifiable stub-free)

```
crawl / crawl_async ─▶ fetch_sync ─▶ [L4 network]
extract_recursive ─▶ crawl + extract ─▶ [L4 network] + [L3 Soup]
extract_web ─▶ render_page ─▶ [L4 Playwright] + [L3 html.parser] + L0 graph/memory/replay/fingerprint
extract_infinite_scroll / capture_dom_mutations / capture_websocket_frames
        ─▶ live source ─▶ [L4 browser]   (transform-core portable against fixtures)
run_canonical_pipeline ─▶ (kind=web) extract_web ─▶ [L4];  (kind=doc/text/repo) pure
extract_native / run_native_cognition ─▶ sys.platform probe ─▶ [L5 OS]   (permanent)
```

### Dispatcher fan-out

```
universal_extract ─▶ ingest_input ─┬─ pdf  ─▶ extract_pdf_text   [L5 pypdf]
                                    ├─ docx ─▶ extract_docx_text  [L5 python-docx]
                                    ├─ image─▶ extract_multimodal [L5 OCR]
                                    ├─ archive ─▶ extract_archive  (READY)
                                    ├─ html ─▶ extract_html_file   [L3 html.parser]
                                    ├─ repository ─▶ extract_repository (READY-harness)
                                    └─ else ─▶ {"unsupported":True}  (READY)
```

---

## 3. Critical-path observations

1. **The Class-A leaves form a closed island.** `extract_document_runtime`,
   `compile_document`, `extract_paginated_content`, `heal_selector`, `ingest_input` and
   the three internal helpers depend on **nothing above L0**. They can ship in one or two
   slices with zero new substrate — exactly the Session-4 connector pattern.

2. **The Soup engine (L3) is the single largest gate.** It blocks **8 public APIs**. It is
   itself **two** sub-projects: an **lxml-parity** engine (`extract` family) and an
   **html.parser-parity** engine (`extract_html_file`, `extract_web` DOM,
   `dom_reconstruction`, `semantic_content`). They are independent and can be sequenced.

3. **L1b is small but mandatory for Class C.** `dumps_deterministic` + `fingerprint_v3`
   are two compact, pure primitives — but they are a hard prerequisite for *any* `extract`
   output to be byte-exact (the envelope embeds the fingerprint). Build them with/just
   before the Soup engine, not before the Class-A slice (Class A never hashes).

4. **`extract_repository` (L2-B) is independent of the Soup engine** but needs a
   path-canonicalization test harness (L? — see Risk R-2). It can proceed in parallel with
   the Class-A slice if that harness is accepted by governance.

5. **Class D/E are not "later work" — they are out of the parity-certifiable set.** Their
   *transform cores* (infinite-scroll/dom-mutation/websocket map; native cognition over a
   snapshot) are portable against fixtures, but the live/platform *source* cannot be
   reproduced deterministically without a stub, which policy §5 forbids in `src/main`.

---

## 4. Optimal implementation order

| # | Slice | Gates needed | Output |
| --- | --- | --- | --- |
| **1** | **Class-A pure document/interaction family** — `extract_document_runtime`, `extract_paginated_content`, `heal_selector`, `ingest_input` (+ internal `extract_archive`, `analyze_document`, `compile_media_ir`) | L0 only | +4 public proven APIs |
| **2** | **`compile_document`** (epistemic Document IR — large pure surface, `core.evidence`) | L0 only | +1 public (may span 2 sessions) |
| **3** | **`extract_repository`** + path-canonicalization harness | L0 + harness decision | +1 public |
| **4** | **`run_live_runtime`** (aggregates the DONE connector family) | L0 + connectors (DONE) | +1 public |
| **5** | **L1b primitives** `dumps_deterministic` + `fingerprint_v3`/`kaalka_engine` | L0 | substrate (no public API yet) |
| **6** | **L3a lxml Soup engine** → `extract`/`extract_async`/`extract_docs`/`extract_repo`/`stream_extract`/`analyze` (raw-text/non-LLM path) | L0+L1b+L3a | +6 public (multi-session) |
| **7** | **L3b html.parser Soup engine** → `extract_html_file`, `universal_extract` (html), `extract_web` deterministic DOM core | L0+L3b | +1–2 public |
| **8** | **Class D transform-cores** (infinite-scroll/dom-mutation/websocket) against fixtures; **Class E** documented permanent-deferred | fixtures | governance: classify Deferred |

Items 1–4 are the **certifiable, stub-free** advances available **this arc**. Items 5–7 are
the heavy Soup-gated multi-session effort. Item 8 closes the governance ledger for the
genuinely platform/live-bound remainder.
