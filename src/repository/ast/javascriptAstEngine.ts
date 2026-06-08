/**
 * Converted from Python: core/repository/ast/javascript_ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";
import { parseAst } from "../../parsers/astEngine.js";

export function parseJavascriptAst(source: any, path: any = ""): any {
  var imports: any[] = [];
  var calls: any[] = [];
  var nodes: any[] = [];
  var match: any;
  for (match of py.iter(py.reFinditer("import\\s+.*?from\\s+['\\\"]([^'\\\"]+)['\\\"]", source, ""))) {
    py.listAppend(imports, {"module": match.group(1), "kind": "es_import"});
  }
  for (match of py.iter(py.reFinditer("function\\s+(\\w+)", source, ""))) {
    py.listAppend(nodes, {"name": match.group(1), "kind": "function"});
  }
  for (match of py.iter(py.reFinditer("class\\s+(\\w+)", source, ""))) {
    py.listAppend(nodes, {"name": match.group(1), "kind": "class"});
  }
  for (match of py.iter(py.reFinditer("(\\w+)\\s*\\(", source, ""))) {
    py.listAppend(calls, {"target": match.group(1), "kind": "call"});
  }
  var ts: any = parseAst(source, "javascript");
  if (py.truthy(py.get(ts, "nodes"))) {
    nodes = py.get(ts, "nodes", nodes);
  }
  return {"language": "javascript", "path": path, "nodes": py.slice(py.sorted(nodes, {key: ((item: any) => py.at(item, "name")) as (item: any) => any}), null, 5000), "imports": py.slice(py.sorted(imports, {key: ((item: any) => py.at(item, "module")) as (item: any) => any}), null, 2000), "calls": py.slice(py.sorted(calls, {key: ((item: any) => py.at(item, "target")) as (item: any) => any}), null, 5000), "bounded": true};
}
export { parseAst };
