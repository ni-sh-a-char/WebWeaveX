/**
 * Converted from Python: core/evolution_runtime/runtime_adaptation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function adaptRuntimeStrategy(strategy: any, optimization: any): any {
  var adapted: any = py.pyDict(strategy);
  if (py.truthy(py.get(optimization, "convergence_gain"))) {
    py.setItem(adapted, "synchronization_path", "continuous");
  }
  if ((py.get(optimization, "runtime_pressure", 0) > 0)) {
    py.setItem(adapted, "extraction_path", "repair_then_extract");
  }
  py.setItem(adapted, "adapted", true);
  py.setItem(adapted, "bounded", true);
  return adapted;
}
