/**
 * Converted from Python: core/synchronization/runtime_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffRuntimeState(previous: any, current: any): any {
  var runtime_changes: any[] = [];
  var semantic_mutations: any[] = [];
  var workflow_mutations: any[] = [];
  var distributed_changes: any[] = [];
  var key: any;
  for (key of py.iter(py.sorted(py.bitor(py.toSet(py.keys(previous)), py.toSet(py.keys(current)))))) {
    if (py.eq(py.get(previous, key), py.get(current, key))) {
      continue;
    }
    var entry: any = {"field": key, "from": py.get(previous, key), "to": py.get(current, key)};
    if (py.contains(key, "semantic")) {
      py.listAppend(semantic_mutations, entry);
    } else if (py.contains(key, "workflow")) {
      py.listAppend(workflow_mutations, entry);
    } else if ((py.contains(key, "distributed") || py.contains(key, "worker"))) {
      py.listAppend(distributed_changes, entry);
    } else {
      py.listAppend(runtime_changes, entry);
    }
  }
  return {"runtime_changes": runtime_changes, "semantic_mutations": semantic_mutations, "workflow_mutations": workflow_mutations, "distributed_changes": distributed_changes, "bounded": true};
}
