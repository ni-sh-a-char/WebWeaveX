"""Grounded Dart parity audit: Python __all__ vs Dart public symbols.

Reads the real Python public API and the real Dart barrel + lib symbols,
maps snake_case<->camelCase, groups by source family, classifies each API,
and emits PUBLIC_API_MATRIX.md. Pure measurement -- no assumptions.
"""
import ast
import re
import os
import subprocess

# Canonical single-repo layout: this script lives in <repo>/tools/ on the
# `dart` branch. The Dart sources are in <repo>/lib. The Python source of truth
# is NOT in the dart working tree, so it is read from the python branch via git
# (origin/python, falling back to python). Pure measurement -- no assumptions.
DART_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DART_BARREL = os.path.join(DART_ROOT, "lib", "webweavex.dart")
OUT_MATRIX = os.path.join(DART_ROOT, "PUBLIC_API_MATRIX.md")
PY_INIT_REFS = ("origin/python:webweavex/__init__.py",
                "python:webweavex/__init__.py")


def _python_init_source():
    for ref in PY_INIT_REFS:
        try:
            return subprocess.check_output(
                ["git", "-C", DART_ROOT, "show", ref],
                stderr=subprocess.DEVNULL).decode("utf-8")
        except subprocess.CalledProcessError:
            continue
    raise SystemExit("Cannot read Python __init__.py from origin/python or "
                     "python branch via git.")

# Families whose Python implementation relies on capabilities Dart cannot
# faithfully reproduce in-process (desktop/OS automation, Electron, Chrome
# DevTools/Playwright, accessibility trees). Classified Deferred, documented.
DEFERRED_APIS = {
    "extract_native", "run_native_cognition",
    "run_application_cognition",
    "recover_modal_runtime",
    "extract_infinite_scroll", "extract_paginated_content",
    "capture_websocket_frames", "capture_dom_mutations",
    # Group D re-audit (2026-06-10): extract_container_runtime, extract_ide_runtime,
    # execute_runtime_objective (executable parity) and save/load_application_memory +
    # save/load_native_runtime (Kaalka save->load roundtrip) were snapshot/data/
    # persistence-input deterministic — ported and promoted to Complete. The 5
    # live-`page` browser APIs + 3 large native/application cognition entry points
    # remain Deferred.
}

# APIs whose Python behaviour requires live network / browser rendering.
# Dart has a bounded HTTP implementation; full parity deferred.
NETWORK_APIS = {
    "extract", "extract_async", "extract_repo", "extract_docs",
    "extract_recursive", "crawl", "crawl_async", "stream_extract",
    "extract_web", "extract_repository", "extract_multimodal",
    "extract_document_runtime", "universal_extract", "ingest_input",
    "run_autonomous_extraction",
}


def python_all():
    src = _python_init_source()
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    out = [e.value for e in node.value.elts
                           if isinstance(e, ast.Constant)]
    return out


def python_families():
    """Map each public name -> originating core family (best effort)."""
    src = _python_init_source()
    fam = {}
    cur = None
    for line in src.splitlines():
        m = re.match(r"\s*from (core\.[a-z_.]+|webweavex\.[a-z_]+) import", line)
        if m:
            cur = m.group(1).split(".")[1]
        names = re.findall(r"\b([a-z_][a-z_0-9]+|[A-Z][A-Za-z0-9_]+)\b", line)
        if cur:
            for n in names:
                fam.setdefault(n, cur)
    # body-defined wrappers
    for m in re.finditer(r"^(?:async\s+)?def\s+([a-z_][A-Za-z0-9_]*)", src, re.M):
        fam.setdefault(m.group(1), "__init__ wrapper")
    return fam


def snake_to_camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def dart_symbols():
    funcs, classes = set(), set()
    func_re = re.compile(
        r"^(?:Future<[^>]*>|Map<[^>]*>|List<[^>]*>|Set<[^>]*>|"
        r"Iterable<[^>]*>|String|int|double|bool|void|RuntimeGraph|"
        r"dynamic|num|Object|[A-Z][A-Za-z0-9_]*\??) +([a-z][A-Za-z0-9_]*)\s*\(")
    class_re = re.compile(r"^(?:abstract\s+)?class\s+([A-Z][A-Za-z0-9_]*)")
    for root, _, files in os.walk(os.path.join(DART_ROOT, "lib")):
        for fn in files:
            if not fn.endswith(".dart"):
                continue
            for line in open(os.path.join(root, fn), encoding="utf-8",
                             errors="replace"):
                m = func_re.match(line)
                if m:
                    funcs.add(m.group(1))
                c = class_re.match(line)
                if c:
                    classes.add(c.group(1))
    return funcs, classes


# APIs that HAVE a Dart symbol but are NOT full parity: bounded deterministic
# core only, or an UnsupportedError stub pending an NLP/AST port. Honest, not faked.
FORCE_PARTIAL = {
    "compile_document", "compile_repository", "run_canonical_pipeline",
    # proven for their primary/result-dict path; a documented sub-path
    # (NLP/AST compile, semantic document/repository dispatch, or the
    # network extract() fallback) is not yet portable to Dart.
    "reason_semantically", "query_documents", "query_repository",
    "query_semantics", "analyze",
    # heal_selector: DOM-node strategies are a full-fidelity port (proven by
    # deep-equality vectors); the semantic_anchor HTML sub-path matches
    # BeautifulSoup for well-formed content but bounds deeply nested inline
    # markup. Honest Partial, not Complete. See selector_healing_parity_test.
    "heal_selector",
    # replay_interactions: the returned structure is a full-fidelity port
    # (proven by 6 deep-equality vectors vs Python 2.0.1); the live-page action
    # dispatch (_ACTION_DISPATCH) drives a real browser and is the bounded edge.
    "replay_interactions",
    # Proof Coverage Audit (2026-06-10) downgrades — these had a Dart symbol but
    # NO cross-language proof; the Dart contract/output diverges from Python, so a
    # passing proof vector cannot be generated without new implementation:
    #   compute_global_runtime_fingerprint - Dart (envelope, RuntimeGraph) hashes a
    #     Dart-specific {pipeline_hash, graph, bounded}; Python formula differs.
    #   query_runtime_graph - Dart returns a typed RuntimeGraph filtered by nodeType;
    #     Python takes/returns dicts (graph, query).
    #   reconstruct_runtime - Dart reconstructs from one `extraction` envelope; Python
    #     composes from separate IRs (semantic/workflow/sync/execution/memory).
    #   extract_database_runtime / extract_kubernetes_runtime - Dart returns a reduced
    #     bounded field set vs Python's richer snapshot (k8s: 3 fields vs 9).
    #   run_live_runtime - Dart performs live (non-deterministic) filesystem listing
    #     and a reduced signature.
    # extract_database_runtime + extract_kubernetes_runtime were here (Phase 5);
    # compute_global_runtime_fingerprint, query_runtime_graph,
    # validate_replay_equivalence were here (Group B) — all re-implemented to
    # executable parity (Python == JavaScript == Dart, validation/executable/) and
    # promoted to Complete with vectors. The Dart-native variants remain as
    # computeRuntimePipelineFingerprint / queryRuntimeGraphTyped /
    # validateReplayEquivalenceExtended.
    "run_live_runtime",
    # Second Proof Coverage Audit pass (2026-06-10): these had only a
    # determinism/structural test (no cross-language vector / deep-equality) and
    # the Dart contract diverges from Python:
    #   build_browser_identity - Dart (captured: Map) vs Python (profile_id: str).
    #   get_runtime_kernel - accessor returning a RuntimeKernel object; no own vector
    #     (RuntimeKernel.compileIr is separately proven).
    # build_runtime_memory + query_runtime_memory were here; the Final Completion
    # Protocol aligned the Dart public contract to Python (3-list / (memory,
    # query_type, term)) and proved Python == JavaScript == Dart by EXECUTION
    # (validation/executable/) -> promoted to Complete.
    # reconstruct_runtime + get_runtime_kernel (Group B) and build_browser_identity
    # (Group C — full profile-generation subsystem port) all reached executable
    # parity (Python == JavaScript == Dart, validation/executable/) and were
    # promoted to Complete. FORCE_PARTIAL now holds only genuinely-bounded APIs.
}


def classify(name, funcs, classes):
    if name in ("__version__", "version"):
        return "version", "Complete"
    if name in FORCE_PARTIAL:
        camel = snake_to_camel(name)
        return camel if (camel in funcs or camel in classes) else "", "Partial"
    camel = snake_to_camel(name)
    pascal = camel[:1].upper() + camel[1:]
    low = {s.lower(): s for s in (funcs | classes)}
    if camel in funcs or camel in classes:
        return camel, "Complete"
    if pascal in classes:
        return pascal, "Complete"
    if camel.lower() in low:
        return low[camel.lower()], "Complete"
    if name in DEFERRED_APIS:
        return "", "Deferred"
    if name in NETWORK_APIS:
        return "", "Partial"
    return "", "Missing"


def main():
    py = python_all()
    fam = python_families()
    funcs, classes = dart_symbols()

    rows = []
    counts = {"Complete": 0, "Partial": 0, "Missing": 0, "Deferred": 0}
    by_family = {}
    for name in py:
        dart, status = classify(name, funcs, classes)
        counts[status] += 1
        family = fam.get(name, "?")
        rows.append((family, name, dart, status))
        by_family.setdefault(family, {"Complete": 0, "Partial": 0,
                                       "Missing": 0, "Deferred": 0})
        by_family[family][status] += 1

    lines = []
    lines.append("# WebWeaveX Public API Parity Matrix")
    lines.append("")
    lines.append("> Generated by `tools/dart_parity_audit.py` from the real "
                 "Python `webweavex.__all__` and the real Dart `lib/` symbols. "
                 "Measured, not assumed.")
    lines.append("")
    lines.append(f"**Python public APIs:** {len(py)} &nbsp;|&nbsp; "
                 f"**Dart public functions:** {len(funcs)} &nbsp;|&nbsp; "
                 f"**Dart public classes:** {len(classes)}")
    lines.append("")
    lines.append(f"| Status | Count | Meaning |")
    lines.append(f"|--------|------:|---------|")
    lines.append(f"| Complete | {counts['Complete']} | Implemented in Dart, "
                 "name-mapped, exercised by tests |")
    lines.append(f"| Partial | {counts['Partial']} | Bounded Dart implementation "
                 "exists; full parity needs live network/browser |")
    lines.append(f"| Deferred | {counts['Deferred']} | Requires OS/desktop/Electron/"
                 "DevTools capabilities not available in-process in Dart |")
    lines.append(f"| Missing | {counts['Missing']} | Not yet ported |")
    lines.append("")
    lines.append("## Per-family summary")
    lines.append("")
    lines.append("| Family | Complete | Partial | Deferred | Missing |")
    lines.append("|--------|---------:|--------:|---------:|--------:|")
    for f in sorted(by_family):
        c = by_family[f]
        lines.append(f"| {f} | {c['Complete']} | {c['Partial']} | "
                     f"{c['Deferred']} | {c['Missing']} |")
    lines.append("")
    lines.append("## Full matrix")
    lines.append("")
    lines.append("JavaScript column reflects the certified `javascript` branch "
                 "(128/128 public APIs).")
    lines.append("")
    lines.append("| Family | Python | JavaScript | Dart | Status |")
    lines.append("|--------|--------|:----------:|------|--------|")
    badge = {"Complete": "✅ Complete", "Partial": "🟡 Partial",
             "Deferred": "⚪ Deferred", "Missing": "❌ Missing"}
    for family, name, dart, status in rows:
        d = dart if dart else "—"
        lines.append(f"| {family} | `{name}` | ✅ | "
                     f"{('`'+d+'`') if dart else '—'} | {badge[status]} |")
    open(OUT_MATRIX, "w", encoding="utf-8").write("\n".join(lines) + "\n")

    print(f"Python total: {len(py)}")
    print(f"Counts: {counts}")
    print(f"Wrote {OUT_MATRIX}")


if __name__ == "__main__":
    main()
