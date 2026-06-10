# PARTIAL_API_AUDIT.md

> Audit of every API classified **Partial** (34) on the `dart` branch, 2026-06-10.
> **Phase 5 update:** `extract_database_runtime` and `extract_kubernetes_runtime` were
> re-implemented to **executable parity** (Python ≡ JavaScript ≡ Dart) and promoted to
> Complete — see `EXECUTABLE_PARITY_MATRIX.md`. The 3 remaining Group-1 contract-divergent
> APIs were proven divergent **by execution** (Dart cannot run them under the current contract).
> Portability key: **A** = can be ported faithfully (full parity feasible) · **B** = bounded
> implementation is the ceiling · **C** = needs external runtime. Effort is rough engineering
> size. Source of truth: `origin/python` 2.0.1 vs `lib/`.

## Summary

| Group | Count | Portability |
|-------|------:|-------------|
| Downgraded by Proof Coverage Audit (contract/output divergence) | 9 | A/B |
| Native Dart ports with a bounded edge | 3 | B (largely done) |
| NLP/AST IR compilers | 2 | B/C |
| Semantic/query document·repository sub-paths | 5 | B |
| Bounded network/browser extraction | 15 | B |

---

## Group 1 — Downgraded by the Proof Coverage Audit (9 remaining)

These were `Complete` by name-match but had **only a determinism/structural test** — no
cross-language vector, deep-equality, or roundtrip — and the Dart contract/output diverges from
Python. `extract_database_runtime` and `extract_kubernetes_runtime` have since been **re-implemented
to executable parity and promoted to Complete** (Phase 5). The remaining 9:

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `query_runtime_graph` | Dart returns a typed `RuntimeGraph` filtered by `nodeType`; Python takes/returns `dict`s `(graph, query)` | **A** | Medium | Public Dart signature change; dict-query variant + Python-aligned vector |
| `reconstruct_runtime` | Dart reconstructs from one `extraction` envelope → `{runtime_id, graph, memory, browser}`; Python composes from separate IRs `(semantic_ir, workflow_ir, …)` | **A** | Medium–High | New IR-composition variant + vectors; signature divergence |
| `compute_global_runtime_fingerprint` | Dart hashes a Dart-specific `{pipeline_hash, graph, bounded}`; Python uses a different multi-input formula | **A** | Medium | Port Python's exact formula; signature `(envelope, RuntimeGraph)` vs 6-arg |
| `run_live_runtime` | Dart performs **live, non-deterministic filesystem listing** + reduced signature `(config)` vs Python `(config, snapshot, memory, tick)` | **B** | Medium | Live FS is non-deterministic; only a snapshot-driven path is provable |
| `build_browser_identity` | **Executably divergent** (`EXECUTABLE_PARITY_MATRIX.md`): Python `(profile_id)` runs a ~10-helper profile-generation subsystem + data tables; Dart `(captured: Map)` cannot run it | **A** | **High** | Public-contract change `(Map)`→`(profile_id)` **and** porting the browser-profile subsystem (UA/platform/webgl/canvas/font/screen tables) |
| `build_runtime_memory` | **Executably divergent**: Python `(runtime_history, lineage, semantic_relations)`; Dart `(RuntimeGraph)` — Dart cannot execute Python's input | **A** | Medium | Public-contract change to the 3-list signature; logic is portable (sha256 id, sorted histories, stable_memory_hash) |
| `query_runtime_memory` | **Executably divergent**: Python `(memory, query_type='semantic', term='')`; Dart `(mem, key)` | **A** | Medium | Public-contract change to `(memory, query_type, term)`; logic is portable |
| `validate_replay_equivalence` | Dart `checks` are `{name, ok}`; Python carries `{name, ok, original, replay}` hash fields from a different fingerprint formula | **A** | Medium–High | Depends on `compute_global_runtime_fingerprint` parity + richer check output |
| `get_runtime_kernel` | accessor returning a `RuntimeKernel` object; no own cross-language vector (`RuntimeKernel.compileIr` is separately proven) | **A** | Low | Add a vector asserting the returned kernel's serialized state/compileIr parity |

**Phase-5 terminal status for the 3 executably-divergent APIs:** `build_runtime_memory` and
`query_runtime_memory` are **one maintainer-approved public-contract change away** from executable
parity (the porting logic is straightforward). `build_browser_identity` additionally requires
porting Python's profile-generation subsystem. All three are **proven impossible without changing
the public Dart contract** — the mission's accepted terminal state — with the evidence captured by
execution in `EXECUTABLE_PARITY_MATRIX.md`.

## Group 2 — Native Dart ports with a documented bounded edge (3)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `heal_selector` | DOM-node strategies are full-fidelity (11 deep-equality vectors); `semantic_anchor` HTML path bounds deeply nested inline markup | **B** | Done (residual: HTML parser) | BeautifulSoup-equivalent `get_text(strip=True)` for nested HTML |
| `replay_interactions` | Returned structure is a full-fidelity pure function of the log (6 vectors); live-page `_ACTION_DISPATCH` is the bounded edge | **B** | Done | Live browser page object |
| `run_canonical_pipeline` | Deterministic kernel core proven; the full pipeline drives network/extraction phases | **B** | High | Live network + the extraction Partials below |

## Group 3 — NLP / AST IR compilers (2)

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `compile_document` | Python compiles documents to a semantic IR via an NLP pipeline; Dart has no equivalent NLP toolchain (currently an `UnsupportedError` stub) | **B/C** | Very High | No Dart NLP/AST stack matching Python's tokenizer/IR; deterministic parity would require porting the whole compiler |
| `compile_repository` | Same, over a repository/AST | **B/C** | Very High | AST extraction toolchain; deterministic IR parity |

## Group 4 — Semantic / query document·repository sub-paths (5)

Primary/result-dict paths are deterministic and tested; the **document/repository/network
sub-paths** depend on Group 3 compilers or live extraction.

| API | Classification reason | Portability | Effort | Blockers |
|-----|-----------------------|-------------|--------|----------|
| `query_repository` | Repository sub-path needs `compile_repository` | **B** | High | Group 3 |
| `query_documents` | Document sub-path needs `compile_document` | **B** | High | Group 3 |
| `query_semantics` | Semantic dispatch over compiled IR | **B** | High | Group 3 |
| `reason_semantically` | Primary path proven; document/repository dispatch bounded | **B** | High | Group 3 |
| `analyze` | Result-dict path proven; the network `extract()` fallback bounded | **B** | High | Group 5 |

## Group 5 — Bounded network / browser extraction (15)

Dart has a bounded HTTP surface; full parity requires live network fetching plus
readability/HTML-content extraction matching Python's exact output byte-for-byte.

`extract`, `extract_async`, `extract_repo`, `extract_docs`, `extract_recursive`,
`crawl`, `crawl_async`, `stream_extract`, `ingest_input`, `universal_extract`,
`extract_web`, `extract_repository`, `extract_multimodal`, `extract_document_runtime`,
`run_autonomous_extraction`.

| Attribute | Value |
|-----------|-------|
| Classification reason | bounded HTTP implementation; live fetch + Python-identical content extraction not reproduced |
| Portability | **B** |
| Effort | High (HTML readability/extraction parity is the hard part, not the HTTP) |
| Blockers | live-network determinism; matching Python's HTML→content heuristics byte-for-byte |

---

## Highest-value next conversions (Partial → Complete)

Group 1 is the most tractable: `extract_database_runtime` and `extract_kubernetes_runtime` are
**pure functions over a provided snapshot** (portability A) — porting Python's full field set and
adding deep-equality vectors would convert them to Complete with no platform dependency. The
contract-divergent trio (`query_runtime_graph`, `reconstruct_runtime`,
`compute_global_runtime_fingerprint`) need a Python-aligned variant + vectors and a decision on
public-signature changes.
