# JAVA_SESSION_6_BLOCKER_AUDIT

**Phase 0 — revalidate the Session-5 `compile_document` blocker via runtime call tracing.
Analysis only; no implementation, no governance changes.**

Python canon `origin/python` @ `9625f4a` (2.1.0), `bs4 4.14.3` installed. Tracer:
[`tools/runtime_trace_s6.py`](../tools/runtime_trace_s6.py) (uses `sys.setprofile` to record
every executed `core.*` function while running `compile_document_ir` on 4 sample documents).
Result: [`tools/runtime_trace_s6.json`](../tools/runtime_trace_s6.json).

---

## Verdict: **A — import-time blocked only** (NOT behaviorally blocked)

| Question | Answer | Evidence |
| --- | --- | --- |
| Can `compile_document_ir` be **imported** without bs4? | **No** | Session 5: `__import__` guard → `ImportError` (hard load-time dep) |
| Does running `compile_document(text)` **execute** any bs4 code path? | **No** | runtime trace: `behaviorally_reaches_bs4 = false`, **0** call-hits in `bs4` / `table_semantics_engine` / `ui_semantics_engine` |

So the BeautifulSoup dependency is **dead eager-package-import weight**, never executed by the
computation. The Session-5 STOP was a correct application of the **import-based** gate, but the
underlying computation is bs4-free and deterministic.

---

## Runtime evidence

Running `compile_document_ir` over 4 samples (empty, headed tutorial, numbered list,
argumentative prose):

| Metric | Value |
| --- | ---: |
| Distinct `core.*` modules **executed** | **238** |
| Distinct `core.*` functions **executed** | **311** |
| `core.evidence` modules executed (incl. `grounding_engine` → `structure_cognition`) | 206 |
| `core.semantic` modules executed | 12 (all *pressure*/*uncertainty* engines — pure) |
| `core.semantic.table_semantics_engine` / `ui_semantics_engine` executed | **0** |
| `bs4` functions executed | **0** |

The 12 executed `core.semantic` modules are
`ambiguity_pressure_engine, contradiction_pressure_engine, contradiction_restraint_engine,
evidence_boundary_pressure_engine, evidence_decay_pressure_engine,
recursive_boundary_pressure_engine, recursive_convergence_pressure_engine,
recursive_dependency_pressure_engine, semantic_boundary_pressure_engine,
semantic_uncertainty_engine, truth_boundary_pressure_engine, uncertainty_pressure_engine` —
all pure (`re`/`typing`/`math`). The two bs4 engines are imported by `core.semantic/__init__`
but **never called**.

---

## Implication (recorded; no action taken this session)

A faithful Java port of `compile_document` that reproduces only the **executed** call-tree
(238 modules / 311 functions, all deterministic) would be **byte-exact and bs4-free**. The
blocker is purely Python's eager package `__init__` loading of unrelated sibling engines.

**This does not, by itself, unblock `compile_document` under the current import-based gate.**
Two clean paths exist for a future session (maintainer decision):

1. **Canon refactor** — make `core.evidence` / `core.semantic` import their bs4 engines lazily
   (or move `structure_cognition` out of the eagerly-loaded package), so the module imports
   without bs4. Then the import-based gate passes.
2. **Gate amendment** — adopt a **behavioral** dependency criterion (runtime-trace-based, as in
   this audit) for the document/IR family, since the import-based criterion produces a
   false-positive here.

Until one of those is chosen, `compile_document` / `query_documents` / `compile_repository`
remain **STOP** under the strict gate, and Session 6 proceeds with the **proven-clean**
`build_interaction_graph` (Phases 1–8).

## Reproduction

```
python tools/runtime_trace_s6.py
#   executed core.* modules=238 funcs=311; core.semantic executed=12;
#   bs4/suspect call-hits=0 -> behaviorally_reaches_bs4=False
```
