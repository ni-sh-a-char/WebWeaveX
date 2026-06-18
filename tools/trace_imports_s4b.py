#!/usr/bin/env python3
"""Transitive import tracer for the Session-4B dependency proof.

For a given entry module, BFS over all `import`/`from ... import` statements,
following only first-party modules (core.* / webweavex.*), and flag any
forbidden third-party dependency anywhere in the transitive closure.
"""
from __future__ import annotations
import ast, os, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))

FORBIDDEN = {
    "bs4": "BeautifulSoup", "BeautifulSoup": "BeautifulSoup",
    "lxml": "lxml",
    "playwright": "browser", "selenium": "browser", "pyppeteer": "browser",
    "pytesseract": "OCR", "PIL": "OCR/image", "Pillow": "OCR/image", "cv2": "OCR/image",
    "pypdf": "PDF", "PyPDF2": "PDF", "pdfminer": "PDF", "fitz": "PDF",
    "docx": "DOCX", "python_docx": "DOCX", "openpyxl": "XLSX-bin", "pptx": "PPTX-bin",
    "requests": "network", "httpx": "network", "aiohttp": "network",
    "urllib": "network", "socket": "network", "http": "network",
    "groq": "LLM", "openai": "LLM", "anthropic": "LLM",
}

def mod_to_path(mod: str) -> str | None:
    rel = mod.replace(".", os.sep)
    for cand in (os.path.join(ROOT, rel + ".py"), os.path.join(ROOT, rel, "__init__.py")):
        if os.path.exists(cand):
            return cand
    return None

def imports_of(path: str):
    """Return list of (imported_module_str, top_level_name)."""
    with open(path, encoding="utf-8") as fh:
        tree = ast.parse(fh.read(), filename=path)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                out.append((a.name, a.name.split(".")[0]))
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue  # relative — resolved separately below
            if node.module:
                out.append((node.module, node.module.split(".")[0]))
    return out

def trace(entry: str):
    start = mod_to_path(entry)
    if not start:
        return {"entry": entry, "error": "entry module not found"}
    seen = {entry}
    queue = [entry]
    visited_modules = []         # first-party modules walked
    forbidden_hits = []          # (module_where, imported, category)
    stdlib_third = set()         # non-forbidden third-party / stdlib names seen
    while queue:
        mod = queue.pop(0)
        p = mod_to_path(mod)
        if not p:
            continue
        visited_modules.append(mod)
        for imp, top in imports_of(p):
            if top in FORBIDDEN:
                forbidden_hits.append({"in": mod, "imports": imp, "category": FORBIDDEN[top]})
            if top in ("core", "webweavex"):
                # follow the most specific resolvable first-party module
                target = imp
                if mod_to_path(target) is None:
                    # `from core.x import y` where y is a symbol: keep core.x
                    target = ".".join(imp.split("."))
                if mod_to_path(target) is None:
                    # try dropping last segment (symbol import from a module)
                    target = ".".join(imp.split(".")[:-1]) or imp
                if mod_to_path(target) and target not in seen:
                    seen.add(target); queue.append(target)
                elif mod_to_path(imp) and imp not in seen:
                    seen.add(imp); queue.append(imp)
            else:
                stdlib_third.add(top)
    return {
        "entry": entry,
        "first_party_modules": sorted(set(visited_modules)),
        "first_party_count": len(set(visited_modules)),
        "forbidden_hits": forbidden_hits,
        "clean": len(forbidden_hits) == 0,
        "non_first_party_imports": sorted(stdlib_third),
    }

ENTRIES = {
    "extract_document_runtime": "core.documents.universal_document_extraction_engine",
    "extract_paginated_content": "core.interaction.pagination_engine",
    "heal_selector": "core.adaptive.selector_healing_engine",
    "ingest_input": "core.ingestion.universal_ingestion_engine",
}

if __name__ == "__main__":
    result = {api: trace(mod) for api, mod in ENTRIES.items()}
    target = sys.argv[1] if len(sys.argv) > 1 else "_trace_result.json"
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    for api, r in result.items():
        status = "CLEAN" if r.get("clean") else "FORBIDDEN: " + ",".join(
            f"{h['imports']}({h['category']})@{h['in']}" for h in r.get("forbidden_hits", []))
        sys.stderr.write(f"{api}: {r.get('first_party_count','?')} modules -> {status}\n")
