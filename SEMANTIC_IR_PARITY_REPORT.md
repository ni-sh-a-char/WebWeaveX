# SEMANTIC_IR_PARITY_REPORT.md

> Living progress report for the Category-A semantic-IR port (the 6 doc/repo/semantic
> Partial APIs). Plan: `SEMANTIC_IR_PHASE_PLAN.md` · Closure map: `SEMANTIC_IR_DEPENDENCY_MAP.md`.
> Every entry below is backed by **executed** Python ≡ JavaScript ≡ Dart parity.

## Closure (recomputed from source)

- **292 functions · 3677 lines · 15 topological phases.**
- Dominated by `core.evidence` (epistemic engine, 2776 lines) — shared by all 6 APIs.
- The 6 public APIs promote to Complete **only** when the full closure is executable-proven.

## Phase progress

| Phase | Scope | Functions ported | Proof | Status |
|-------|-------|-----------------:|-------|--------|
| A.1 | `core.documents.*` parser leaves | 5 | Python ≡ JS ≡ Dart, 12 fixtures | ✅ proven |
| A.2…A.n | remaining Phase-A leaves (incl. `core.evidence` leaf bundlers) | 0 / ~207 | — | pending |
| B–O | higher layers (evidence integrity, semantic IR assembly, IR dispatchers) | 0 | — | pending |

## A.1 — document-parser leaves (proven)

Ported to `lib/src/semantic_ir/document_parser.dart`, proven by executing all three
implementations on shared fixtures (`validation/semantic_ir/`):

| Function | Python source | Fixtures | Result |
|----------|---------------|---------:|--------|
| `extract_rhetorical_structure` | `core.documents.rhetorical_structure_engine` | 4 | ✅ ALL3 |
| `assign_semantic_roles` | `core.documents.semantic_role_engine` | 2 | ✅ ALL3 |
| `extract_headings` | `core.documents.heading_engine` | 2 | ✅ ALL3 |
| `reconstruct_argument_dependencies` | `core.documents.argument_dependency_engine` | 2 | ✅ ALL3 |
| `resolve_coreferences` | `core.documents.coreference_resolution_engine` | 2 | ✅ ALL3 |

- Vectors: `validation/parity/semantic_ir_document_parser_vectors.json` (12, from executed Python).
- Test: `test/parity/semantic_ir_document_parser_test.dart`.
- Harness: `validation/semantic_ir/run_python.py` · `run_js.mjs` · `run_dart.dart`.

## Promotion status

**No public API promoted yet** — `compile_document`, `query_documents`, `compile_repository`,
`query_repository`, `query_semantics`, `reason_semantically` remain **Partial** until their full
closure (including the 2776-line `core.evidence` engine) is executable-proven. Per protocol: no
promotion without end-to-end executable proof; no approximation.

## Next

Continue Phase A leaf-by-leaf (document → repository → AST → the `core.evidence` leaf bundlers),
each ported and proven via the 3-language harness, then ascend the topological layers B→O until the
6 dispatchers close with executable parity.
