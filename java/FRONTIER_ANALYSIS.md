# FRONTIER_ANALYSIS

**Session-33c runtime frontier analysis of the AST/repository cluster — runtime closures, not import
closures. Empirically traced.** Source-derived. Directive Phases 4 & 7.

## Cluster: `query_semantics` / `reason_semantically` / `compile_repository`

All three route a branch through `compile_repository_ir(source, path)`:
```
compile_repository_ir(source, path)
├ raw = build_repository_execution_ir(source, path, files, openapi)
│  ├ base = build_repository_semantic_ir(source, path, files)
│  │    └ parsed = parse_source(source, path)        [core.parsers.parser_registry — ~13 sub-engines]
│  │    returns {language, symbols, runtime_dependencies, execution_flow, service_interactions,
│  │             parser_grounding, evidence}          ← NOTE: parsed["ast"] is NOT returned
│  ├ flow     = reason_runtime_flow(...)              [runtime_semantics + execution_dependency]
│  ├ services = build_service_runtime_graph(...)      [service_interaction]
│  ├ deploy   = analyze_deployment_semantics(files)   [infra_relationship]
│  └ api      = reason_api_contract(openapi)          [api_surface] — only if openapi_spec given
└ semantic_ast = compile_semantic_ast_ir(source)      [DONE S33 — io.webweavex.ast.*]
```

## Frontier reduction 1 — epistemic engine DISCARDED (measured)
`compile_repository_ir` output has **zero** epistemic fields (`uncertainty`/`entropy`/`epistemic`/
`observed`/`inferred`/`belief`); serialized ≈3.2 KB. The ~2776-line `core.evidence` engine is imported
(eager) but its result never reaches the observable output. **Do not port it** (Phase 7). Prior
estimate of "~3600-line epistemic port" was wrong.

## Frontier reduction 2 — `parse_ast` DFS node list DISCARDED (measured)
`core.parsers.ast_engine.parse_ast` runs a full DFS over real CPython `ast` producing
`nodes=[{id,kind}]`. But `build_repository_semantic_ir` returns only `symbols`/`dependencies`/…, **not**
`parsed["ast"]`. The DFS node list reaches the output **only** as the boolean `evidence.ast =
bool(ast_tree.nodes)`. **Do not reproduce the DFS node list** — only its non-emptiness matters.

## Frontier reduction 3 — language="text" for source-only inputs (measured)
`detect_language` keys off the **path suffix**. For `compile_repository_ir(source, path="")` (the common
contract) language = `"text"`, so `parse_ast` takes the tree-sitter branch which has no "text" grammar →
`{nodes:[], parse_error:True}`. Symbols/calls/deps then come from the parsers' **regex** engines, not a
real AST. Empirically `compile_repository_ir("import os\ndef main():\n  return 1")` →
`symbols={functions:["main"],methods:["main"],…}`, `semantic_evidence=["lang=text","parser:call_graph",
"parser:functions","symbols=1"]`, everything else empty. **The observable frontier is the regex parser
engines, not CPython AST** (except `semantic_ast`, already ported).

## Remaining port (precisely scoped, post-reduction)

| Layer | Modules | Status |
|---|---|---|
| **AST summary** (`compile_semantic_ast_ir`) | `python_ast_engine`, `semantic_ast_ir_engine`, symbol/cfg/exec-path | ✅ **DONE (S33)** — byte-exact vs CPython |
| **parser pipeline** (`parse_source`, text/regex path) | `parser_registry` + ~13: recover_syntax, parse_ast(bool), resolve_symbols, build_call_graph, resolve_imports, resolve_dependencies, resolve_runtime, resolve_frameworks, resolve_api_surface, build_semantic_graph, normalize_parser_output, require_parser_evidence, parser_budget | pending — regex/text engines, ~600 L |
| **repository engines** | ~8: repository_semantic_ir, runtime_flow_reasoner (runtime_semantics + execution_dependency), service_runtime_graph (service_interaction), deployment_semantics (infra_relationship), api_contract (api_surface), execution_flow, runtime_dependency | pending — ~400 L |
| **IR assembly** | `repository_ir` (`empty_repository_ir`/`merge_evidence`/`empty_lineage`/`empty_confidence`) + dispatch | pending — ~120 L |

**Net remaining ≈ 1120 L across ~22 small regex/text modules (NO epistemic engine, NO AST DFS).**
Once ported on top of the AST foundation, certifies `compile_repository` directly and the
`repository`/`runtime` branch of `query_semantics`/`reason_semantically`; the document/graph/knowledge/
discourse/topology branches already reuse certified Java engines (`DocumentSemanticIr` S22,
`GraphQuery`/`OntologyQuery` S3).

## Verdict
The AST cluster is **portable and bounded** (~1120 L regex/text, not the ~3600 L feared). It is a
multi-session port (Rule 4: no partial ports — each parser/repository engine ported + tested
individually as a reusable foundation, then composed). No frontier-reduction avenue remains
unexplored; nothing here is impossible. Foundation layer delivered S33; pipeline layers scoped above.
