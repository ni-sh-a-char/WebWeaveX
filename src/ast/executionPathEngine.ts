/**
 * Converted from Python: core/ast/execution_path_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_EXECUTION_PATHS: any = 100;
export function reconstructExecutionPaths(cfg: any): any {
  var paths: any[] = [];
  var nodes: any = py.get(cfg, "nodes", []);
  var node: any;
  for (node of py.iter(py.slice(nodes, null, MAX_EXECUTION_PATHS))) {
    py.listAppend(paths, [py.at(node, "id")]);
  }
  return {"paths": paths, "path_count": py.len(paths), "bounded": true};
}
