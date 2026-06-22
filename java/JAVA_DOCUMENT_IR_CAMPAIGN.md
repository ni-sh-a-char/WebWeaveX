# JAVA_DOCUMENT_IR_CAMPAIGN

**Tier-B1 campaign (S22) — executed.** `query_documents` certified byte-exact. Canon `9625f4a`.

## Dependency graph (runtime, not import closure)

`query_documents` (`core.query.document_query_engine`) → `compile_document_ir`
(`core.ir.document_ir`) → `build_document_semantic_ir` (`core.documents`), which fans to 6 engines,
transitively **21 pure document modules / ~417 lines**:

```
build_document_semantic_ir
├ parse_rhetorical_structure ─ extract_rhetorical_structure, assign_semantic_roles
├ build_argument_dependencies ─ reconstruct_argument_dependencies
├ model_concept_progression ─ model_semantic_transitions ─ model_concept_transitions ─
│   parse_semantic_discourse ─ build_argument_graph
├ infer_tutorial_prerequisites ─ analyze_instructional_semantics ─ extract_instructional_flow
│   └ reconstruct_tutorial_dependencies ─ extract_tutorial_flow ─ extract_sections ─ extract_headings
│       └ (structure_cognition)              └ (structure_cognition)
├ build_coreference_graph ─ resolve_coreferences
└ build_document_dependency_graph ─ extract_instructional_flow, model_concept_transitions
```

## The certification frontier (the key finding)

The two tutorial engines call `core.evidence.structure_cognition`, whose import closure is the
**216-module / 4496-line epistemic engine**. Naively this looks like a 5000-line wall.

**But the document path only ever reads back the passthrough `observed/inferred/reconciled`
fields** (`legacy.get("reconciled")`). **Empirically verified:** `query_documents` output contains
ZERO epistemic-computed fields (no `uncertainty`/`entropy`/`epistemic_state`/`confidence_basis`/…).
The entire epistemic engine is computed then **discarded** on this path.

→ The minimum certifiable subset is **the 21 pure document engines + a passthrough
`structure_cognition`** (returns `{observed, inferred, reconciled}`). The 4496-line epistemic
engine is **not needed** for `query_documents` byte-exactness.

## Result

`io.webweavex.documents.DocumentSemanticIr` ports all 21 engines + `compile_document_ir` +
`query_documents` + the passthrough `structure_cognition`. Faithful Python `str.splitlines()`,
`re.match`/`findall` semantics (MULTILINE/DOTALL/IGNORECASE), `sorted(set(...))`. **137/137 vectors
byte-exact** (query_documents + 18 engine sections + reconstruct_argument_dependencies × 7–4 docs).
Zero new substrate.

## Forward path to query_semantics / reason_semantically

- **`query_semantics`** dispatches by `query_type`: `graph`→`query_graph` (PROVEN), `knowledge`→
  `query_knowledge` (PROVEN), `document`→`query_documents` (**now PROVEN, S22**), `repository`→
  `core.query.query_repository`. So query_semantics needs only the **repository** engine + the
  small `compile_semantic_query_ir` (17 L) to be fully certifiable. **Next target — high ROI.**
- **`reason_semantically`** likely shares the same passthrough property over `structure_cognition`;
  re-run the empirical epistemic-field check before porting (the S22 method generalizes).

## Lesson

The "port 6500 lines" estimate was import-closure noise. The **certification frontier** is found by
(1) tracing the *runtime* call graph and (2) empirically checking which computed fields actually
reach the output. Here it collapsed 5000 lines → ~450.
