/**
 * Converted from Python: core/execution_physics/semantic_runtime_friction_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_FRICTION: any = 100000;
export function computeRuntimeFriction(runtime_ir: any): any {
  var conflicts: any = py.get(runtime_ir, "runtime_conflicts", {});
  var conflict_count: any = py.len((((conflicts !== null && typeof conflicts === "object" && !Array.isArray(conflicts) && !(conflicts instanceof Set) && !(conflicts instanceof Map))) ? py.get(conflicts, "conflicts", []) : []));
  var friction: any = py.min([py.mul(conflict_count, 10), MAX_FRICTION]);
  return {"friction": friction, "conflict_count": conflict_count, "bounded": true};
}
