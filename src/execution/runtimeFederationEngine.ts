/**
 * Converted from Python: core/execution/runtime_federation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeWorkers } from "./runtimeWorkerEngine.js";

export function federateRuntimeExecution(workers: any, actions: any = null): any {
  var built: any = buildRuntimeWorkers(workers);
  var routes: any[] = [];
  var index: any;
  var worker: any;
  for ([index, worker] of py.enumerate(built)) {
    var action: any = (py.truthy(actions) ? py.at(py.or2(actions, () => ([{}])), py.mod(index, py.max([py.len(py.or2(actions, () => ([{}]))), 1]))) : {});
    py.listAppend(routes, {"worker_id": py.at(worker, "worker_id"), "runtime": py.at(worker, "runtime"), "action_id": py.toStr(py.get(action, "id", `route:${py.toStr(index)}`)), "route_order": index});
  }
  return {"workers": built, "execution_routes": py.sorted(routes, {key: ((item: any) => py.at(item, "route_order")) as (item: any) => any}), "federated": true, "bounded": true};
}
export { buildRuntimeWorkers };
