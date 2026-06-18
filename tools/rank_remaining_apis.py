#!/usr/bin/env python3
"""Machine-derived ranking: for every manifest API not yet Java-proven, resolve its Python
entry module and trace the relative-aware closure -> clean/forbidden + size."""
from __future__ import annotations
import ast, json, os, re, sys
import trace_imports_s5_relative as _tr  # relative-aware tracer

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = json.load(open(os.path.join(ROOT, "PARITY_MANIFEST.json"), encoding="utf-8")) \
    if os.path.exists(os.path.join(ROOT, "PARITY_MANIFEST.json")) else None

PROVEN = {
    'UniversalInput','build_interaction_graph','build_runtime_graph','build_runtime_memory',
    'compile_unified_runtime_ir','compute_global_runtime_fingerprint','compute_kaalka_hash',
    'decrypt_value','encrypt_value','extract_api_runtime','extract_database_runtime',
    'extract_document_runtime','extract_paginated_content','extract_runtime_streams',
    'extract_telemetry_runtime','fingerprint','query_graph','query_knowledge',
    'query_runtime_graph','query_runtime_memory','reconstruct_runtime','search_runtime_memory',
    'validate_reconstructed_runtime','validate_replay_equivalence',
}


def init_export_map():
    """name -> module, from webweavex/__init__.py `from core.X import (a, b)` statements."""
    path = os.path.join(ROOT, "webweavex", "__init__.py")
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    m = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("core"):
            for a in node.names:
                m[a.asname or a.name] = node.module
    return m


def find_def_module(api):
    """grep core/ + webweavex/ for `def api(` ; return first dotted module."""
    pat = re.compile(rf"^\s*(?:async\s+)?def\s+{re.escape(api)}\s*\(", re.M)
    hits = []
    for base in ("core", "webweavex"):
        for dp, _d, names in os.walk(os.path.join(ROOT, base)):
            for n in names:
                if not n.endswith(".py"):
                    continue
                fp = os.path.join(dp, n)
                try:
                    if pat.search(open(fp, encoding="utf-8-sig").read()):
                        rel = os.path.relpath(fp, ROOT).replace(os.sep, "/")
                        mod = rel[:-3].replace("/", ".")
                        if mod.endswith(".__init__"):
                            mod = mod[:-9]
                        hits.append(mod)
                except Exception:
                    pass
    # prefer non-__init__, non-webweavex
    hits.sort(key=lambda x: ("webweavex" in x, "__init__" in x, len(x)))
    return hits[0] if hits else None


def main():
    export_map = init_export_map()
    rows = []
    apis = [a["api"] for a in MANIFEST["apis"]] if MANIFEST else []
    for api in apis:
        if api in PROVEN or api in ("RuntimeKernel", "__version__", "version"):
            continue
        mod = export_map.get(api) or find_def_module(api)
        if not mod or not _tr.mod_to_path(mod):
            rows.append({"api": api, "module": mod or "?", "status": "UNRESOLVED",
                         "modules": 0, "lines": 0, "forbidden": []})
            continue
        try:
            mods, forb = _tr.trace(mod)
            lines = sum(x["lines"] for x in mods.values())
            cats = sorted({n.split(":")[-1] for f in forb for n in f["notes"]})
            rows.append({"api": api, "module": mod, "status": "CLEAN" if not forb else "FORBIDDEN",
                         "modules": len(mods), "lines": lines, "forbidden": cats})
        except Exception as e:
            rows.append({"api": api, "module": mod, "status": "ERROR:" + str(e)[:40],
                         "modules": 0, "lines": 0, "forbidden": []})
    clean = [r for r in rows if r["status"] == "CLEAN"]
    forb = [r for r in rows if r["status"] == "FORBIDDEN"]
    unres = [r for r in rows if r["status"] not in ("CLEAN", "FORBIDDEN")]
    clean.sort(key=lambda r: (r["lines"], r["modules"]))
    out = {"proven": len(PROVEN), "remaining": len(rows),
           "clean": clean, "forbidden": forb, "unresolved": unres}
    json.dump(out, open(os.path.join(ROOT, "_rank.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    sys.stderr.write(f"remaining={len(rows)} CLEAN={len(clean)} FORBIDDEN={len(forb)} UNRESOLVED={len(unres)}\n\n")
    sys.stderr.write("== CLEAN (sorted by closure size) ==\n")
    for r in clean:
        sys.stderr.write(f"  {r['lines']:5d}L {r['modules']:3d}m  {r['api']:35s} {r['module']}\n")
    sys.stderr.write("\n== FORBIDDEN ==\n")
    for r in forb:
        sys.stderr.write(f"  {r['api']:35s} {','.join(r['forbidden'])}\n")
    if unres:
        sys.stderr.write("\n== UNRESOLVED ==\n")
        for r in unres:
            sys.stderr.write(f"  {r['api']:35s} {r['status']} {r['module']}\n")


if __name__ == "__main__":
    main()
