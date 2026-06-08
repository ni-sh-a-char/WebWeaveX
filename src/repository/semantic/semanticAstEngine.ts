/**
 * Repository semantic AST extraction — faithful port of
 * core/repository/semantic/semantic_ast_engine.py.
 * Hand-written production module (protected); Python-AST analysis delegates
 * to the shared analyzer.
 */
import * as py from "../../runtime/pyCompat.js";
import { parsePythonAst } from "../../ast/pythonAstEngine.js";

const _LANG_PATTERNS: Record<string, string[]> = {
  python: ["\\bdef\\s+\\w+\\s*\\(", "\\bclass\\s+\\w+\\s*[:(]", "\\bimport\\s+\\w+"],
  javascript: ["\\bfunction\\s+\\w+\\s*\\(", "\\bconst\\s+\\w+\\s*=", "\\brequire\\("],
  typescript: ["\\binterface\\s+\\w+", "\\btype\\s+\\w+\\s*=", "\\bimport\\s+.+\\sfrom\\s+"],
  java: ["\\bpublic\\s+class\\s+\\w+", "\\bpackage\\s+\\w+[\\w.]*\\s*;"],
  kotlin: ["\\bfun\\s+\\w+\\s*\\(", "\\bclass\\s+\\w+", "\\bimport\\s+[\\w.]+"],
  dart: ["\\bimport\\s+'package:", "\\bclass\\s+\\w+", "\\bvoid\\s+main\\s*\\("],
  go: ["\\bpackage\\s+\\w+", "\\bfunc\\s+\\w+\\s*\\("],
  rust: ["\\bfn\\s+\\w+\\s*\\(", "\\buse\\s+[\\w:]+"],
};

function sortedSet(values: Set<string>): string[] {
  return py.sorted([...values].filter((v) => v.length > 0)) as string[];
}

function findAll(pattern: string, source: string): string[] {
  const out: string[] = [];
  const rx = new RegExp(pattern, "g");
  let m: RegExpExecArray | null;
  while ((m = rx.exec(source)) !== null) {
    out.push(m[1]!);
    
  }
  return out;
}

export function extractSemanticAst(text: string): Record<string, string[]> {
  const source = text || "";
  const languages = new Set<string>();
  for (const [lang, patterns] of Object.entries(_LANG_PATTERNS)) {
    if (patterns.some((p) => new RegExp(p).test(source))) languages.add(lang);
  }

  const symbols = new Set<string>();
  const imports = new Set<string>();
  const classes = new Set<string>();
  const interfaces = new Set<string>();
  const traits = new Set<string>();
  const functions = new Set<string>();
  const methods = new Set<string>();
  const decorators = new Set<string>();
  const annotations = new Set<string>();
  const generics = new Set<string>();
  const exports = new Set<string>();

  try {
    const tree = parsePythonAst(source) as {
      functions: { name: string }[];
      classes: { name: string }[];
      imports: ({ modules?: string[]; module?: string; names?: string[] })[];
    };
    languages.add("python");
    for (const c of tree.classes) {
      classes.add(c.name);
      symbols.add(c.name);
    }
    for (const f of tree.functions) {
      functions.add(f.name);
      symbols.add(f.name);
    }
    for (const imp of tree.imports) {
      if (Array.isArray(imp.modules)) {
        for (const mname of imp.modules) imports.add(mname);
      } else {
        imports.add(String(imp.module));
        for (const alias of imp.names!) symbols.add(alias);
      }
    }
  } catch {
    /* SyntaxError — not python */
  }

  for (const n of findAll("\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)", source)) classes.add(n);
  for (const n of findAll("\\binterface\\s+([A-Za-z_][A-Za-z0-9_]*)", source)) interfaces.add(n);
  for (const n of findAll("\\btrait\\s+([A-Za-z_][A-Za-z0-9_]*)", source)) traits.add(n);
  for (const n of findAll("\\b(?:def|function|fun|fn)\\s+([A-Za-z_][A-Za-z0-9_]*)", source)) functions.add(n);
  for (const n of findAll("\\b([A-Za-z_][A-Za-z0-9_]*)\\s*\\([^)]*\\)\\s*\\{", source)) methods.add(n);
  for (const n of findAll("\\bimport\\s+([A-Za-z0-9_./:*'-]+)", source)) imports.add(n);
  for (const n of findAll("\\brequire\\(['\"]([^'\"]+)['\"]\\)", source)) imports.add(n);
  for (const n of findAll(
    "\\bexport\\s+(?:default\\s+)?(?:class|function|const|let|var)?\\s*([A-Za-z_][A-Za-z0-9_]*)",
    source,
  )) exports.add(n);
  for (const n of findAll("@([A-Za-z_][A-Za-z0-9_]*)", source)) annotations.add(n);
  for (const n of findAll("\\b[A-Za-z_][A-Za-z0-9_]*<([A-Za-z0-9_, ?]+)>", source)) generics.add(n);
  for (const x of annotations) decorators.add(`@${x}`);

  for (const s of classes) symbols.add(s);
  for (const s of interfaces) symbols.add(s);
  for (const s of traits) symbols.add(s);
  for (const s of functions) symbols.add(s);
  for (const s of methods) symbols.add(s);

  return {
    languages: sortedSet(languages),
    symbols: sortedSet(symbols),
    imports: sortedSet(imports),
    classes: sortedSet(classes),
    interfaces: sortedSet(interfaces),
    traits: sortedSet(traits),
    functions: sortedSet(functions),
    methods: sortedSet(methods),
    decorators: sortedSet(decorators),
    annotations: sortedSet(annotations),
    generics: sortedSet(generics),
    exports: sortedSet(exports),
  };
}
