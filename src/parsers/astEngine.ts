/**
 * Converted from Python: core/parsers/ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

const ast: any = py.astModule;
export let MAX_AST_NODES: any = 100000;
export function parseAst(source: any, language: any): any {
  var lang: any = String(py.or2(language, () => ("text"))).toLowerCase();
  if (py.eq(lang, "python")) {
    return _pythonAst(source);
  }
  return _treeSitterAst(source, lang);
}
export function _pythonAst(source: any): any {
  try {
    var tree: any = ast.parse(py.or2(source, () => ("")));
  } catch (_e: any) {
    return {"language": "python", "nodes": [], "parse_error": true};
  }
  var nodes: any[] = [];
  var stack: any = [tree];
  var idx: any = 0;
  while ((py.truthy(stack) && py.lt(idx, MAX_AST_NODES))) {
    var node: any = py.pop(stack);
    idx = py.add(idx, 1);
    py.listAppend(nodes, {"id": idx, "kind": (Array.isArray(node) ? "list" : node === null ? "NoneType" : typeof node === "string" ? "str" : typeof node === "boolean" ? "bool" : typeof node === "number" ? (Number.isInteger(node) ? "int" : "float") : node instanceof Set ? "set" : node instanceof Error ? ((node as Error).name || "Exception") : typeof node === "object" ? ((node as object).constructor === Object ? "dict" : (node as object).constructor?.name ?? "object") : typeof node)});
    py.extend(stack, py.reversed([...py.iter(ast.iter_child_nodes(node))]));
  }
  return {"language": "python", "nodes": nodes};
}
export function _treeSitterAst(source: any, language: any): any {
  var get_parser: any = null;
  return {"language": language, "nodes": [], "parse_error": true};
}
