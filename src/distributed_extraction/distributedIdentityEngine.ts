/**
 * Converted from Python: core/distributed_extraction/distributed_identity_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function routeBrowserIdentity(workers: any): any {
  var routes: any[] = [];
  var worker: any;
  for (worker of py.iter(workers)) {
    var identity: any = py.get(worker, "identity", {});
    py.listAppend(routes, {"worker_id": py.toStr(py.get(worker, "worker_id", "")), "profile_id": py.toStr(py.get(identity, "profile_id", "default")), "fingerprint_hash": py.toStr(py.get(identity, "fingerprint_hash", ""))});
  }
  return {"routes": py.sorted(routes, {key: ((item: any) => py.at(item, "worker_id")) as (item: any) => any}), "bounded": true};
}
