/**
 * Converted from Python: core/execution_physics/semantic_pressure_field_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FIELD: any = 1000;
export function buildPressureField(runtime_ir: any): any {
  var workers_raw: any = py.get(runtime_ir, "distributed_workers", []);
  if (((workers_raw !== null && typeof workers_raw === "object" && !Array.isArray(workers_raw) && !(workers_raw instanceof Set) && !(workers_raw instanceof Map)))) {
    var workers: any = [...py.iter(py.get(workers_raw, "assignments", []))];
  } else {
    workers = [...py.iter(workers_raw)];
  }
  var field: any[] = [];
  var worker: any;
  for (worker of py.iter(py.slice(workers, null, MAX_FIELD))) {
    var worker_key: any = (((worker !== null && typeof worker === "object" && !Array.isArray(worker) && !(worker instanceof Set) && !(worker instanceof Map))) ? py.toStr(py.get(worker, "worker")) : py.toStr(worker));
    py.listAppend(field, {"worker": worker_key, "pressure": 1});
  }
  return {"pressure_field": py.sorted(field, {key: ((x: any) => py.at(x, "worker")) as (item: any) => any}), "bounded": true};
}
