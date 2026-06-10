# SEMANTIC_IR_DEPENDENCY_MAP.md

> **Recomputed from `origin/python` 2.0.1 source** (function-level closure, not module-level) by `tools/gen_semantic_ir_map.py`. The Final Completion Protocol's prior "~628-line" estimate was wrong — corrected here.

## Headline scope (closure of all 6 Category-A APIs)

- **Functions: 282**
- **Modules: 266**
- **Total lines: 3611**

## Lines by package

| Package | Lines |
|---------|------:|
| `core.evidence` | 2776 |
| `core.documents` | 237 |
| `core.repository` | 189 |
| `core.ast` | 149 |
| `core.ir` | 94 |
| `core.graph` | 75 |
| `core.semantic` | 74 |
| `core.parsers` | 7 |
| `core.query` | 6 |
| `core.reasoning` | 4 |

## Dominant dependency

`core.evidence` (the epistemic integrity / provenance / confidence / explainability / traceability engine) is **2776 lines** — the shared gate for every one of the 6 APIs (each public dispatcher has at least one path through it).

## Determinism rules to preserve (bit-for-bit)

| Construct | Occurrences in closure |
|-----------|----------------------:|
| `round` | 123 |
| `sorted` | 100 |
| `set(` | 89 |
| `sha256` | 0 |
| `json.dumps` | 0 |
| `re.` | 35 |

Float rounding is `round(x, 3)`; sets are normalized via `sorted(set(...))`; hashing is sha256 over `json.dumps(..., sort_keys=True)`. Every one of these must match Python exactly for hash parity.

## Top modules by line count

| Module | Lines |
|--------|------:|
| `core.evidence.recursive_reality_integrity_engine` | 85 |
| `core.evidence.civilizational_epistemic_openness_engine` | 84 |
| `core.evidence.reality_alignment_engine` | 84 |
| `core.evidence.recursive_epistemic_sovereignty_engine` | 81 |
| `core.evidence.cognitive_humility_engine` | 75 |
| `core.evidence.truth_preservation_engine` | 74 |
| `core.evidence.cognitive_anti_capture_engine` | 74 |
| `core.evidence.epistemic_civilization_stability_engine` | 68 |
| `core.ast.python_ast_engine` | 66 |
| `core.evidence.cognitive_integrity_engine` | 61 |
| `core.evidence.semantic_integrity_engine` | 59 |
| `core.evidence.semantic_restraint_engine` | 59 |
| `core.evidence.speculative_inference_engine` | 54 |
| `core.evidence.epistemic_evidence_engine` | 51 |
| `core.ir.repository_ir` | 50 |
| `core.evidence.formal_semantic_foundation_engine` | 43 |
| `core.evidence.grounding_engine` | 40 |
| `core.evidence.confidence_degradation_engine` | 38 |
| `core.evidence.confidence_collapse_engine` | 38 |
| `core.ir.document_ir` | 37 |
| `core.evidence.semantic_confidence_engine` | 37 |
| `core.graph.semantic_cycle_analysis_engine` | 37 |
| `core.evidence.epistemic_confidence_engine` | 36 |
| `core.evidence.reality_bounded_confidence_engine` | 36 |
| `core.evidence.semantic_fragility_engine` | 35 |
| `core.evidence.recursive_confidence_decay_engine` | 35 |
| `core.evidence.unsupported_continuity_engine` | 34 |
| `core.documents.argument_dependency_engine` | 33 |
| `core.evidence.explainability_engine` | 32 |
| `core.evidence.semantic_conservatism_engine` | 29 |
| `core.evidence.confidence_cap_engine` | 27 |
| `core.evidence.unsupported_stabilization_engine` | 27 |
| `core.evidence.recursive_semantic_closure_engine` | 26 |
| `core.ast.control_flow_engine` | 26 |
| `core.repository.runtime_dependency_engine` | 26 |
| `core.evidence.incompleteness_engine` | 24 |
| `core.evidence.semantic_justification_engine` | 24 |
| `core.documents.tutorial_reasoning_engine` | 24 |
| `core.evidence.noninference_engine` | 23 |
| `core.evidence.semantic_stability_engine` | 23 |

## Assessment

The 6 APIs are confirmed **Category A** (pure, deterministic, no BeautifulSoup/AST-lib/NLP/network/live-runtime). However, the recomputed closure is **3611 lines across 266 modules**, dominated by a **2776-line epistemic `core.evidence` engine** with bit-exact float-rounding, sorted-set, and sha256/json determinism requirements. A faithful canonical port (no approximations — protocol rule) is a large, dedicated effort. Porting proceeds phase-by-phase with executable Python ≡ JavaScript ≡ Dart proof per phase; no API is promoted without that proof.
