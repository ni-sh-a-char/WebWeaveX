#!/usr/bin/env python3
"""Generate src/publicApi.ts — the JavaScript public API surface that conforms
to the same specification as the Python `webweavex` package (RULE 15).

Resolves every public name in `origin/python:webweavex/__init__.py` __all__ to
its JavaScript implementation (re-export) or ports the package-level wrapper.
"""
from __future__ import annotations

import ast
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def camel(name: str) -> str:
    if name.startswith("__") and name.endswith("__"):
        return name
    if re.fullmatch(r"[A-Z0-9_]+", name):  # ALL_CAPS constant
        return name
    lead = len(name) - len(name.lstrip("_"))
    core = name[lead:]
    parts = core.split("_")
    out = parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:] if p)
    return "_" * lead + out


def pascal(name: str) -> str:
    parts = name.split("_")
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def py_init() -> str:
    r = subprocess.run(
        ["git", "show", "origin/python:webweavex/__init__.py"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
    )
    return r.stdout


def resolve_module(mod: str) -> str | None:
    """core.a.b_c -> relative src import path (without .js), probing file vs package."""
    if mod.startswith("webweavex."):
        return None  # package-level module, ported by hand below
    parts = mod.split(".")
    if parts[0] != "core":
        return None
    rest = parts[1:]
    # module file: src/a/b/camel(last).ts
    file_rel = "/".join(rest[:-1] + [camel(rest[-1])]) if rest else ""
    if (SRC / (file_rel + ".ts")).exists():
        return "./" + file_rel + ".js"
    # package barrel: src/a/b/index.ts
    pkg_rel = "/".join(rest)
    if (SRC / pkg_rel / "index.ts").exists():
        return "./" + pkg_rel + "/index.js"
    # class-bearing module named after a Pascal export (rare)
    if (SRC / (file_rel + ".ts")).exists():
        return "./" + file_rel + ".js"
    return None


def index_exported_names() -> set[str]:
    """Names already exported by src/index.ts — publicApi must not shadow these
    (they are the established, certified JS public exports)."""
    idx = (SRC / "index.ts").read_text(encoding="utf-8")
    names: set[str] = set()
    for m in re.finditer(r"export\s*(?:type\s*)?\{([^}]*)\}", idx):
        for part in m.group(1).split(","):
            tail = part.split(" as ")[-1].strip()
            if tail:
                names.add(tail)
    for m in re.finditer(r"export\s+(?:const|let|function|class)\s+([A-Za-z0-9_]+)", idx):
        names.add(m.group(1))
    # names pulled in by `export * from "./connectors/index.js"`
    conn = SRC / "connectors" / "index.ts"
    if conn.exists():
        ct = conn.read_text(encoding="utf-8")
        for m in re.finditer(r"export\s*\{([^}]*)\}", ct):
            for part in m.group(1).split(","):
                tail = part.split(" as ")[-1].strip()
                if tail:
                    names.add(tail)
    return names


def main() -> int:
    src = py_init()
    tree = ast.parse(src)
    index_names = index_exported_names()
    allset: set[str] = set()
    imports: list[tuple[str, str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "__all__":
                    allset = set(ast.literal_eval(node.value))
        if isinstance(node, ast.ImportFrom) and node.module:
            for a in node.names:
                imports.append((node.module, a.name, a.asname or a.name))

    bound: dict[str, tuple[str, str]] = {}
    for mod, orig, local in imports:
        if local in allset:
            bound[local] = (mod, orig)

    def file_exports(rel_js: str, name: str) -> bool:
        """Does the src file at this relative .js import path export `name`?"""
        p = SRC / (rel_js[2:].rsplit(".js", 1)[0] + ".ts")
        if not p.exists():
            return False
        txt = p.read_text(encoding="utf-8", errors="replace")
        if re.search(rf"export\s+(?:async\s+)?(?:function|const|let|class)\s+{re.escape(name)}\b", txt):
            return True
        # re-export forms: export { name } / export { x as name } / export * (assume yes only on explicit)
        for m in re.finditer(r"export\s*\{([^}]*)\}", txt):
            for part in m.group(1).split(","):
                tail = part.split(" as ")[-1].strip()
                if tail == name:
                    return True
        return False

    def find_submodule(pkg_rel: str, name: str) -> str | None:
        """Search a package dir for the submodule that exports `name`."""
        base = SRC / pkg_rel
        if not base.exists():
            return None
        for p in sorted(base.rglob("*.ts")):
            if p.name == "index.ts":
                continue
            rel = "./" + str(p.relative_to(SRC)).replace("\\", "/")[:-3] + ".js"
            if file_exports(rel, name):
                return rel
        return None

    # group bound names by resolved src module, preserving (jsExport, publicName)
    by_target: dict[str, list[tuple[str, str]]] = {}
    unresolved: list[str] = []
    for public, (mod, orig) in sorted(bound.items()):
        target = resolve_module(mod)
        if target is None:
            unresolved.append(f"{public} <- {mod}.{orig}")
            continue
        js_export = camel(orig)
        public_js = camel(public)
        # never shadow a name index.ts already exports — those established
        # exports are certified and authoritative; publicApi only ADDS the
        # genuinely-missing public names
        if public_js in index_names:
            continue
        # if the resolved target (often a package barrel) doesn't actually
        # export the name, repoint to the submodule that does
        if not file_exports(target, js_export):
            pkg_rel = mod.split(".", 1)[1].replace(".", "/") if mod.startswith("core.") else ""
            alt = find_submodule(pkg_rel, js_export) if pkg_rel else None
            if alt:
                target = alt
            else:
                unresolved.append(f"{public} <- {mod}.{orig} (export {js_export} not found)")
                continue
        by_target.setdefault(target, []).append((js_export, public_js))

    lines: list[str] = [
        "/**",
        " * WebWeaveX JavaScript public API surface.",
        " *",
        " * @generated by tools/convergence/build_public_api.py — conforms to the",
        " * same specification as the Python `webweavex` package public API",
        " * (origin/python:webweavex/__init__.py __all__). Hand-edit the generator,",
        " * not this file. Re-exports resolve to certified `src/` implementations.",
        " */",
        'import { ingestInput } from "./ingestion/universalIngestionEngine.js";',
        'import { extractPdfText } from "./files/pdfExtractionEngine.js";',
        'import { extractDocxText } from "./files/docxExtractionEngine.js";',
        'import { extractMultimodal as _extractMultimodal } from "./multimodal/universalMultimodalExtractionEngine.js";',
        'import { extractArchive } from "./archive/archiveExtractionEngine.js";',
        'import { extractHtmlFile } from "./files/htmlFileExtractionEngine.js";',
        'import { compileMediaIr } from "./ir/mediaIr.js";',
        'import { extractRepository as _extractRepositoryPath } from "./repository/universalRepositoryExtractionEngine.js";',
        'import { extract as _extract } from "./extract/pipeline.js";',
        'import { crawl as _crawl } from "./crawling/crawlerEngine.js";',
        'import { analyzeGraph } from "./intelligence/graphAnalyzer.js";',
        'import { queryGraph as _queryGraphIr } from "./query/graphQueryEngine.js";',
        'import { queryDocuments as _queryDocumentIr } from "./query/documentQueryEngine.js";',
        'import { queryKnowledge as _queryKnowledgeIr } from "./query/ontologyQueryEngine.js";',
        'import { queryRepository as _queryRepositoryIr } from "./query/repositoryQueryEngine.js";',
        'import { compileDocumentIr } from "./ir/documentIr.js";',
        'import { compileRepositoryIr } from "./ir/repositoryIr.js";',
        "",
        "/* ---- re-exported certified implementations (spec-equivalent names) ---- */",
        "",
    ]
    for target in sorted(by_target):
        specs = sorted(set(by_target[target]))
        clause = ", ".join(j if j == p else f"{j} as {p}" for j, p in specs)
        lines.append(f'export {{ {clause} }} from "{target}";')

    # package-level convenience wrappers (defined in webweavex/__init__.py body)
    lines += [
        "",
        "/* ---- package-level convenience API (ported from webweavex/__init__.py) ---- */",
        "",
        'export const version = "2.0.0";',
        "",
        "export function universalExtract(path: string): Record<string, unknown> {",
        "  const info = ingestInput(path) as Record<string, unknown>;",
        '  const inputType = info["input_type"];',
        '  if (inputType === "image") {',
        "    const multimodal = _extractMultimodal(path) as Record<string, unknown>;",
        '    return { ingestion: info, extraction: multimodal, multimodal_ir: multimodal["multimodal_ir"] ?? {}, bounded: true };',
        "  }",
        '  if (inputType === "repository") {',
        "    const repo = _extractRepositoryPath(path) as Record<string, unknown>;",
        '    return { ingestion: info, extraction: repo, repository_ir: repo["repository_ir"] ?? {}, bounded: true };',
        "  }",
        "  let payload: Record<string, unknown> | null = null;",
        '  if (inputType === "pdf") payload = extractPdfText(path) as Record<string, unknown>;',
        '  else if (inputType === "docx") payload = extractDocxText(path) as Record<string, unknown>;',
        '  else if (inputType === "archive") payload = extractArchive(path) as Record<string, unknown>;',
        '  else if (inputType === "html") payload = extractHtmlFile(path) as Record<string, unknown>;',
        "  if (payload === null) {",
        '    return { unsupported: true, input_type: inputType, ingestion: info, bounded: true };',
        "  }",
        "  return { ingestion: info, extraction: payload, media_ir: compileMediaIr(payload), bounded: true };",
        "}",
        "",
        "export function analyze(inputData: unknown, edges: unknown = null): unknown {",
        "  if (edges !== null && edges !== undefined) return analyzeGraph(inputData, edges);",
        "  const result = _extract(inputData as never) as Record<string, any>;",
        '  const graph = (result?.relationships?.execution_graph ?? {}) as Record<string, any>;',
        "  return analyzeGraph(graph.nodes ?? [], graph.edges ?? []);",
        "}",
        "",
        "export function crawl(url: string, opts: Record<string, unknown> = {}): unknown {",
        "  return _crawl(url, opts as never);",
        "}",
        "",
        "export async function crawlAsync(url: string, opts: Record<string, unknown> = {}): Promise<unknown> {",
        "  return _crawl(url, opts as never);",
        "}",
        "",
        "export function extractRecursive(url: string, opts: Record<string, unknown> = {}): Record<string, any> {",
        "  const crawled = _crawl(url, opts as never) as Record<string, any>;",
        "  const out = _extract(url as never) as Record<string, any>;",
        "  out.metadata = out.metadata ?? {};",
        "  out.metadata.crawl = { visited: crawled?.visited ?? [], discovered: crawled?.discovered ?? [] };",
        "  out.repository = out?.content?.repository ?? {};",
        "  out.documents = out?.content?.documents ?? {};",
        "  return out;",
        "}",
        "",
        "export function queryGraph(result: Record<string, any> | null = null, node = \"\", graph: Record<string, any> | null = null): unknown {",
        "  if (graph !== null && graph !== undefined) return _queryGraphIr(graph, node);",
        "  if (result === null || result === undefined) return _queryGraphIr({}, node);",
        '  const g = "relationships" in result ? (result?.relationships?.execution_graph ?? {}) : result;',
        "  return _queryGraphIr(g, node);",
        "}",
        "",
        "export function queryRepo(result: Record<string, any>): unknown {",
        "  return result?.content?.repository ?? {};",
        "}",
        "",
        "export function queryRepository(result: Record<string, any> | null = null, source = \"\", path = \"\", opts: Record<string, any> = {}): unknown {",
        "  if (result !== null && result !== undefined && !source) return queryRepo(result);",
        "  return _queryRepositoryIr(source, path, opts.files);",
        "}",
        "",
        "export function queryKnowledge(result: Record<string, any> | null = null, entities: unknown = null, edges: unknown = null): unknown {",
        "  if (entities !== null || edges !== null) return _queryKnowledgeIr((entities as unknown[]) ?? [], (edges as unknown[]) ?? []);",
        "  const content = (result && typeof result === \"object\" ? result.content : {}) ?? {};",
        "  return { knowledge_v2: content.knowledge_v2 ?? {}, knowledge_v18: content.knowledge_reconstruction_v18 ?? {} };",
        "}",
        "",
        "export function queryDocuments(result: Record<string, any> | null = null, text = \"\"): unknown {",
        "  if (text) return _queryDocumentIr(text);",
        "  if (result !== null && result !== undefined) return result?.content?.documents ?? {};",
        "  return _queryDocumentIr(\"\");",
        "}",
        "",
        "export function compileDocument(text: string): unknown {",
        "  return compileDocumentIr(text);",
        "}",
        "",
        "export function compileRepository(source: string, path = \"\", opts: Record<string, any> = {}): unknown {",
        "  return compileRepositoryIr(source, path, opts.files);",
        "}",
        "",
    ]

    out = SRC / "publicApi.ts"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out} — {sum(len(v) for v in by_target.values())} re-exports across {len(by_target)} modules")
    if unresolved:
        print("UNRESOLVED (need attention):")
        for u in unresolved:
            print("  ", u)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
