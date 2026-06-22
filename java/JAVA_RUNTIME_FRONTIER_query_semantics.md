# JAVA_RUNTIME_FRONTIER_query_semantics

**Runtime frontier analysis (Phase B2). Verdict: BLOCKED — non-portable (Python `ast`).** Canon
`9625f4a`. Measured, not estimated.

## Dispatch (runtime branches)

`query_semantics(query_type, payload)` (`core.query.semantic_query_engine`) dispatches by
`query_type`, wraps every result in `compile_semantic_query_ir` (17 lines, pure):

| query_type | engine | status |
| --- | --- | --- |
| `document` | `query_documents` | **PROVEN (S22)** — `io.webweavex.documents.DocumentSemanticIr` |
| `graph` | `query_graph` | **PROVEN** — `io.webweavex.query.GraphQuery` |
| `knowledge` | `query_knowledge` | **PROVEN** — `io.webweavex.query.OntologyQuery` |
| (unknown) | `compile_semantic_query_ir(qt,"",{error})` | pure |
| `repository` | `query_repository` → `compile_repository_ir` | **BLOCKED ↓** |

## The blocking frontier

`repository` → `core.query.repository_query_engine.query_repository` → `compile_repository_ir`
(`core.ir.repository_ir`) → `compile_semantic_ast_ir` (`core.ast`) →
**`core/parsers/ast_engine.py` which does `import ast; ast.parse(source)`** (CPython's AST).

The repository-branch output **embeds the full `compile_repository_ir`** (no discard — verified the
output contains `ir._raw`, `semantic_ast`), so byte-exact parity requires reproducing
`ast.parse(source)` for arbitrary source. **Java cannot replicate CPython's `ast` module
byte-exact** (different parser, different node model). For `source=""` the AST is empty (portable),
but the function accepts arbitrary source → not byte-exact-certifiable across all inputs.

## Verdict

**`query_semantics` is BLOCKED** by a non-portable runtime dependency (Python `ast.parse`) in its
`repository` branch. Per the deferred-API rule (condition B), it cannot be certified byte-exact
without changing the Python canon (e.g. replacing the AST engine with a portable parser) or
embedding a CPython-equivalent parser in Java. Its other four branches are already
proven/pure — the only obstruction is the AST engine. **Deferred with proof.**
