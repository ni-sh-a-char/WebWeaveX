/**
 * Converted from Python: core/execution/runtime_scheduler_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function scheduleRuntimeExecution(actions: any, priorities: any = null, cooldown_ticks: any = 0, worker_id: any = "worker:0", tick: any = 0): any {
  priorities = py.or2(priorities, () => ({}));
  var scheduled: any[] = [];
  var index: any;
  var action: any;
  for ([index, action] of py.enumerate(py.slice(actions, null, 10000))) {
    var action_id: any = py.toStr(py.get(action, "id", `action:${py.toStr(index)}`));
    var priority: any = py.toInt(py.get(priorities, action_id, 0));
    py.listAppend(scheduled, {"action": action, "priority": priority, "worker_id": worker_id, "tick": py.add(tick, py.mul(index, py.max([cooldown_ticks, 0]))), "retry": 0, "paced": true});
  }
  scheduled = py.sorted(scheduled, {key: ((item: any) => [(-py.at(item, "priority")), py.at(item, "tick"), py.toStr(py.get(py.at(item, "action"), "id", ""))]) as (item: any) => any});
  return {"scheduled": scheduled, "worker_id": worker_id, "cooldown_ticks": cooldown_ticks, "deterministic": true, "bounded": true};
}
