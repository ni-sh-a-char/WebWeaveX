# JAVA_SESSION_3_ANALYSIS

Mandatory pre-implementation analysis for Session 3 (query + memory +
reconstruction). All findings come from reading the **canonical Python branch**
(`core/`); the Dart branch is treated as a non-authoritative reference only
(Session 2 proved Dart public symbols can diverge from Python).

## State entering Session 3

17 → no; **9 manifest APIs** parity-proven (sessions 1–2): `compute_kaalka_hash`,
`encrypt_value`, `decrypt_value`, `UniversalInput`, `build_runtime_graph`,
`compile_unified_runtime_ir`, `compute_global_runtime_fingerprint`,
`fingerprint`, `validate_replay_equivalence`. These must not regress.

## Verification strategy (unchanged, enforced)

For every API: drive the **Python** public function (which transitively runs all
its sub-engines) over crafted inputs → record canonical `stable_serialize` +
`compute_kaalka_hash` of the output (and exact string for hash-returning fns) →
Java reconstructs inputs, recomputes, asserts byte-equality. Golden vectors come
from Python only (`tools/gen_java_parity_vectors_s3.py`). No internal-consistency
tests.

## Dependency graph (Python canon, all deterministic, no network/OS)

```
query_runtime_graph        (runtime_graph/runtime_graph_query_engine)         [leaf]
reason_topology            (graph/topology_reasoning_engine)
  ├─ prove_topology        (graph/topology_proof_engine)                      [leaf]
  └─ model_graph_entropy   (graph/graph_entropy_engine)                       [leaf, round()]
query_graph                (query/graph_query_engine)
  ├─ compile_semantic_graph_ir (ir/semantic_graph_ir)
  │    └─ prove_graph_consistency (graph/graph_consistency_prover)
  │         ├─ validate_semantic_graph (graph/semantic_graph_validator)
  │         │    ├─ check_graph_invariants (graph/graph_invariant_engine)     [leaf]
  │         │    └─ validate_semantic_edge (graph/semantic_edge_validation_engine) [leaf]
  │         └─ assess_graph_consistency (graph/graph_consistency_engine) → check_graph_invariants
  ├─ query_nodes / query_edges (agents/graph_query_engine)                    [leaf]
  └─ empty_lineage (ir/_base)                                                 [leaf]
query_knowledge            (query/ontology_query_engine)
  └─ compile_knowledge_ir  (ir/knowledge_ir)
       ├─ reconcile_ontology_edges (knowledge/ontology_reconciliation_engine)
       │    ├─ merge_with_evidence (knowledge/semantic_merge_rigor_engine)    [leaf, sorted(set)]
       │    └─ stamp_ontology_lineage (knowledge/ontology_lineage_engine)     [leaf]
       ├─ resolve_semantic_identities (knowledge/semantic_identity_resolver)
       │    └─ identity_hash (knowledge/semantic_identity_calculus)           [leaf, sha256[:16]]
       ├─ detect_ontology_conflicts (knowledge/ontology_conflict_engine)
       │    └─ build_contradiction_lattice (evidence/contradiction_lattice_engine) [leaf, round()]
       └─ empty_confidence/empty_knowledge_ir (ir/_base, ir/knowledge_ir)

build_runtime_memory       (memory/runtime_memory_engine)
  └─ stable_memory_hash    (memory/stable_memory_hash) → compute_kaalka_hash(json.dumps compact)
query_runtime_memory       (memory/runtime_query_engine)   [leaf, sorts by str(dict) → PyRepr]
search_runtime_memory      (memory/runtime_search_engine)  [leaf]

reconstruct_runtime        (reconstruction/runtime_reconstruction_engine) [json.dumps default + sha256[:32]]
reconstruct_runtime_memory (reconstruction/runtime_memory_reconstruction) [leaf]
reconstruct_graph          (graph/graph_reconstruction_engine)            [leaf, sorted(set)]
reconstruct_browser_runtime(reconstruction/browser_reconstruction_engine) [leaf]
validate_reconstructed_runtime (reconstruction/runtime_validation_engine) [leaf]
```

## Implementation order (bottom-up)

1. Helpers: `PyRepr` (Python `str(dict)`/`repr`), `PyRound` (Python `round(x,n)` half-even).
2. `io.webweavex.graph`: GraphInvariants, SemanticEdge, SemanticGraphValidator,
   GraphConsistency, TopologyProof, GraphEntropy, GraphReconstruction.
3. `io.webweavex.ir`: IrBase, SemanticGraphIr, KnowledgeIr.
4. `io.webweavex.knowledge`: OntologyReconciliation, SemanticIdentity,
   OntologyConflict, ContradictionLattice.
5. `io.webweavex.query`: GraphQuery (query_graph + query_runtime_graph + nodes/edges),
   OntologyQuery (query_knowledge), TopologyReasoning (reason_topology).
6. `io.webweavex.memory`: RuntimeMemory (+ stable hash), MemoryQuery, MemorySearch.
7. `io.webweavex.reconstruction`: RuntimeReconstruction, MemoryReconstruction,
   BrowserReconstruction, RuntimeValidation.

## Remaining APIs after this slice

Session-3 PORT-NOW closes these manifest APIs (8): `query_graph`,
`query_knowledge`, `query_runtime_graph`, `build_runtime_memory`,
`query_runtime_memory`, `search_runtime_memory`, `reconstruct_runtime`,
`validate_reconstructed_runtime`. Plus requested sub-engines `reason_topology`,
`reconstruct_runtime_memory`, `reconstruct_graph`, `reconstruct_browser_runtime`
(tracked, tested, but not separate manifest API rows).

### Deferred (NOT stubbed — honest dependency blocks)

- **`query_semantics`**: dispatches to `query_repository` + `query_documents`,
  which require the (unported) repository and document extraction subsystems.
  Will land with those layers.
- **`reconstruct_replay`**: no canonical Python function exists (Dart-only
  concept); excluded as non-canonical.

## Parity hazards catalogued

- Python `round(x, n)` is round-half-to-even on the exact value → `PyRound` via
  `BigDecimal(x).setScale(n, HALF_EVEN)` (entropy, pressure, density).
- `sorted(set(...))` → dedup then code-point sort (evidence, identities, pairs,
  graph reconstruction nodes/edges).
- `query_runtime_memory` sorts results by `str(item)` where item is a dict →
  needs faithful Python `repr` (`PyRepr`): single-quoted strings, `, `/`: `
  separators, insertion-ordered keys.
- `reconstruct_runtime` hashes `json.dumps(..., sort_keys=True)` **default**
  separators; `stable_memory_hash` uses **compact** `(",",":")`. Reuse
  `PyJson.dumpsDefaultAscii` / `dumpsCompactAscii`.
- sha256 truncations: `[:32]` (memory_id, runtime_id), `[:16]` (identity_hash).
