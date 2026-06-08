/**
 * Converted from Python: core/distributed_extraction/extraction_scheduler_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SCHEDULED: any = 5000;
export let DEFAULT_COOLDOWN: any = 5;
export function scheduleExtractionRuntime(tasks: any, tick: any = 0): any {
  var scheduled: any[] = [];
  var index: any;
  var task: any;
  for ([index, task] of py.enumerate(py.slice(tasks, null, MAX_SCHEDULED))) {
    var priority: any = py.toInt(py.get(task, "priority", 0));
    var retries: any = py.toInt(py.get(task, "retries", 0));
    var cooldown: any = py.toInt(py.get(task, "cooldown", DEFAULT_COOLDOWN));
    var pacing: any = py.toInt(py.get(task, "pacing", 1));
    var run_at: any = py.add(py.add(tick, py.mul(cooldown, retries)), py.mul(pacing, index));
    py.listAppend(scheduled, {"task_id": py.toStr(py.get(task, "task_id", `task_${py.toStr(index)}`)), "url": py.toStr(py.get(task, "url", "")), "priority": priority, "run_at": run_at, "retries": retries, "bounded": true});
  }
  scheduled = py.sorted(scheduled, {key: ((item: any) => [py.toInt(py.get(item, "run_at", 0)), (-py.toInt(py.get(item, "priority", 0))), py.toStr(py.get(item, "task_id", ""))]) as (item: any) => any});
  return {"scheduled": scheduled, "tick": tick, "bounded": true};
}
