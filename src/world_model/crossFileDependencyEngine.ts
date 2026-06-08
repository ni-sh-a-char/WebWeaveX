/**
 * Converted from Python: core/world_model/cross_file_dependency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { normalizeImports } from "./_normalize.js";

export function buildCrossFileDependencies(repository_irs: any): any {
  var edges: any[] = [];
  var known_paths: any = py.toSet(py.iter(repository_irs).map((ir: any) => py.get(ir, "path")));
  var ir: any;
  for (ir of py.iter(repository_irs)) {
    var source: any = py.get(ir, "path");
    var semantic_ast: any = py.get(ir, "semantic_ast", {});
    var item: any;
    for (item of py.iter(normalizeImports(semantic_ast))) {
      var target: any = py.get(item, "module");
      if (py.contains(known_paths, target)) {
        py.listAppend(edges, {"from": source, "to": target, "relation": "cross_file_dependency"});
      }
    }
  }
  return {"edges": py.sorted(edges, {key: ((x: any) => [py.toStr(py.at(x, "from")), py.toStr(py.at(x, "to"))]) as (item: any) => any})};
}
export { normalizeImports };
