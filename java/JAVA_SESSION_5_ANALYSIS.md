# JAVA_SESSION_5_ANALYSIS

**Pre-implementation gate for `compile_document`. Result: STOP — forbidden dependency
(BeautifulSoup) in the transitive closure. No implementation performed.**

Python canon `origin/python` @ `9625f4a` (2.1.0), materialized worktree. Tracers committed:
[`tools/trace_imports_s5.py`](../tools/trace_imports_s5.py) (absolute-import only) and
[`tools/trace_imports_s5_relative.py`](../tools/trace_imports_s5_relative.py)
(**relative-import-aware** — required for correctness here).

---

## 0. Verdict

| | |
| --- | --- |
| API | `compile_document` → `core.ir.document_ir.compile_document_ir(text)` |
| Forbidden dependency | **BeautifulSoup** (`bs4`) — checks #1 |
| Reachability | **Load-time, hard** (cannot `import` the module without `bs4`) |
| Gate rule | "If any dependency is BeautifulSoup … STOP. Document it. Do not implement." |
| **Decision** | **STOP. Not implemented.** Parity stays **23 / 128**. |

The mission's premise — that `compile_document` is "the largest deterministic,
dependency-clean document subsystem that remains" — is **falsified by the rigorous proof**.
The earlier Session-4A note that called `compile_document` "READY (large)" relied on a
sub-agent's claim that `core.evidence` is dependency-clean; that claim missed the **relative
imports** inside `core.evidence/__init__.py`. The corrected, relative-aware trace below shows
the closure pulls in `core.semantic`, which imports BeautifulSoup.

---

## 1. Why the first trace looked clean (and was wrong)

The naive absolute-import trace ([`tools/trace_result_s5.json`](../tools/trace_result_s5.json))
reports a **25-module / 582-line / 0-forbidden / all-PURE** closure. That is an **artifact**:
the AST tracer skipped `from .x import y` (relative) statements, so it counted
`core.evidence/__init__.py` (77 lines) but never followed the **37 relative imports** inside
it. `core.evidence` is a package whose `__init__` eagerly imports all 37 engines; importing
it executes that whole graph.

The relative-aware trace ([`tools/trace_result_s5_relative.json`](../tools/trace_result_s5_relative.json))
gives the true closure: **275 modules, 6571 lines, 2 FORBIDDEN (BeautifulSoup)**.

---

## 2. The forbidden import chain (exact, reproducible)

`compile_document`'s call graph reaches `core.evidence` because the tutorial-prerequisite
branch uses `structure_cognition`:

```
core.ir.document_ir.compile_document_ir
  → core.documents.document_semantic_ir_engine.build_document_semantic_ir
    → core.documents.tutorial_prerequisite_engine.infer_tutorial_prerequisites
      → core.documents.tutorial_dependency_engine.reconstruct_tutorial_dependencies
        → core.documents.tutorial_reasoning_engine.extract_tutorial_flow
          → from core.evidence import structure_cognition        ← loads core.evidence/__init__
            → core.evidence.epistemic_evidence_engine
              → core.semantic.contradiction_pressure_engine       ← loads core.semantic/__init__
                → core.semantic.semantic_orchestrator
                  → core.semantic.table_semantics_engine  → from bs4 import BeautifulSoup
                  → core.semantic.ui_semantics_engine     → from bs4 import BeautifulSoup
```

`from core.evidence import structure_cognition` triggers `core.evidence/__init__.py`, which
imports `epistemic_evidence_engine`; that transitively imports
`core.semantic.contradiction_pressure_engine`, whose load runs `core.semantic/__init__.py`,
which imports `semantic_orchestrator` → `table_semantics_engine` / `ui_semantics_engine`,
both of which `from bs4 import BeautifulSoup` at module top level.

### Executable proof (bs4 blocked → import fails)

```python
import builtins
_real = builtins.__import__
def guard(name, *a, **k):
    if name == "bs4" or name.startswith("bs4."):
        raise ImportError("bs4 blocked (proof)")
    return _real(name, *a, **k)
builtins.__import__ = guard
from core.ir.document_ir import compile_document_ir   # bypasses webweavex/__init__
# -> ImportError: bs4 blocked (proof)
```

With BeautifulSoup made unimportable, `compile_document_ir` **cannot be imported** — proving
the dependency is real and load-time, not a tracer artifact. (`bs4 4.14.3` is installed in the
canon, so vectors *could* be generated; that does not make the dependency clean.)

---

## 3. Dependency classification

### 3a. The pure document path (the part that *would* be portable in isolation)

These engines — the 5 of 6 discourse branches that do **not** touch `core.evidence` — are
**Pure deterministic** (`re` / `typing` only):

| Module | Lines | Imports (first-party) | Class |
| --- | ---: | --- | --- |
| `core/ir/document_ir.py` | 50 | `document_semantic_ir_engine`, `ir._base` | Pure |
| `core/ir/_base.py` | 17 | — | Pure |
| `core/documents/document_semantic_ir_engine.py` | 28 | the 6 discourse engines | Pure (orchestrator) |
| `core/documents/rhetorical_parser_engine.py` | 24 | `rhetorical_structure_engine`, `semantic_role_engine` | Pure |
| `core/documents/rhetorical_structure_engine.py` | 23 | — (`re`) | Pure |
| `core/documents/semantic_role_engine.py` | 23 | — (`re`) | Pure |
| `core/documents/argument_dependency_engine.py` | 44 | — | Pure |
| `core/documents/concept_progression_engine.py` | 18 | `semantic_transition_engine`, `concept_transition_engine` | Pure |
| `core/documents/coreference_graph_engine.py` | 20 | `coreference_resolution_engine` | Pure |
| `core/documents/document_dependency_graph_engine.py` | 15 | `semantic_discourse_parser` | Pure |
| (+ ~10 more pure `core.documents.*` regex engines) | ~180 | — | Pure |

### 3b. The contaminating branch

| Module | Lines | Imports | Class |
| --- | ---: | --- | --- |
| `core/documents/tutorial_prerequisite_engine.py` | 26 | `instructional_semantics_engine`, **`tutorial_dependency_engine`** | bridges to forbidden |
| `core/documents/tutorial_dependency_engine.py` | 17 | `tutorial_reasoning_engine`, **`core.evidence`** | **Parser-dependent (transitive bs4)** |
| `core/documents/tutorial_reasoning_engine.py` | 33 | `section_engine`, **`core.evidence`** | **Parser-dependent (transitive bs4)** |
| `core.evidence` (package, 37 engines, eager `__init__`) | ~1.5k | relative → `core.semantic`, `core.crypto`, `core.determinism`, … | mixed; **pulls bs4** |
| `core.semantic.table_semantics_engine` | — | **`bs4`** | **Parser-dependent (BeautifulSoup)** |
| `core.semantic.ui_semantics_engine` | — | **`bs4`** | **Parser-dependent (BeautifulSoup)** |

### 3c. Other non-pure modules surfaced in the 275-module closure (informational)

| Module | Note | Class |
| --- | --- | --- |
| `core.determinism.normalization` | `unicodedata` (NFKC) — already ported in Java | Pure-deterministic (stdlib) |
| `core.crypto.kaalka_runtime_engine` | `hashlib`, `base64` — already ported | Pure-deterministic (stdlib) |
| `core.semantic.semantic_memory_engine` | `pathlib` | Deterministic-with-filesystem |
| `core.semantic.{table,ui}_semantics_engine` | **`bs4`** | **Parser-dependent — FORBIDDEN** |

No network, OCR, PDF, DOCX, browser, or LLM dependency was found; the **only** forbidden
class present is **BeautifulSoup**.

---

## 4. Forbidden-dependency checklist

| # | Forbidden class | Present in `compile_document` closure? |
| --- | --- | :---: |
| 1 | **BeautifulSoup** | **YES** — `core.semantic.{table,ui}_semantics_engine` (load-time reachable) |
| 2 | lxml | no |
| 3 | OCR | no |
| 4 | PDF binary | no |
| 5 | DOCX binary | no |
| 6 | Browser runtime | no |
| 7 | Network runtime | no |
| 8 | LLM runtime | no |

**Check #1 fails ⇒ STOP.**

---

## 5. Why this is not implemented (gate compliance)

- The gate is unambiguous: any BeautifulSoup dependency ⇒ STOP, document, do not implement.
- This matches the **Session-4B precedent**, where `heal_selector` and `ingest_input` were
  removed for transitive `bs4` / OCR imports.
- **Nuance, recorded honestly:** the bs4 code (`table_semantics_engine`,
  `ui_semantics_engine`) is *imported* but never *executed* during `compile_document(text)` —
  it is dead weight eagerly loaded by the `core.evidence` / `core.semantic` package `__init__`
  files. A Java port that reproduced only the *called* functions (`structure_cognition` + its
  real call-tree) could in principle be byte-exact and bs4-free. **This does not satisfy the
  gate as written** (the dependency proof is import-based and the canonical module cannot load
  without bs4), so it is not pursued unilaterally. Re-scoping `compile_document` to bypass the
  eager `core.evidence` package import is a design decision for the maintainer, not a silent
  port-time judgement call.

No Java source, no parity vectors, no governance/matrix/validator changes, no manifest edit
were made this session. `PARITY_MANIFEST.json` untouched.

---

## 6. Proven-clean alternatives (for redirection — not implemented)

Running the **relative-aware** proof on other unported `Complete` manifest APIs:

| Candidate API | Entry module | Closure | Verdict |
| --- | --- | --- | --- |
| `compile_document` | `core.ir.document_ir` | 275 mods / 6571 L | ❌ **bs4** |
| `query_documents` | `core.query.document_query_engine` | 276 mods / 6582 L | ❌ **bs4** (same `core.evidence` bridge) |
| `compile_repository` | `core.ir.repository_ir` | 306 mods / 8108 L | ❌ **bs4** |
| **`build_interaction_graph`** | `core.interaction.interaction_graph_engine` | **5 mods / 326 L** | ✅ **CLEAN** |
| `build_runtime_delta` | `core.synchronization.runtime_delta_engine` | 1 mod / 54 L | ✅ CLEAN |
| `recover_modal_runtime` | `core.adaptive.modal_recovery_engine` | 1 mod / 57 L | ✅ CLEAN |
| `clone_runtime_environment` | `core.reconstruction.runtime_clone_engine` | 1 mod / 26 L | ✅ CLEAN |
| `simulate_runtime_execution` | `core.runtime.runtime_simulation_engine` | 1 mod / 29 L | ✅ CLEAN |

The whole `core.evidence`-dependent document/IR family (`compile_document`,
`query_documents`, `compile_repository`) is gated by the same BeautifulSoup bridge and is
**not portable until the bs4-eager `core.semantic` package import is decoupled from
`core.evidence`** (a Python-canon refactor, out of scope here).

**Recommended next dependency slice:** `build_interaction_graph`
(`core.interaction.interaction_graph_engine`, 5 pure modules / 326 lines) — the largest
**proven-clean** deterministic subsystem remaining — pending the same dependency-proof gate
and the maintainer's go-ahead (the current mission scoped implementation to `compile_document`
only).

---

## 7. Reproduction

```
git worktree add -f /tmp/wwx-python origin/python
cd /tmp/wwx-python && python tools/trace_imports_s5_relative.py out.json
#   modules=275 lines=6571 forbidden=2
#     FORBIDDEN: core.semantic.table_semantics_engine ['FORBIDDEN:BeautifulSoup']
#     FORBIDDEN: core.semantic.ui_semantics_engine    ['FORBIDDEN:BeautifulSoup']
```
