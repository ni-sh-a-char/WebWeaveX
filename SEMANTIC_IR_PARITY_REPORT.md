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
| A.2 | non-evidence leaves: `core.semantic` pressure ×10, `core.ir._base` ×3, `core.graph` ×3, `core.repository` ×5, `core.ast` ×3 | 24 | Python ≡ JS ≡ Dart, 54 fixtures (66/66 incl. A.1, hash + deep equality) | ✅ proven |
| A.3 b1 | `core.evidence` trivial leaves (record-shaped bool/count/round engines) | 60 | Python ≡ JS ≡ Dart, 119 fixtures (185/185 cumulative, hash + deep equality) | ✅ proven |
| A.3 b2 | `core.evidence` leaves: recursive/semantic/unsupported families (incl. sorted/set/round + deep-equality sites) | 57 | Python ≡ JS ≡ Dart, 113 fixtures (298/298 cumulative, hash + deep equality) | ✅ proven |
| A.3 b3 | `core.evidence` medium leaves: confidence caps, contradiction lattice, evidence algebra/weighting, explainability, lineage/provenance/traceability, noninference, instability | 24 | Python ≡ JS ≡ Dart, 51 fixtures (349/349 cumulative, hash + deep equality) | ✅ proven |
| A.3 b4… | remaining `core.evidence` public leaves (the semantic_* heavy cluster: confidence/conservatism/consistency/decay/drift/entropy/fragility/honesty/incompleteness/inference/instability/justification/limits/overreach/plurality/proof/refusal/self-limitation/stability + uncertainty/visibility/escalation) | 0 / 27 | — | pending |
| — | 13 private leaf helpers (`_depth`×4, `_record`×3, `_suppression_record`×2, `_lineage_depth`, `_closure_record`, `_continuation_record`, `_stabilization_record`) | deferred | proven through their module's public parent (only callers) | deferred |
| B–O | higher layers (evidence integrity, semantic IR assembly, IR dispatchers) | 0 | — | pending |

Phase-A leaves proven: **170 / 212** (plus 2 reclassified below; 13 privates fold into their parents' phases — several share the name `_depth`/`_record` across modules, which the fn-name-keyed harness can't address directly).

## A.1 — document-parser leaves (proven)

Ported to `lib/src/semantic_ir/document_parser.dart`:

| Function | Python source | Fixtures | Result |
|----------|---------------|---------:|--------|
| `extract_rhetorical_structure` | `core.documents.rhetorical_structure_engine` | 4 | ✅ ALL3 |
| `assign_semantic_roles` | `core.documents.semantic_role_engine` | 2 | ✅ ALL3 |
| `extract_headings` | `core.documents.heading_engine` | 2 | ✅ ALL3 |
| `reconstruct_argument_dependencies` | `core.documents.argument_dependency_engine` | 2 | ✅ ALL3 |
| `resolve_coreferences` | `core.documents.coreference_resolution_engine` | 2 | ✅ ALL3 |

## A.2 — non-evidence leaves (proven)

Ported to `lib/src/semantic_ir/{pressure_engines,ir_base,graph_engines,repository_engines,ast_engines}.dart`
over a Python-semantics helper layer `lib/src/semantic_ir/py_compat.dart`
(`pythonRound` — exact CPython round-half-to-even via BigInt decomposition of the
binary double; `pyToStr`/`pyFloatStr` — Python `str()`/float repr; `pyTruthy`;
`pyGet` — missing-key vs explicit-null; `pyStableSortedBy` — Python's stable sort).

| Group | Functions | Fixtures |
|-------|-----------|---------:|
| `core.semantic.*_pressure_engine` | `compute_ambiguity_pressure`, `compute_contradiction_pressure`, `compute_evidence_boundary_pressure`, `compute_evidence_decay_pressure`, `compute_recursive_boundary_pressure`, `compute_recursive_convergence_pressure`, `compute_recursive_dependency_pressure`, `compute_semantic_boundary_pressure`, `compute_truth_boundary_pressure`, `compute_uncertainty_pressure` | 23 |
| `core.ir._base` | `empty_confidence`, `empty_lineage`, `merge_evidence` | 5 |
| `core.graph` | `model_graph_entropy`, `detect_cycles`, `prove_topology` | 8 |
| `core.repository` | `reason_api_surface`, `reconstruct_execution_flow`, `detect_infra_signals`, `resolve_runtime_dependencies`, `infer_service_interactions` | 12 |
| `core.ast` | `build_control_flow_graph`, `reconstruct_execution_paths`, `resolve_symbols` | 6 |

- **Proof:** all 66 fixtures (12 A.1 + 54 A.2) pass `validation/semantic_ir/compare_results.py`
  with `hash(Python) == hash(JS) == hash(Dart)` **and** deep output equality, executed against
  Python 2.0.1 (`origin/python`), the JS engine (`origin/javascript`), and this Dart tree.
- Vectors: `validation/parity/semantic_ir_a2_vectors.json` (54, from executed Python).
- Test: `test/parity/semantic_ir_a2_test.dart` (+60 tests → 931 total, all passing).
- Float determinism proven by execution: ties-to-even rounding (`0.4 + 5*0.06 → 0.7`,
  `3*0.15 → 0.45`), unrounded float tails (`3 cycles * 0.2 → 0.6000000000000001`),
  integral-float formatting (`0.0`), Python `str()` of mixed types (`1`, `True`).

## A.3 batch 1 — evidence trivial leaves (proven)

60 record-shaped `core.evidence` leaf engines ported to
`lib/src/semantic_ir/evidence_leaves.dart` (authority/autonomy/causal/cognitive/
confidence-echo/continuity/epistemic-openness/evidence-decay/explanatory×8/
inference-refusal/interpretive×8/ontology×12/plurality/recursive×11/stability/
topology×2/truth/worldview×4). Notables proven bit-exact by execution:
`detect_confidence_echo`/`detect_recursive_confidence_echo` (float average +
Python-rounded collapse), `model_explanatory_diversity` (`k in str(evidence)` —
substring of the Python list repr, via `pyToStr`), `refuse_unsupported_continuity`
(null `boundary_failures` from missing keys), `model_worldview_variance`
(ties-to-even rounding of `0.2/0.15` accumulations).

- Vectors: `validation/parity/semantic_ir_a3_vectors.json` (119, from executed Python).
- Test: `test/parity/semantic_ir_a3_test.dart` (+123 tests → 1054 total, all passing).
- Cumulative proof: **185/185 fixtures** pass 3-way hash + deep equality.

## A.3 batch 2 — evidence leaves, recursive/semantic/unsupported (proven)

57 leaf engines ported to `lib/src/semantic_ir/evidence_leaves_2.dart`. Notables
proven bit-exact by execution: `detect_semantic_self_reinforcement` (Python's
structural `reconciled == inferred`, via new `pyDeepEq` with numeric cross-type
equality), `measure_semantic_momentum` (true division `inferred/max(1,evidence)`),
`model_semantic_alternatives` (sorted union of dict keys, observed-priority),
`refuse_recursive_stabilization` (nested `.get(...,{}).get("type")` null chains),
`terminate_semantic_chain`/`terminate_recursive_stabilization` (truthy-filtered
sorted sets), `expose_ambiguity_visibility`/`preserve_recursive_uncertainty`
(`sorted(set(str(x)))`).

- Vectors: `validation/parity/semantic_ir_a3b_vectors.json` (113, from executed Python).
- Test: `test/parity/semantic_ir_a3b_test.dart` (+117 tests → 1171 total, all passing).
- Cumulative proof: **298/298 fixtures** pass 3-way hash + deep equality.

## A.3 batch 3 — evidence medium leaves (proven)

24 engines ported to `lib/src/semantic_ir/evidence_leaves_3.dart`. Determinism
sites proven bit-exact by execution: `apply_confidence_caps` (stacked rounded
penalties, `float()` cap coercion, floor at 0.0, float-formatted f-strings),
`combine_evidence`/`weight_evidence_calculus` (Python's empty `sum()` stays
**int 0** — payload `0` not `0.0`), `build_contradiction_lattice` (stringified
pair tuples in lexicographic tuple order), `terminate_inference_chain`
(`stop_at` is the pre-sort first element), `model_noninference` /
`detect_speculative_coherence` (structural `!=` via `pyDeepEq`),
`build_explainability` (eager nested-get fallbacks, `{}`-is-falsy language
default), `build_lineage` (per-stage `step_{idx}` defaults, list-typed guards).

- Vectors: `validation/parity/semantic_ir_a3c_vectors.json` (51, from executed Python).
- Test: `test/parity/semantic_ir_a3c_test.dart` (+56 tests → 1227 total, all passing).
- Cumulative proof: **349/349 fixtures** pass 3-way hash + deep equality.

## Plan corrections (recomputed from source, rule 10)

1. **`parse_source` is NOT a Phase-A leaf.** `core.parsers.parser_registry.parse_source`
   delegates to `ParserRegistry.parse` (a `@staticmethod`), which fans out into the whole
   `core.parsers.*` subsystem (`parse_ast`, `build_call_graph`, `resolve_imports`,
   `resolve_dependencies`, `resolve_runtime`, `resolve_frameworks`, `resolve_api_surface`,
   `build_semantic_graph`, `normalize_parser_output`, `require_parser_evidence`, …).
   `tools/gen_semantic_ir_phaseplan.py` resolves call edges via module-level functions only,
   so the static-method edge was invisible and the closure under-counts. `parse_source`
   is reclassified out of Phase A; its true closure (the parser subsystem) must be mapped
   before the phases that consume it (`model_execution_dependencies`,
   `analyze_runtime_execution`, `build_service_runtime_graph`).
2. **`core.ast.python_ast_engine._node` deferred to the `parse_python_ast` phase.** Its
   input is a live `ast.AST` node (not JSON-fixturable in isolation); it will be proven
   through `parse_python_ast(code: str)` end-to-end.

## Finding — JS-branch canonical hash divergence (discovered by execution)

The JS branch's `computeKaalkaHash` does **not** implement Python's canonical
`compute_kaalka_hash = sha256(stable_serialize(value))` for float-typed outputs of
py2ts-generated engines:

- `PyFloat` boxes are plain objects to its `stableSortKeys`, so they hash as `{"v":0.24}`
  instead of `0.24` (probed: `compute_ambiguity_pressure(["a","b"])` → Python
  `7ed6fc90…` vs JS `e53b2151…` despite identical outputs).
- Its serializer (`fast-json-stable-stringify`) renders integral floats JS-style (`0`)
  where Python emits `0.0`.

The A.1/executable harnesses never hit this (no float-typed outputs). The semantic-IR
harness (`validation/semantic_ir/run_js.mjs`) therefore computes the JS hash with
`pyStableHash` — the canonical Python `stable_serialize` payload definition applied to
the JS engine's typed output via the engine's own Python-faithful serializer
(`pyCompat.jsonDumps`, `PyFloat → "0.0"`). Dart's `computeDeterministicHash` matches the
canonical definition as-is. This is a JS-branch bug to fix on `origin/javascript`
(out of scope for the dart branch); it does not affect Python ≡ Dart parity.

## Promotion status

**No public API promoted yet** — `compile_document`, `query_documents`, `compile_repository`,
`query_repository`, `query_semantics`, `reason_semantically` remain **Partial** until their full
closure (including the 2776-line `core.evidence` engine) is executable-proven. Per protocol: no
promotion without end-to-end executable proof; no approximation. State unchanged: 94/26/8/0.

## Next

A.3 batch 4 (final Phase-A batch): the 27 remaining `core.evidence` public leaves —
the semantic_* heavy cluster (`score_semantic_confidence` 37L,
`apply_semantic_conservatism` 29L, `model_fragility` 35L, `detect_semantic_drift`,
`model_semantic_stability`, `model_uncertainty`, `infer_from_evidence`,
`build_justification`, `prove_semantic_claim`, `refuse_unsupported_conclusions`,
`apply_semantic_self_limitation`, `expose_uncertainty_visibility`,
`block_unsupported_confidence_escalation`, …). The 13 private leaf helpers prove
through their parents; then ascend layers B→O until the 6 dispatchers close with
executable parity.
