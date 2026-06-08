/**
 * Converted from Python: core/runtime/semantic_worker_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export let MAX_WORKERS: any = 16;
export function runSemanticWorkers(tasks: any, handler: any): any {
  var results: any[] = [];
  var task: any;
  for (task of py.iter(py.slice(tasks, null, MAX_WORKERS))) {
    py.listAppend(results, handler(task));
  }
  return py.sorted(results, {key: ((r: any) => py.toStr(py.get(r, "id", ""))) as (item: any) => any});
}
