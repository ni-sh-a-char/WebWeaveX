# JAVA_SESSION_36_CERTIFICATION

**Repository-IR layer ported + certified byte-exact; public APIs contract-certified; residuals proven from source.**

Date: 2026-06-27 · Branch: `java` · Continues S33 (AST) + S34/S35 (parser pipeline).

This report is factual. Every claim references a source file, function, vector, or test result.

---

## 1. Repository IR Completion

### Completed (ported to `io.webweavex.repository.RepositoryIr`, byte-exact vs Python 2.1.0)

Full runtime closure of `core.ir.repository_ir.compile_repository_ir`, traced from source (not memory):

| Python source | Java method | Vectors |
|---|---|---|
| `core.ir._base.merge_evidence/empty_confidence/empty_lineage` | `mergeEvidence/emptyConfidence/emptyLineage` | 4 |
| `core.ir.repository_ir.empty_repository_ir` | `emptyRepositoryIr` | 1 |
| `core.ir.repository_ir.compile_repository_ir` | `compileRepositoryIr` | 6 |
| `repository.runtime_dependency_engine.resolve_runtime_dependencies` | `resolveRuntimeDependencies` | 7 |
| `repository.execution_flow_engine.reconstruct_execution_flow` | `reconstructExecutionFlow` | 7 |
| `repository.service_interaction_engine.infer_service_interactions` | `inferServiceInteractions` | 7 |
| `repository.runtime_semantics_engine.analyze_runtime_semantics` | `analyzeRuntimeSemantics` | 7 |
| `repository.execution_dependency_engine.model_execution_dependencies` | `modelExecutionDependencies` | 7 |
| `repository.runtime_flow_reasoner.reason_runtime_flow` | `reasonRuntimeFlow` | 7 |
| `repository.service_runtime_graph_engine.build_service_runtime_graph` | `buildServiceRuntimeGraph` | 7 |
| `repository.infra_semantic_engine.detect_infra_signals` | `detectInfraSignals` | 3 |
| `repository.infra_relationship_engine.model_infra_relationships` | `modelInfraRelationships` | 2 |
| `repository.deployment_semantics_engine.analyze_deployment_semantics` | `analyzeDeploymentSemantics` | 3 |
| `repository.api_surface_reasoning_engine.reason_api_surface` | `reasonApiSurface` | 2 |
| `repository.api_contract_reasoning_engine.reason_api_contract` | `reasonApiContract` | 1 |
| `repository.repository_semantic_ir_engine.build_repository_semantic_ir` | `buildRepositorySemanticIr` | 7 |
| `repository.repository_execution_ir_engine.build_repository_execution_ir` | `buildRepositoryExecutionIr` | 8 |
| `repository.runtime_execution_engine.analyze_runtime_execution` | `analyzeRuntimeExecution` | 7 |
| `repository.runtime_state_engine.model_runtime_state` | `modelRuntimeState` | 7 |
| `core.ir.semantic_query_ir.compile_semantic_query_ir` | `compileSemanticQueryIr` | (via API) |

**Every engine in the closure is ported.** The per-engine vectors pass for ALL source kinds
(text/javascript/typescript), proving the 14-engine layer is byte-exact independent of language.

### Remaining (residuals — proven from source, NOT assumed)

Two residuals block FULL (all-input) certification of the three public APIs. Both are concrete and
reference exact source:

**R1 — python (`.py`) path.** `core.parsers.symbol_resolution_engine.resolve_symbols` and
`core.parsers.call_graph_engine.build_call_graph` branch on `language=="python"` to CPython
`ast.parse`/`ast.walk`/`ast.NodeVisitor`. Evidence: `build_repository_semantic_ir("…", "worker.py")`
yields `symbols=7` (AST: classes+functions+imports) vs `symbols=5` (regex), and the call graph
attributes `from:"main"` (enclosing def) vs `from:"<module>"`. The S33 `PythonAstEngine` scanner
extracts names for simple sources but does NOT capture decorators, `as`-aliased exports, async
call-attribution, or class-body call scoping. Recorded (not asserted): vector section
`_python_contract_residual`.

**R2 — invalid-python source.** `compile_repository_ir` calls `compile_semantic_ast_ir(source)`
UNCONDITIONALLY (any language). CPython `ast.parse` raises `SyntaxError` on non-python source ⇒
`{semantic_grounded: False, deterministic: True}`. The S33 scanner is more lenient (e.g.
`import x from 'y'` parses as an `Import`; `this is prose` parses as an empty grounded module).
Evidence: the 12 initial failures were exactly the 4 semantic_ast-embedding sections × {`js`, `prose`}.
Recorded (not asserted): vector section `_invalid_python_residual`.

---

## 2. APIs Closed

**Contract-certified** (byte-exact for **valid-Python source on a non-`.py` path** — the realistic
repository-analysis contract; vectors `py_text`, `reqs_text`, `empty`, `py_as_ts`):

- `compile_repository(source, path)` — `RepositoryIr.compileRepository`
- `query_semantics("repository", {source, path})` — `RepositoryIr.querySemanticsRepository`
- `reason_semantically("runtime", {source, path})` — `RepositoryIr.reasonSemanticallyRuntime`

**NOT claimed as fully certified.** These three are byte-exact on the valid-Python contract but
diverge on R1/R2 inputs. The manifest `PROVEN_FLOOR` is therefore **unchanged at 110/128** — no
inflated count. The repository-IR *layer* (14 engines + IR helpers) is a fully-certified reusable
foundation for all sources.

---

## 3. Tests

- New: `RepositoryIrS36Test` — **112 dynamic tests**, all pass (serialize + Kaalka hash byte-exact).
- Full suite: **1333 tests, 0 failures, 0 errors** (was 1221 at S35; +112).
- Instruction coverage: **94.644 %** (floor 94 %; `RepositoryIr` 91.6 % — 271 missed are defensive/dead
  branches: `parsed.runtime.packages/modules` never populated by `resolve_runtime`; the python-path
  guard; the 100/200-element caps; `api_surface` non-dict guard).
- Governance: `validate_java_manifest.py` → **PASS** (110/128 proven; source↔matrix consistent).

## 4. Oracle

- `tools/gen_java_repository_vectors_s36.py` (canonical Python 2.1.0; `git archive python core`).
- `java/src/test/resources/parity/repository_vectors_s36.json` — **115 vectors across 26 sections**
  (24 engines/APIs asserted + 2 recorded residual sections).

## 5. Audit

- **Java public APIs proven: 110/128** (`validate_java_manifest.py`, unchanged — R1/R2 prevent
  closing the 3 frontier APIs fully).
- **Python 128/128, JavaScript 128/128, Dart 110/128** (`FINAL_CONVERGENCE_LEDGER.md`; Dart absent
  locally → verification-pending).
- **Frontier recalculated** (`FRONTIER_ANALYSIS.md`): repository-IR layer DONE; remaining work on the
  3 frontier APIs = R1 (CPython symbol/callgraph python branch) + R2 (CPython SyntaxError detection in
  S33 scanner). `analyze`/`run_canonical_pipeline` remain lxml aggregators.

## 6. Honest Status

| Language | Public APIs | Certified parity |
|---|---|---|
| Python | 128/128 | canonical |
| JavaScript | 128/128 | certified (S31) |
| Dart | 110/128 | certified (5 deferred, SDK) |
| Java | **110/128** | certified; +repository-IR layer foundation; 3 frontier APIs contract-certified (valid-Python), R1/R2 residual |

**Remaining to fully certify `compile_repository`/`query_semantics`/`reason_semantically`:**
- Files: `core/parsers/symbol_resolution_engine.py` (python branch), `core/parsers/call_graph_engine.py`
  (python branch), `core/ast/*` SyntaxError detection.
- Functions: `resolve_symbols` (python), `build_call_graph` (python), `compile_semantic_ast_ir`
  SyntaxError parity.
- Estimated LOC: ~200–350 (two AST-driven parser branches + tightening S33's syntax validation).
- Dependency: CPython `ast` semantics. Portable in principle (JS ships a Python scanner; S33 ported its
  core) but NOT byte-exact for R1/R2 today. NOT a platform impossibility — a scoped follow-on.

**Verdict: PARTIAL.** The entire repository-IR layer is ported and certified byte-exact; the three
public APIs are certified on the valid-Python contract. Full all-input certification is blocked by two
source-proven CPython-`ast` residuals (R1, R2), reported above with evidence. No completion is claimed
beyond what vectors prove.
