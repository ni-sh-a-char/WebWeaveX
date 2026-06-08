/**
 * Converted from Python: core/memory/runtime_convergence_memory_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function convergeRuntimeMemory(replicas: any): any {
  if (!py.truthy(replicas)) {
    return {"converged": true, "memory_id": "", "bounded": true};
  }
  var base: any = py.at(replicas, 0);
  var replica: any;
  for (replica of py.iter(py.slice(replicas, 1, null))) {
    if (!py.eq(py.get(replica, "memory_id"), py.get(base, "memory_id"))) {
      return {"converged": false, "conflict": true, "bounded": true};
    }
  }
  return {"converged": true, "memory_id": py.get(base, "memory_id", ""), "replica_count": py.len(replicas), "bounded": true};
}
