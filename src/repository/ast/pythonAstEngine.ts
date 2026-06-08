/**
 * Repository Python AST summary — faithful port of
 * core/repository/ast/python_ast_engine.py.
 * Hand-written production module (protected).
 */
import * as py from "../../runtime/pyCompat.js";
import { parsePythonAst as analyze } from "../../ast/pythonAstEngine.js";

const PY_KEYWORDS = new Set([
  "if", "elif", "while", "for", "return", "yield", "assert", "del",
  "with", "not", "and", "or", "in", "is", "lambda", "def", "class",
  "except", "raise", "from", "import", "print_stmt",
]);

export function parsePythonAst(source: string, path = ""): Record<string, unknown> {
  let summary: Record<string, unknown>;
  try {
    summary = analyze(String(source));
  } catch (exc) {
    return {
      language: "python",
      parse_error: py.toStr(exc).replace("<unknown>", path || "<python>"),
      nodes: [],
      imports: [],
      calls: [],
      bounded: true,
    };
  }

  const imports: { module: string; kind: string }[] = [];
  for (const imp of summary.imports as Record<string, unknown>[]) {
    if (Array.isArray(imp.modules)) {
      for (const m of imp.modules) imports.push({ module: String(m), kind: "import" });
    } else {
      imports.push({ module: String(imp.module), kind: "import_from" });
    }
  }

  const nodes: { name: string; kind: string }[] = [];
  for (const f of summary.functions as Record<string, unknown>[]) {
    nodes.push({ name: String(f.name), kind: "FunctionDef" });
  }
  for (const c of summary.classes as Record<string, unknown>[]) {
    nodes.push({ name: String(c.name), kind: "ClassDef" });
  }

  // ast.Call approximation: identifier followed by "(" that is not a keyword
  // or a def/class header
  const calls: { target: string; kind: string }[] = [];
  const src = String(source);
  const callRe = /([A-Za-z_][A-Za-z0-9_]*)\s*\(/g;
  let m: RegExpExecArray | null;
  while ((m = callRe.exec(src)) !== null) {
    const name = m[1]!;
    if (PY_KEYWORDS.has(name)) continue;
    const before = src.slice(Math.max(0, m.index - 10), m.index);
    if (/\b(?:def|class)\s+$/.test(before)) continue;
    calls.push({ target: name, kind: "call" });
  }

  return {
    language: "python",
    nodes: py.sorted(nodes, { key: (x) => (x as { name: string }).name }) as unknown[],
    imports: py.sorted(imports, { key: (x) => (x as { module: string }).module }) as unknown[],
    calls: (py.sorted(calls, { key: (x) => (x as { target: string }).target }) as unknown[]).slice(0, 5000),
    bounded: true,
  };
}
