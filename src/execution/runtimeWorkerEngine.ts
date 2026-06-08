/**
 * Converted from Python: core/execution/runtime_worker_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeWorkers(nodes: any): any {
  var workers: any[] = [];
  var index: any;
  var node: any;
  for ([index, node] of py.enumerate(py.slice(nodes, null, 1000))) {
    py.listAppend(workers, {"worker_id": py.toStr(py.get(node, "worker_id", py.get(node, "node_id", `worker:${py.toStr(index)}`))), "runtime": py.toStr(py.get(node, "runtime", "browser")), "synced": py.truthy(py.get(node, "synced", true)), "bounded": true});
  }
  return py.sorted(workers, {key: ((item: any) => py.at(item, "worker_id")) as (item: any) => any});
}
