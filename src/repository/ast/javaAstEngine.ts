/**
 * Converted from Python: core/repository/ast/java_ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function parseJavaAst(source: any, path: any = ""): any {
  var imports: any = py.iter(py.reFinditer("import\\s+([\\w.]+);", source, "")).map((m: any) => ({"module": m.group(1), "kind": "java_import"}));
  var nodes: any = py.iter(py.reFinditer("class\\s+(\\w+)", source, "")).map((m: any) => ({"name": m.group(1), "kind": "class"}));
  var calls: any = py.iter(py.reFinditer("(\\w+)\\s*\\(", source, "")).map((m: any) => ({"target": m.group(1), "kind": "call"}));
  return {"language": "java", "path": path, "nodes": py.slice(py.sorted(nodes, {key: ((item: any) => py.at(item, "name")) as (item: any) => any}), null, 5000), "imports": py.slice(py.sorted(imports, {key: ((item: any) => py.at(item, "module")) as (item: any) => any}), null, 2000), "calls": py.slice(py.sorted(calls, {key: ((item: any) => py.at(item, "target")) as (item: any) => any}), null, 5000), "bounded": true};
}
