# JAVA_RUNTIME_FRONTIER_reason_semantically

**Runtime frontier analysis (Phase B2). Verdict: BLOCKED — non-portable (Python `ast`).** Canon
`9625f4a`. Measured empirically.

## Dispatch (runtime branches)

`reason_semantically(domain, payload)` (`core.reasoning.semantic_reasoning_engine`) dispatches by
`domain`, then returns `{**result, domain, deterministic:True}`:

| domain | engine | frontier | output (measured) |
| --- | --- | --- | --- |
| `discourse` | `reason_discourse_semantic` | 25 mod / 514 L, **epistemic-free** (verified: no `uncertainty`/`entropy`/`epistemic_state` in output), reuses the proven document-IR engines | **PORTABLE** |
| `topology` | `reason_topology_semantic` | 5 mod / 115 L; `uncertainty`/`entropy`/`justification` are computed **inline** by small local functions (not the 4496-line epistemic engine) | **PORTABLE** |
| `runtime` | `reason_runtime_semantic` | → `parser_registry` → `import ast; ast.parse(source)` | **BLOCKED ↓** |
| (unknown) | `{error, explainable}` | pure | portable |

## The blocking frontier

The `runtime` branch parses `source` via `core/parsers/*` which use **CPython's `ast` module**
(`ast.parse`, `ast.NodeVisitor`). The branch output embeds the parsed AST IR, so byte-exact parity
requires reproducing CPython's AST for arbitrary source — **non-portable**.

## Verdict

Two of three branches (`discourse` 514 L, `topology` 115 L) are **portable and epistemic-free** —
a pleasant frontier result (the 4496-line epistemic engine is NOT needed). But the `runtime` branch
is **BLOCKED** by Python `ast.parse`. Because byte-exact parity must hold for every `domain`,
**`reason_semantically` as a whole is BLOCKED** (condition B) until the AST engine is portable or
the canon changes. The portable discourse/topology engines are reusable substrate if the AST
blocker is ever lifted. **Deferred with proof.**
