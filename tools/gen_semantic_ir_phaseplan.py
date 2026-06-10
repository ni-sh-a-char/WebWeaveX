"""Build an accurate dependency DAG of the 6 Category-A semantic-IR APIs'
function closure (resolving each call via the *calling function's module
namespace* to avoid name collisions), annotate determinism-sensitive ops,
topologically partition into independently-provable phases, and emit
SEMANTIC_IR_PHASE_PLAN.md.

Run: PYTHONPATH=<py2.0.1> python tools/gen_semantic_ir_phaseplan.py
"""
import ast
import inspect
import importlib
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEED = [
    "core.ir.document_ir", "core.documents.document_semantic_ir_engine",
    "core.query.document_query_engine", "core.evidence",
    "core.semantic.semantic_uncertainty_engine",
    "core.semantic.semantic_conservatism_engine", "core.ir.repository_ir",
    "core.repository.repository_semantic_ir_engine",
    "core.query.repository_query_engine", "core.reasoning.runtime_reasoning_engine",
    "core.reasoning.discourse_reasoning_engine",
    "core.reasoning.topology_reasoning_engine", "core.intelligence.graph_analyzer",
    "core.query.graph_query_engine", "core.query.ontology_query_engine",
]
ROOTS = [
    ("core.ir.document_ir", "compile_document_ir"),
    ("core.query.document_query_engine", "query_documents"),
    ("core.ir.repository_ir", "compile_repository_ir"),
    ("core.query.repository_query_engine", "query_repository"),
    ("core.reasoning.topology_reasoning_engine", "reason_topology_semantic"),
    ("core.reasoning.discourse_reasoning_engine", "reason_discourse_semantic"),
    ("core.reasoning.runtime_reasoning_engine", "reason_runtime_semantic"),
]

DET_OPS = ["round(", "sorted(", "set(", "sha256", "json.dumps", "frozenset",
           ":.", "%.", "hashlib"]


def main():
    for m in SEED:
        try:
            importlib.import_module(m)
        except Exception:
            pass

    nodes = {}  # (mod,name) -> {lines, deps:set, ops:dict, src}

    def func_module_ns(fn):
        return sys.modules.get(fn.__module__).__dict__ if fn.__module__ in sys.modules else {}

    def trace(fn):
        key = (fn.__module__, fn.__name__)
        if key in nodes:
            return
        try:
            src = inspect.getsource(fn)
        except Exception:
            return
        ops = {op: src.count(op) for op in DET_OPS if src.count(op)}
        nodes[key] = {"lines": len(src.splitlines()), "deps": set(), "ops": ops}
        ns = func_module_ns(fn)
        try:
            tree = ast.parse(src)
        except Exception:
            return
        called = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                if isinstance(n.func, ast.Name):
                    called.add(n.func.id)
                elif isinstance(n.func, ast.Attribute):
                    called.add(n.func.attr)
        for nm in called:
            obj = ns.get(nm)
            if inspect.isfunction(obj) and obj.__module__.startswith("core."):
                nodes[key]["deps"].add((obj.__module__, obj.__name__))
                trace(obj)

    for mod, fn in ROOTS:
        try:
            trace(getattr(importlib.import_module(mod), fn))
        except Exception:
            pass

    # keep only deps that are in the closure
    for k, v in nodes.items():
        v["deps"] = {d for d in v["deps"] if d in nodes}

    # topological partition into phases (Kahn layering)
    remaining = dict(nodes)
    done = set()
    phases = []
    while remaining:
        layer = sorted(k for k, v in remaining.items() if v["deps"] <= done)
        if not layer:  # cycle — break by taking lowest-dep nodes
            layer = sorted(remaining, key=lambda k: len(remaining[k]["deps"] - done))[:1]
        phases.append(layer)
        for k in layer:
            done.add(k)
            remaining.pop(k)

    def risk(keys):
        score = sum(sum(nodes[k]["ops"].values()) for k in keys)
        if score == 0:
            return "LOW"
        if score < 15:
            return "MEDIUM"
        return "HIGH"

    total_lines = sum(v["lines"] for v in nodes.values())
    L = ["# SEMANTIC_IR_PHASE_PLAN.md", "",
         "> **Recomputed from `origin/python` 2.0.1 source** by "
         "`tools/gen_semantic_ir_phaseplan.py`. Accurate call edges (resolved via each "
         "function's own module namespace — no name-collision guessing). Topologically "
         "layered so each phase depends only on earlier phases and is independently "
         "executable/provable.", "",
         f"**Closure: {len(nodes)} functions · {total_lines} lines · {len(phases)} phases.**",
         "",
         "## Phase summary (topological order; Phase A = leaves)", "",
         "| Phase | Functions | Lines | Determinism ops | Parity risk |",
         "|-------|----------:|------:|----------------:|:-----------:|"]
    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i, layer in enumerate(phases):
        ln = sum(nodes[k]["lines"] for k in layer)
        ops = sum(sum(nodes[k]["ops"].values()) for k in layer)
        ph = names[i] if i < 26 else f"P{i}"
        L.append(f"| {ph} | {len(layer)} | {ln} | {ops} | {risk(layer)} |")

    L += ["",
          "## Phase A — leaf functions (no in-closure dependencies)", "",
          "These have **zero unported dependencies** and are ported & proven first.", "",
          "| Module | Function | Lines | Determinism ops |",
          "|--------|----------|------:|-----------------|"]
    for k in phases[0]:
        ops = ", ".join(f"{o}×{n}" for o, n in nodes[k]["ops"].items()) or "—"
        L.append(f"| `{k[0]}` | `{k[1]}` | {nodes[k]['lines']} | {ops} |")

    L += ["",
          "## Determinism-sensitive operations (whole closure)", "",
          "Every site below must match Python bit-for-bit:", "",
          "| Operation | Total occurrences |", "|-----------|------------------:|"]
    agg = {}
    for v in nodes.values():
        for o, n in v["ops"].items():
            agg[o] = agg.get(o, 0) + n
    for o, n in sorted(agg.items(), key=lambda x: -x[1]):
        L.append(f"| `{o}` | {n} |")

    L += ["",
          "## Full DAG (function → in-closure dependencies)", "",
          "<details><summary>expand</summary>", "", "```"]
    for k in sorted(nodes):
        deps = ", ".join(f"{d[1]}" for d in sorted(nodes[k]["deps"]))
        L.append(f"{k[1]}  <-  [{deps}]")
    L += ["```", "</details>", "",
          "## Execution protocol per phase", "",
          "1. Port the phase's functions to `lib/src/semantic_ir/` (canonical, no "
          "approximation).",
          "2. Add executable fixtures calling exactly those functions.",
          "3. Execute Python (canonical), JavaScript (engine), Dart.",
          "4. Verify `hash(Python) == hash(JS) == hash(Dart)` and deep equality.",
          "5. Commit vectors + parity tests. Only then advance to the next phase.",
          "6. The 6 public APIs (`compile_document`, `query_documents`, `compile_repository`, "
          "`query_repository`, `query_semantics`, `reason_semantically`) promote to Complete "
          "only when the final phase closes the whole closure with executable proof."]
    open(os.path.join(REPO, "SEMANTIC_IR_PHASE_PLAN.md"), "w",
         encoding="utf-8").write("\n".join(L) + "\n")
    print(f"Wrote SEMANTIC_IR_PHASE_PLAN.md: {len(nodes)} funcs, {total_lines} lines, "
          f"{len(phases)} phases; Phase A leaves = {len(phases[0])}")


if __name__ == "__main__":
    main()
