/**
 * Converted from Python: core/evolution_runtime/runtime_diff_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function diffEvolutionRuntime(previous: any, current: any): any {
  var prev_id: any = py.toStr(py.get(previous, "evolution_id", ""));
  var curr_id: any = py.toStr(py.get(current, "evolution_id", ""));
  return {"evolution_changed": !py.eq(prev_id, curr_id), "previous_id": prev_id, "current_id": curr_id, "mutation_delta": py.sub(py.len(py.get(current, "mutations", [])), py.len(py.get(previous, "mutations", []))), "revertible": true, "bounded": true};
}
