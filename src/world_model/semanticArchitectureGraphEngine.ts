/**
 * Converted from Python: core/world_model/semantic_architecture_graph_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeImports } from "./_normalize.js";

export function buildSemanticArchitectureGraph(repository_irs: any): any {
  var nodes: any[] = [];
  var edges: any[] = [];
  var ir: any;
  for (ir of py.iter(repository_irs)) {
    var path: any = py.get(ir, "path");
    py.listAppend(nodes, {"id": path, "kind": "repository_file"});
    var semantic_ast: any = py.get(ir, "semantic_ast", {});
    var item: any;
    for (item of py.iter(normalizeImports(semantic_ast))) {
      var target: any = py.get(item, "module");
      if (py.truthy(target)) {
        py.listAppend(edges, {"from": path, "to": target, "relation": "architectural_dependency"});
      }
    }
  }
  return {"nodes": py.sorted(nodes, {key: ((x: any) => py.toStr(py.at(x, "id"))) as (item: any) => any}), "edges": py.sorted(edges, {key: ((x: any) => [py.toStr(py.at(x, "from")), py.toStr(py.at(x, "to"))]) as (item: any) => any})};
}
export { normalizeImports };
