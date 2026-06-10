# PARTIAL_API_AUDIT.md

> **Generated from `PARITY_MANIFEST.json`** (26 Partial APIs). Each Partial has a documented bounded blocker.

| API | Blocker |
|-----|---------|
| `analyze` | result-dict path proven; the network extract() fallback is bounded |
| `compile_document` | needs an NLP/AST IR compiler (no in-process Dart toolchain) |
| `compile_repository` | needs an AST/repository IR compiler |
| `crawl` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `crawl_async` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_async` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_docs` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_document_runtime` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_multimodal` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_recursive` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_repo` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_repository` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `extract_web` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `heal_selector` | DOM-node strategies full-fidelity (vectors); semantic_anchor HTML sub-path bounds nested markup |
| `ingest_input` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `query_documents` | document sub-path needs compile_document |
| `query_repository` | repository sub-path needs compile_repository |
| `query_semantics` | semantic dispatch over compiled IR |
| `reason_semantically` | primary/dict path proven; document/repository sub-paths need the NLP/AST compilers |
| `replay_interactions` | returned structure full-fidelity (vectors); live-page action dispatch is the bounded edge |
| `run_autonomous_extraction` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `run_canonical_pipeline` | deterministic kernel core proven; full pipeline drives live network/extraction phases |
| `run_live_runtime` | performs live, non-deterministic filesystem listing; only a snapshot path is provable |
| `stream_extract` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |
| `universal_extract` | bounded HTTP surface; full parity needs live network fetch + Python-identical HTML/content extraction |

**26 Partial.** The network/extraction group (`extract*`, `crawl*`, `stream_extract`, `ingest_input`, `universal_extract`, `run_autonomous_extraction`) shares the bounded-HTTP blocker; the query/semantic group depends on the NLP/AST compilers.
