# JAVA_AST_FRONTIER_query_semantics

**AST frontier audit (Phase B3). Verdict: CONDITION-B BLOCKED — observable output requires CPython
AST semantics. Proven, not assumed.** Canon `9625f4a`.

## Trace: ast.parse → API output

```
query_semantics("repository", payload)
└ query_repository(payload.source, payload.path)
  └ compile_repository_ir(source, path)
    └ semantic_ast = compile_semantic_ast_ir(source)        [core.ast]
      └ parse_python_ast(code)  ── import ast; ast.parse(code); ast.walk(tree)
    └ ir["semantic_ast"] = semantic_ast        ← KEPT in returned ir
  └ returns {ir, evidence, explainable, bounded}            ← ir kept whole
└ compile_semantic_query_ir("repository", target, result)   ← result kept whole
  └ {query_type, target, result, evidence, explainable, deterministic}
```

`result.ir.semantic_ast` is **in the serialized output** — not discarded.

## AST fields: created / consumed / discarded / observable

`parse_python_ast` creates per `ast.walk` node: `imports`, `functions` (`name`, `args=[a.arg…]`,
`node={type, lineno, end_lineno}`), `classes` (`name`, `bases=[base.id…]`, `node={…}`),
`assignments`. `resolve_symbols`/`build_control_flow_graph`/`reconstruct_execution_paths` derive
`symbols`/`cfg`/`execution_paths` from them. **None are discarded** — `compile_semantic_ast_ir`
returns all of them and `compile_repository_ir` stores the whole bundle in `ir["semantic_ast"]`.

## CRITICAL QUESTION — answered: AST is OBSERVABLE.

### 1. Concrete output example
`query_semantics("repository", {"source": "def foo(a, b):\n    x = bar()\n    return x\nclass A(Base):\n    pass"})`
→ (excerpt of the serialized result)
```
functions: [{"name":"foo","args":["a","b"],"node":{"type":"FunctionDef","lineno":1,"end_lineno":3}}]
classes:   [{"name":"A","bases":["Base"],"node":{"type":"ClassDef","lineno":4,"end_lineno":5}}]
```
(verified: `"lineno"`, `"end_lineno"`, `"FunctionDef"` all present in `json.dumps(output)`).

### 2. Exact AST-derived fields in observable output
`node.lineno`, `node.end_lineno`, `node.type` (CPython class name), `functions[].args`
(`ast.arguments.args`), `classes[].bases` (`getattr(base,"id",None)`), plus `symbols`/`cfg`/
`execution_paths` derived from them.

### 3. Why Java cannot reproduce them (for arbitrary source)
- **`end_lineno`** is the precise last source line of a def/class body. Computing it for arbitrary
  Python (nested defs, decorators, multiline expressions, continuation lines, comments, blank
  lines) requires a real structural parser — not a regex/heuristic.
- **`args`** = `node.args.args` — CPython's exact positional-or-keyword arg model (excludes
  `*args`/`**kw`, handles annotations/defaults/multiline signatures). A hand parser diverges on
  non-trivial signatures.
- **`node.type`** uses CPython's AST class taxonomy; **`bases`** depends on Name-vs-Attribute node
  discrimination.
Reproducing these byte-exact for *all* source strings is equivalent to embedding a
CPython-equivalent parser in Java — a non-portable runtime dependency (success-condition B).

### 4. Why frontier reduction fails
Unlike the epistemic engine (computed then **discarded** — proven absent from `query_documents`
output, which is why S22 succeeded with a passthrough), the AST IS the observable output
(`result.ir.semantic_ast.ast` with `lineno`/`end_lineno`/`args`/`bases`). There is no discard to
exploit; the minimal observable frontier **is** CPython AST fidelity.

## Verdict
**CONDITION-B BLOCKED.** `query_semantics` cannot be certified byte-exact without changing the
Python canon (replace the CPython-AST repository engine with a portable parser) or embedding a
CPython-equivalent parser in Java. Its document/graph/knowledge/unknown branches remain proven/pure
— the sole obstruction is the AST-backed `repository` branch.
