/**
 * Converted from Python: core/execution_physics/distributed_runtime_inertia_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_INERTIA: any = 100000;
export function computeRuntimeInertia(runtime_ir: any): any {
  var momentum: any = py.toInt((((py.get(runtime_ir, "semantic_momentum") !== null && typeof py.get(runtime_ir, "semantic_momentum") === "object" && !Array.isArray(py.get(runtime_ir, "semantic_momentum")) && !(py.get(runtime_ir, "semantic_momentum") instanceof Set) && !(py.get(runtime_ir, "semantic_momentum") instanceof Map))) ? py.get(py.get(runtime_ir, "semantic_momentum", {}), "runtime_momentum", 0) : py.get(runtime_ir, "runtime_momentum", 0)));
  var workers: any = py.len([...py.iter(py.or2(py.get(runtime_ir, "distributed_workers", []), () => ([])))]);
  var inertia: any = py.min([py.mul(momentum, py.max([workers, 1])), MAX_INERTIA]);
  return {"runtime_inertia": inertia, "worker_count": workers, "bounded": true};
}
