# JAVA_AST_ADVERSARIAL_REVIEW

**Adversarial attack on the AST (CPython `ast`) blocker proof. CPython AST output is compared field-by-
field against what JavaParser and Tree-sitter can produce, under the byte-exact + pure-Java
constraints.** Python canon `9625f4a`.

## Question
Can byte-exact parity for the AST-backed APIs (`query_semantics` repository branch,
`reason_semantically` runtime branch, `compile_repository`) be achieved? — **NO.**

## The observable target (empirically captured)
`compile_repository("def foo(a, b=2, *args):\n    x = bar()\n    return x\nclass A(Base):\n    pass")`
emits, verbatim in the serialized result:
```json
functions: [{"name":"foo","args":["a","b"],"node":{"type":"FunctionDef","lineno":1,"end_lineno":3}}]
classes:   [{"name":"A","bases":["Base"],"node":{"type":"ClassDef","lineno":4,"end_lineno":5}}]
```
Key invariants any port must reproduce **byte-exact for arbitrary source**:
- `node.type` = the **CPython AST class name** (`FunctionDef`, `ClassDef`, …).
- `node.lineno` = CPython 1-based start line; `node.end_lineno` = CPython's computed last line of the
  node's body (spanning nested defs, decorators, multiline expressions, continuations).
- `args` = `ast.arguments.args` names only — note the example yields `["a","b"]`: it **excludes**
  `*args` and drops default values. This is CPython's exact positional-or-keyword model.
- `bases` = base names via CPython Name-vs-Attribute node discrimination.

## Candidate comparison

### CPython `ast` (the oracle) — baseline
`import ast; ast.parse(src); ast.walk(tree)` gives `FunctionDef`/`ClassDef` nodes with `lineno`/
`end_lineno`/`args`(=`arguments.args`)/`bases`. This is the exact source of every observable field.

### JavaParser — NO (categorically inapplicable)
JavaParser parses **Java**, not Python. It cannot parse `def foo(...)`/`class A(Base)` at all. Even by
analogy its model is alien: node types are Java (`MethodDeclaration`, `ClassOrInterfaceDeclaration`),
positions are `Range(begin:line/col, end:line/col)` (includes columns; different end semantics), and it
has no `ast.arguments` Python parameter model. Zero field overlap. Not a candidate.

### Tree-sitter (tree-sitter-python) — NO (different model; not byte-exact)
Tree-sitter produces a **concrete syntax tree**, not CPython's AST. Concrete divergences:
- **Node type names differ**: tree-sitter emits `function_definition` / `class_definition` /
  `identifier`, *not* CPython's `FunctionDef` / `ClassDef`. Byte-exact `node.type` would require a hand
  re-mapping table for the entire CPython AST taxonomy.
- **Position model differs**: tree-sitter exposes `start_point`/`end_point` as **0-based (row, column)**
  byte offsets; CPython exposes **1-based `lineno`** and a computed **`end_lineno`**. The values and the
  field semantics differ; reproducing CPython's `end_lineno` (last line of the *logical* node body) from
  tree-sitter's byte ranges requires re-implementing CPython's end-position computation, including its
  treatment of decorators, trailing comments/blank lines, multiline strings and continuations.
- **Parameter model differs**: tree-sitter's `parameters` is a CST node list (each a
  `identifier`/`typed_parameter`/`default_parameter`/`list_splat_pattern`); deriving exactly
  `ast.arguments.args` (positional-or-keyword names only, excluding `*args`/`**kwargs`, dropping
  defaults — e.g. `["a","b"]` from `(a, b=2, *args)`) requires re-deriving CPython's arg-classification
  rules on top of the CST.
In short, tree-sitter would have to be wrapped in a full CPython-AST-emulation layer (taxonomy +
end-position + argument model) to match — and any divergence on a single construct breaks the byte-exact
`fingerprint`.

### (also rejected) JNI to CPython / subprocess to Python — NO (constraint violation)
Embedding the CPython parser via JNI or shelling out to `python -c "import ast…"` would match by
definition, but ships a Python runtime dependency — non-portable, non-deterministic across
environments, and contrary to an independent pure-Java port. Fails the project constraints (same
rejection as the libxml2 bridge in JAVA_EXTRACTION_ADVERSARIAL_REVIEW).

## Frontier-reduction re-test
In S22 the epistemic engine's output was computed then **discarded**, so a passthrough sufficed. Here
the AST **is** the observable output (`result.ir.semantic_ast.ast` with `node.type`/`lineno`/
`end_lineno`/`args`/`bases`). There is no discard to exploit; the minimal observable frontier *is*
CPython-AST fidelity over arbitrary source.

## Verdict
**NO** — byte-exact AST parity cannot be achieved under project constraints. JavaParser is
inapplicable (wrong language); Tree-sitter produces a structurally different tree (node taxonomy,
0-based byte positions vs CPython `lineno`/`end_lineno`, CST vs `ast.arguments`) and would require a
full CPython-AST-emulation layer that cannot be guaranteed byte-exact for arbitrary input; CPython
embedding/subprocess violate portability. The blocker stands. Affected: `query_semantics`,
`reason_semantically`, `compile_repository`. Unblock requires an upstream canon change (replace the
CPython-AST repository engine with a specified portable parser/IR).
