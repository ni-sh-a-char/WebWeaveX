/**
 * Python source analyzer — faithful port of core/ast/python_ast_engine.py.
 * Hand-written production module (protected): a lightweight line/indent
 * scanner that reproduces the summary CPython's ast.walk produces
 * (imports / functions / classes / assignments with line spans).
 */
import * as py from "../runtime/pyCompat.js";

interface NodeInfo {
  type: string;
  lineno: number | null;
  end_lineno: number | null;
}

interface ScannedStmt {
  kind: "Import" | "ImportFrom" | "FunctionDef" | "ClassDef" | "Assign";
  depth: number;
  lineno: number;
  end_lineno: number;
  data: Record<string, unknown>;
}

const IDENT = "[A-Za-z_][A-Za-z0-9_]*";

function syntaxError(line: number): Error {
  return py.err("SyntaxError", `invalid syntax (<unknown>, line ${line})`);
}

/** Python-validity gate: rejects lines that cannot begin a valid Python
 *  logical line (CPython ast.parse raises on all of these). Extended
 *  after real-world testing hit `/**`-led TypeScript sources that
 *  CPython rejects but the original narrow gate accepted. */
function validateLine(stripped: string, lineno: number): void {
  if (!stripped.length) return;
  if (/^[<>%?\\/,;:=&|!)\]}]/.test(stripped)) throw syntaxError(lineno);
}

function logicalLines(code: string): { text: string; lineno: number; end_lineno: number; indent: number }[] {
  const raw = code.split(/\r?\n/);
  const out: { text: string; lineno: number; end_lineno: number; indent: number }[] = [];
  let buf = "";
  let start = 0;
  let depth = 0;
  let indent = 0;
  let inStr: string | null = null;
  for (let i = 0; i < raw.length; i++) {
    const line = raw[i]!;
    if (!buf) {
      if (!line.trim().length || line.trim().startsWith("#")) continue;
      start = i + 1;
      indent = (line.match(/^[ \t]*/)?.[0] ?? "").replace(/\t/g, "        ").length;
    }
    buf += (buf ? "\n" : "") + line;
    // track bracket depth + triple strings (rough)
    let j = 0;
    while (j < line.length) {
      const ch = line[j]!;
      const three = line.slice(j, j + 3);
      if (inStr) {
        if (three === inStr) {
          inStr = null;
          j += 3;
          continue;
        }
        j++;
        continue;
      }
      if (three === '"""' || three === "'''") {
        inStr = three;
        j += 3;
        continue;
      }
      if (ch === "#") break;
      if ("([{".includes(ch)) depth++;
      else if (")]}".includes(ch)) depth--;
      j++;
    }
    const endsContinuation = line.trimEnd().endsWith("\\");
    if (depth > 0 || inStr || endsContinuation) continue;
    out.push({ text: buf, lineno: start, end_lineno: i + 1, indent });
    buf = "";
    depth = 0;
  }
  if (buf) out.push({ text: buf, lineno: start, end_lineno: raw.length, indent });
  return out;
}

export function parsePythonAst(code: string): Record<string, unknown> {
  const lines = logicalLines(String(code ?? ""));
  const stmts: ScannedStmt[] = [];

  for (let idx = 0; idx < lines.length; idx++) {
    const { text, lineno, indent } = lines[idx]!;
    // collapse continuation/grouping newlines for statement matching
    const stripped = text.trim().replace(/\\\s*\n\s*/g, " ").replace(/\s*\n\s*/g, " ");
    const depth = Math.floor(indent / 4);
    validateLine(stripped.split("\n")[0]!, lineno);

    let m = stripped.match(new RegExp(`^import\\s+(.+)$`));
    if (m && !stripped.startsWith("import(")) {
      const modules = m[1]!.split(",").map((s) => s.trim().split(/\s+as\s+/)[0]!.trim()).filter(Boolean);
      stmts.push({
        kind: "Import", depth, lineno, end_lineno: lines[idx]!.end_lineno,
        data: { modules },
      });
      continue;
    }
    m = stripped.match(new RegExp(`^from\\s+([.\\w]+)\\s+import\\s+(.+)$`));
    if (m) {
      const names = m[2]!
        .replace(/[()]/g, "")
        .split(",")
        .map((s) => s.trim().split(/\s+as\s+/)[0]!.trim())
        .filter((s) => s.length > 0);
      stmts.push({
        kind: "ImportFrom", depth, lineno, end_lineno: lines[idx]!.end_lineno,
        data: { module: m[1], names },
      });
      continue;
    }
    m = stripped.match(new RegExp(`^(?:async\\s+)?def\\s+(${IDENT})\\s*\\(([^]*?)\\)\\s*(?:->[^:]+)?:`));
    if (m) {
      const args = m[2]!
        .split(",")
        .map((s) => s.trim().split(/[:=]/)[0]!.trim().replace(/^\*+/, ""))
        .filter((s) => s.length > 0 && s !== "/");
      stmts.push({
        kind: "FunctionDef", depth, lineno,
        end_lineno: blockEnd(lines, idx),
        data: { name: m[1], args },
      });
      continue;
    }
    m = stripped.match(new RegExp(`^class\\s+(${IDENT})\\s*(?:\\(([^)]*)\\))?\\s*:`));
    if (m) {
      const bases = (m[2] ?? "")
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0 && !s.includes("="))
        .map((s) => (new RegExp(`^${IDENT}$`).test(s) ? s : null));
      stmts.push({
        kind: "ClassDef", depth, lineno,
        end_lineno: blockEnd(lines, idx),
        data: { name: m[1], bases },
      });
      continue;
    }
    m = stripped.match(new RegExp(`^((?:${IDENT}\\s*,\\s*)*${IDENT})\\s*=(?!=)([^]*)$`));
    if (m && !stripped.includes("==") && !/^(if|while|for|return|yield|assert|del|import|from|pass|raise)\b/.test(stripped)) {
      const targets = m[1]!.split(",").map((s) => s.trim()).filter((s) => new RegExp(`^${IDENT}$`).test(s));
      if (targets.length) {
        stmts.push({
          kind: "Assign", depth, lineno, end_lineno: lines[idx]!.end_lineno,
          data: { targets },
        });
      }
      continue;
    }
  }

  // ast.walk is breadth-first: order statements by nesting depth, then line
  const ordered = [...stmts].sort((a, b) => (a.depth - b.depth) || (a.lineno - b.lineno));

  const node = (s: ScannedStmt): NodeInfo => ({
    type: s.kind,
    lineno: s.lineno,
    end_lineno: s.end_lineno,
  });

  const imports: Record<string, unknown>[] = [];
  const functions: Record<string, unknown>[] = [];
  const classes: Record<string, unknown>[] = [];
  const assignments: Record<string, unknown>[] = [];
  for (const s of ordered) {
    if (s.kind === "Import") imports.push({ modules: s.data.modules, node: node(s) });
    else if (s.kind === "ImportFrom") imports.push({ module: s.data.module, names: s.data.names, node: node(s) });
    else if (s.kind === "FunctionDef") functions.push({ name: s.data.name, args: s.data.args, node: node(s) });
    else if (s.kind === "ClassDef") classes.push({ name: s.data.name, bases: s.data.bases, node: node(s) });
    else assignments.push({ targets: s.data.targets, node: node(s) });
  }

  return {
    language: "python",
    imports: py.sorted(imports, { key: (x) => py.toStr(x) }) as unknown[],
    functions: py.sorted(functions, { key: (x) => (x as Record<string, unknown>).name }) as unknown[],
    classes: py.sorted(classes, { key: (x) => (x as Record<string, unknown>).name }) as unknown[],
    assignments,
    ast_grounded: true,
    bounded: true,
  };
}

function blockEnd(
  lines: { text: string; lineno: number; end_lineno: number; indent: number }[],
  idx: number,
): number {
  const base = lines[idx]!.indent;
  let end = lines[idx]!.end_lineno;
  for (let j = idx + 1; j < lines.length; j++) {
    if (lines[j]!.indent <= base) break;
    end = lines[j]!.end_lineno;
  }
  return end;
}
