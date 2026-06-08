/**
 * Converted from Python: core/distributed_extraction/distributed_session_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function routeAuthenticatedSessions(workers: any): any {
  var routes: any[] = [];
  var worker: any;
  for (worker of py.iter(workers)) {
    var worker_id: any = py.toStr(py.get(worker, "worker_id", ""));
    var session: any = py.get(py.get(worker, "runtime_state", {}), "session", {});
    py.listAppend(routes, {"worker_id": worker_id, "session_fingerprint": py.toStr(py.get(session, "session_fingerprint", worker_id)), "isolated": true});
  }
  return {"routes": py.sorted(routes, {key: ((item: any) => py.at(item, "worker_id")) as (item: any) => any}), "bounded": true};
}
