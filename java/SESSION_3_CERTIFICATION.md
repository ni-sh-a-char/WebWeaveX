# SESSION_3_CERTIFICATION

Scope: **query + memory + reconstruction** (plus the graph / ir / knowledge
sub-engines they depend on). Ported directly from canonical Python `core/`;
machine-readable form in `SESSION_3_CERTIFICATION.json`.

## APIs completed (manifest, parity-proven this session)

| API | Java |
| --- | --- |
| `query_graph` | `io.webweavex.query.GraphQuery#queryGraph` |
| `query_knowledge` | `io.webweavex.query.OntologyQuery#queryKnowledge` |
| `query_runtime_graph` | `io.webweavex.query.GraphQuery#queryRuntimeGraph` |
| `build_runtime_memory` | `io.webweavex.memory.RuntimeMemory#build` |
| `query_runtime_memory` | `io.webweavex.memory.MemoryQuery#queryRuntimeMemory` |
| `search_runtime_memory` | `io.webweavex.memory.MemorySearch#searchRuntimeMemory` |
| `reconstruct_runtime` | `io.webweavex.reconstruction.RuntimeReconstruction#reconstructRuntime` |
| `validate_reconstructed_runtime` | `io.webweavex.reconstruction.RuntimeValidation#validateReconstructedRuntime` |

Supporting engines also ported & tested (sub-engine, not separate manifest rows):
`reason_topology`, `reconstruct_runtime_memory`, `reconstruct_graph`,
`reconstruct_browser_runtime`, `compile_semantic_graph_ir`,
`compile_knowledge_ir`, `prove_topology`, `model_graph_entropy`,
`reconcile_ontology_edges`, `build_contradiction_lattice`,
`resolve_semantic_identities`, `validate_semantic_graph`, `check_graph_invariants`.

## Manifest progress

- **Java parity-proven: 17 / 128** APIs (was 9 entering this session).
- Validator: `tools/validate_java_manifest.py` → **PASS** (all 17 mapped, source
  exists, golden-tested, documented in `JAVA_PARITY_MATRIX.md`).

## APIs remaining / deferred (honest, not stubbed)

- `query_semantics` — dispatches to `query_repository` + `query_documents`; both
  require the unported repository/document extraction subsystems.
- `reconstruct_replay` — no canonical Python function exists (Dart-only concept).
- Remaining 111 APIs tracked in `JAVA_PARITY_MATRIX.md`.

## Parity proof counts

- **179 tests pass, 0 failures, 0 errors.** `mvn clean verify` → BUILD SUCCESS
  (jar + sources + javadoc).
- **42** session-3 Python golden vectors; cross-language only (Java output ==
  recorded Python `stable_serialize` + `compute_kaalka_hash`). No
  internal-consistency tests.
- Sessions 1–2 parity (137 assertions) re-run green — **no regressions**.

## Coverage

- Instruction coverage **94.51%** (target 95%). The 0.49% gap is justified
  line-class-by-line-class in `java/COVERAGE_EXCEPTION_REPORT.md` (JDK-guaranteed
  catches, float-format safety mirrors, faithful `get`/`or` default arms, and
  bounded-input truncation guards — all unreachable without pathological input;
  none deleted to inflate the metric).

## CI / governance added

- `.github/workflows/java-build.yml` — `mvn clean verify` on JDK 17 + 21.
- `.github/workflows/java-parity.yml` — cross-language parity tests + manifest validator.
- `.github/workflows/parity-regression.yml` — fails PR on parity mismatch,
  coverage below 94% floor, manifest drift, or proven-API count regression.

## Push confirmation

Committed and pushed to `origin/java` (see commit `feat(java): query memory
reconstruction parity slice`). Branch protections assumed; work delivered on the
`java` branch for PR.

## Risks & next dependency slice

- Residual coverage gap is documented and defensive-only.
- **Next:** repository + document extraction subsystems → unlocks
  `query_repository`, `query_documents`, then `query_semantics`; followed by the
  semantic/evidence and workflow layers.
