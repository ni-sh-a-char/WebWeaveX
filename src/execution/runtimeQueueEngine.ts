/**
 * Converted from Python: core/execution/runtime_queue_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_QUEUE: any = 100000;
export function enqueueRuntimeAction(queue: any, action: any, priority: any = 0): any {
  var updated: any = [...py.iter(queue)];
  var entry: any = {"action": action, "priority": priority, "order": py.len(updated)};
  py.listAppend(updated, entry);
  updated = py.slice(py.sorted(updated, {key: ((item: any) => [(-py.toInt(py.get(item, "priority", 0))), py.toInt(py.get(item, "order", 0))]) as (item: any) => any}), null, MAX_QUEUE);
  return {"queue": updated, "size": py.len(updated), "bounded": true};
}
export function dequeueRuntimeAction(queue: any): any {
  if (!py.truthy(queue)) {
    return {"queue": [], "action": null, "bounded": true};
  }
  var ordered: any = py.sorted(queue, {key: ((item: any) => [(-py.toInt(py.get(item, "priority", 0))), py.toInt(py.get(item, "order", 0))]) as (item: any) => any});
  var head: any = py.at(ordered, 0);
  var rest: any = py.slice(ordered, 1, null);
  return {"queue": rest, "action": py.get(head, "action"), "bounded": true};
}
