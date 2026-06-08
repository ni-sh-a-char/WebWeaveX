/**
 * Converted from Python: core/repository/ast/rust_ast_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../../runtime/pyCompat.js";

export function parseRustAst(source: any, path: any = ""): any {
  var nodes: any = py.iter(py.reFinditer("fn\\s+(\\w+)", source, "")).map((m: any) => ({"name": m.group(1), "kind": "fn"}));
  var imports: any = py.iter(py.reFinditer("use\\s+([^;]+);", source, "")).map((m: any) => ({"module": m.group(1), "kind": "use"}));
  return {"language": "rust", "path": path, "nodes": py.slice(py.sorted(nodes, {key: ((item: any) => py.at(item, "name")) as (item: any) => any}), null, 5000), "imports": py.slice(py.sorted(imports, {key: ((item: any) => py.at(item, "module")) as (item: any) => any}), null, 2000), "calls": [], "bounded": true};
}
