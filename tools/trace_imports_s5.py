#!/usr/bin/env python3
"""Detailed transitive closure for compile_document (Session 5 dependency proof)."""
from __future__ import annotations
import ast, os, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))

FORBIDDEN = {
    "bs4": "BeautifulSoup", "BeautifulSoup": "BeautifulSoup", "lxml": "lxml",
    "playwright": "browser", "selenium": "browser", "pyppeteer": "browser",
    "pytesseract": "OCR", "PIL": "OCR/image", "cv2": "OCR/image",
    "pypdf": "PDF", "PyPDF2": "PDF", "pdfminer": "PDF", "fitz": "PDF",
    "docx": "DOCX", "openpyxl": "XLSX-bin", "pptx": "PPTX-bin",
    "requests": "network", "httpx": "network", "aiohttp": "network",
    "urllib": "network", "socket": "network", "http": "network",
    "groq": "LLM", "openai": "LLM", "anthropic": "LLM",
}
# stdlib modules that may legitimately appear (deterministic)
STD_OK = {"__future__", "typing", "re", "collections", "dataclasses", "math",
          "json", "itertools", "functools", "enum", "abc", "copy", "string"}


def mod_to_path(mod):
    rel = mod.replace(".", os.sep)
    for cand in (os.path.join(ROOT, rel + ".py"), os.path.join(ROOT, rel, "__init__.py")):
        if os.path.exists(cand):
            return cand
    return None


def parse(path):
    with open(path, encoding="utf-8-sig") as fh:
        src = fh.read()
    tree = ast.parse(src, filename=path)
    fp, tp, fns = [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                top = a.name.split(".")[0]
                (fp if top in ("core", "webweavex") else tp).append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level and node.level > 0:
                continue
            if node.module:
                top = node.module.split(".")[0]
                (fp if top in ("core", "webweavex") else tp).append(node.module)
        elif isinstance(node, ast.FunctionDef):
            fns.append(node.name)
    return src.count("\n") + 1, fp, tp, fns


def classify(third):
    cats = set()
    for t in third:
        top = t.split(".")[0]
        if top in FORBIDDEN:
            cats.add("FORBIDDEN:" + FORBIDDEN[top])
        elif top not in STD_OK:
            cats.add("third?:" + top)
    if any(c.startswith("FORBIDDEN") for c in cats):
        return "FORBIDDEN", sorted(cats)
    if cats:
        return "REVIEW", sorted(cats)
    return "PURE", []


def trace(entry):
    seen, queue, modules = {entry}, [entry], {}
    forbidden = []
    while queue:
        mod = queue.pop(0)
        p = mod_to_path(mod)
        if not p:
            continue
        lines, fp, tp, fns = parse(p)
        cls, notes = classify(tp)
        modules[mod] = {"path": os.path.relpath(p, ROOT).replace("\\", "/"),
                        "lines": lines, "functions": fns, "third_party": sorted(set(tp)),
                        "first_party": sorted(set(fp)), "class": cls, "notes": notes}
        if cls == "FORBIDDEN":
            forbidden.append({"module": mod, "notes": notes})
        for imp in fp:
            for target in (imp, ".".join(imp.split(".")[:-1])):
                if mod_to_path(target) and target not in seen:
                    seen.add(target); queue.append(target); break
    return modules, forbidden


if __name__ == "__main__":
    modules, forbidden = trace("core.ir.document_ir")
    total_lines = sum(m["lines"] for m in modules.values())
    total_fns = sum(len(m["functions"]) for m in modules.values())
    result = {"entry": "core.ir.document_ir (compile_document_ir)",
              "module_count": len(modules), "total_lines": total_lines,
              "total_functions": total_fns, "forbidden": forbidden, "modules": modules}
    out = sys.argv[1] if len(sys.argv) > 1 else "_trace_s5.json"
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
    sys.stderr.write(f"modules={len(modules)} lines={total_lines} fns={total_fns} "
                     f"forbidden={len(forbidden)}\n")
    for m, info in sorted(modules.items()):
        if info["class"] != "PURE":
            sys.stderr.write(f"  {info['class']}: {m} {info['notes']}\n")
