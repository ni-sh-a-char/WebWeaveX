# JAVA_AST_FINAL_VERDICT

**Phase-1 re-audit (Session 28). Verdict: CONDITION-B BLOCKED — re-proven from runtime output, not
trusted from prior sessions.** Python canon `9625f4a`. Tooling re-evaluated: tree-sitter, JavaParser,
hand parser, canonical-IR normalization. None reproduce CPython `ast` byte-exact.

## APIs in scope
`query_semantics` (repository branch), `reason_semantically` (runtime branch), `compile_repository`.
(`extract_repo`, `extract_recursive`, `analyze` are sometimes mislabeled "AST" — they are actually
**lxml**-blocked via `extract()`; see JAVA_EXTRACTION_FINAL_VERDICT.)

## A. Concrete runtime example
```
compile_repository("def foo(a, b):\n    x = bar()\n    return x\nclass A(Base):\n    pass")
→ result.ir.semantic_ast.ast (excerpt, present verbatim in json.dumps(output)):
  functions: [{"name":"foo","args":["a","b"],"node":{"type":"FunctionDef","lineno":1,"end_lineno":3}}]
  classes:   [{"name":"A","bases":["Base"],"node":{"type":"ClassDef","lineno":4,"end_lineno":5}}]
```
Trace: `compile_repository → compile_repository_ir → compile_semantic_ast_ir → parse_python_ast`,
which executes `import ast; ast.parse(source); ast.walk(tree)` and extracts `lineno`/`end_lineno`/
`args`/`bases`. The bundle is stored in `ir["semantic_ast"]` and **returned whole**.

## B. Observable output dependency
The serialized result embeds CPython AST field values: `node.lineno`, `node.end_lineno`,
`node.type` (CPython AST class name, e.g. `FunctionDef`/`ClassDef`), `functions[].args`
(`ast.arguments.args`), `classes[].bases` (Name-vs-Attribute discrimination), plus `symbols`/`cfg`/
`execution_paths` derived from the same tree. All reach `json.dumps(output)` and the global fingerprint.

## C. Why Java cannot reproduce it (under project constraints)
- **JavaParser** parses *Java*, not Python — categorically inapplicable.
- **tree-sitter-python** builds a *different* grammar/taxonomy: node kinds are `function_definition`/
  `class_definition` (not CPython's `FunctionDef`/`ClassDef`), it exposes byte/point ranges rather
  than CPython's 1-based `lineno` + computed `end_lineno`, and its parameter model is a CST node list,
  not `ast.arguments.args`. Byte-exact field-name/value parity would require translating tree-sitter's
  CST into CPython's AST taxonomy — i.e. re-implementing CPython's `ast` semantics on top, including
  `end_lineno` body-span computation across decorators/nesting/multiline/continuations.
- **A hand parser** diverges on non-trivial signatures (annotations, defaults, `*args`/`**kw`
  exclusion), comprehensions, and `end_lineno` edge cases — not byte-exact for arbitrary source.
- **Canonical-IR normalization** cannot help: there is no lossy normalization step to exploit (see D).
The only byte-exact route is embedding a CPython-equivalent parser in the JVM — a non-portable
native-equivalent dependency. Pure-Java parity cannot be **guaranteed** for arbitrary source.

## D. Why frontier reduction fails
Reduction succeeded in S22 (`query_documents`) because the epistemic engine's output was *computed
then discarded* — absent from the observable surface. Here the AST **is** the observable surface
(`result.ir.semantic_ast.ast` with `lineno`/`end_lineno`/`args`/`bases`). There is no discard to
exploit; the minimal observable frontier *is* CPython-AST fidelity over arbitrary input.

## Verdict
**CONDITION-B BLOCKED** for `query_semantics`, `reason_semantically`, `compile_repository`. The
document/graph/knowledge/unknown branches of `query_semantics` remain pure/portable; the sole
obstruction is the AST-backed branch, which gates the whole API's byte-exact certification.
