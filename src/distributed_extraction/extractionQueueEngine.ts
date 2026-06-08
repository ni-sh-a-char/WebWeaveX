/**
 * Converted from Python: core/distributed_extraction/extraction_queue_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_QUEUE_SIZE: any = 10000;
export function enqueueExtraction(queue: any, task: any): any {
  var bounded: any = py.slice([...py.iter(queue)], null, MAX_QUEUE_SIZE);
  var task_id: any = py.toStr(py.get(task, "task_id", `task_${py.toStr(py.len(bounded))}`));
  var entry: any = {"task_id": task_id, "url": py.toStr(py.get(task, "url", "")), "priority": py.toInt(py.get(task, "priority", 0)), "order": py.len(bounded), "bounded": true};
  py.listAppend(bounded, entry);
  bounded = py.sorted(bounded, {key: ((item: any) => [(-py.toInt(py.get(item, "priority", 0))), py.toInt(py.get(item, "order", 0)), py.toStr(py.get(item, "task_id", ""))]) as (item: any) => any});
  return {"queue": py.slice(bounded, null, MAX_QUEUE_SIZE), "enqueued": task_id, "bounded": true};
}
export function dequeueExtraction(queue: any): any {
  var bounded: any = py.sorted([...py.iter(queue)], {key: ((item: any) => [(-py.toInt(py.get(item, "priority", 0))), py.toInt(py.get(item, "order", 0)), py.toStr(py.get(item, "task_id", ""))]) as (item: any) => any});
  if (!py.truthy(bounded)) {
    return {"task": null, "queue": [], "bounded": true};
  }
  var task: any = py.at(bounded, 0);
  var remaining: any = py.slice(bounded, 1, null);
  return {"task": task, "queue": remaining, "bounded": true};
}
