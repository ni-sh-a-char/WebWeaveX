# PARTIAL_API_AUDIT.md

> **Generated from `PARITY_MANIFEST.json`** (26 Partial APIs). Re-audited against `origin/python` source (not report descriptions). Category: **A** = pure & portable (executable parity achievable, port pending) · **B** = bounded parity only (documented limitation) · **C** = platform-impossible (network/live runtime).

**Category split: A=6 · B=4 · C=16**

| API | Category | Blocker |
|-----|:--------:|---------|
| `analyze` | B | graph-edges path is pure (analyze_graph); the no-edges path delegates to the network extract() |
| `compile_document` | A | pure document semantic-IR (regex/line heuristics, no NLP/AST); port pending of the ~550-line document-IR subsystem |
| `compile_repository` | A | pure repository semantic-IR (no AST lib); port pending of the ~490-line repository-IR subsystem |
| `crawl` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `crawl_async` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_async` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_docs` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_document_runtime` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_multimodal` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_recursive` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_repo` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_repository` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_web` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `heal_selector` | B | DOM-node strategies full-fidelity (vectors); semantic_anchor HTML sub-path bounds nested markup vs BeautifulSoup |
| `ingest_input` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `query_documents` | A | pure; calls compile_document_ir — same document-IR subsystem port |
| `query_repository` | A | pure; calls query_repository_ir / query_repo — repository-IR subsystem port |
| `query_semantics` | A | pure dispatch (graph/knowledge paths already Complete; document/repository paths need the IR subsystems) |
| `reason_semantically` | A | pure dispatch (topology path pure; runtime/discourse paths need the IR subsystems) |
| `replay_interactions` | B | returned structure full-fidelity (vectors); live-page action dispatch is the bounded edge |
| `run_autonomous_extraction` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `run_canonical_pipeline` | C | deterministic kernel core proven; full pipeline drives live network/extraction phases |
| `run_live_runtime` | B | performs live, non-deterministic filesystem listing; only a snapshot path is provable |
| `stream_extract` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `universal_extract` | C | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |

## Category A — pure & portable (executable parity achievable)

The document/repository/semantic APIs (`compile_document`, `compile_repository`, `query_documents`, `query_repository`, `query_semantics`, `reason_semantically`) were **re-verified from source**: they use pure regex/line/graph heuristics — **no BeautifulSoup, no AST, no NLP libraries** (correcting the prior "NLP/AST compiler" label). They are gated only on porting the shared, fully-deterministic `core.documents.*` / `core.repository.*` / `core.evidence` semantic-IR subsystem (~750 pure lines). That port is the concrete remaining Category-A work; until each is executable-proven it stays Partial.

## Category B/C — bounded or platform-impossible

The network/extraction group (`extract*`, `crawl*`, `stream_extract`, `ingest_input`, `universal_extract`, `run_autonomous_extraction`, `run_canonical_pipeline`) requires live HTTP + Python-identical HTML extraction (C). `heal_selector` / `analyze` / `run_live_runtime` / `replay_interactions` are bounded (B) with documented edges.
