/**
 * Converted from Python: core/repository/ast/ast_cognition_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { parseGoAst } from "./goAstEngine.js";
import { parseJavaAst } from "./javaAstEngine.js";
import { parseJavascriptAst } from "./javascriptAstEngine.js";
import { parsePythonAst } from "./pythonAstEngine.js";
import { parseRustAst } from "./rustAstEngine.js";

let _PARSERS: any = {"python": parsePythonAst, "javascript": parseJavascriptAst, "typescript": parseJavascriptAst, "go": parseGoAst, "rust": parseRustAst, "java": parseJavaAst};
let _EXT: any = {".py": "python", ".js": "javascript", ".jsx": "javascript", ".ts": "typescript", ".tsx": "typescript", ".go": "go", ".rs": "rust", ".java": "java"};
export function analyzeSourceAst(source: any, path: any = "", language: any = ""): any {
  var lang: any = py.or2(language, () => (py.get(_EXT, String(py.path(path).suffix).toLowerCase(), "python")));
  var parser: any = py.get(_PARSERS, lang, parsePythonAst);
  var result: any = parser(source, path);
  return {...(result), "call_graph": py.get(result, "calls", []), "dependencies": py.get(result, "imports", []), "semantic_topology": {"nodes": py.len(py.get(result, "nodes", [])), "imports": py.len(py.get(result, "imports", [])), "calls": py.len(py.get(result, "calls", []))}, "deterministic": true, "bounded": true};
}
export { parseGoAst, parseJavaAst, parseJavascriptAst, parsePythonAst, parseRustAst };
