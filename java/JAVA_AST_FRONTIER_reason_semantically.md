# JAVA_AST_FRONTIER_reason_semantically

**AST frontier audit (Phase B3). Verdict: CONDITION-B BLOCKED — observable output requires CPython
AST semantics. Proven.** Canon `9625f4a`.

## Trace
`reason_semantically("runtime", payload)` → `reason_runtime_semantic(source, path)` → the runtime
IR embeds `parse_python_ast(source)` / parser_registry AST (`import ast; ast.parse`). Returns
`{**result, domain, deterministic}` — `result.ir` kept whole.

## Empirical proof — AST is OBSERVABLE
`reason_semantically("runtime", {"source": "def foo(a, b):\n    x = bar()\n    return x\nclass A(Base):\n    pass"})`
→ `json.dumps(output)` contains `"lineno"`, `"end_lineno"`, `"FunctionDef"` (verified). The same
CPython-AST-derived fields (`node.lineno`/`end_lineno`/`type`, `args`, `bases`) reach the output as
in `query_semantics` — see `JAVA_AST_FRONTIER_query_semantics.md` for the field-level argument.

## Frontier note (the portable part)
The other two branches are NOT AST-coupled and ARE portable: **`discourse`** (514 L,
epistemic-free, reuses the proven document-IR engines) and **`topology`** (115 L, inline epistemic
math). Only the **`runtime`** branch embeds the CPython AST. Because byte-exact parity must hold for
every `domain`, the whole API is blocked — but the discourse/topology engines are reusable substrate
if the AST blocker is ever lifted upstream.

## Verdict
**CONDITION-B BLOCKED** (CPython AST in the `runtime` branch). Same proof structure and same four
points (concrete example, exact fields, why-Java-cannot, why-frontier-reduction-fails) as
`query_semantics`. Deferred with proof.
