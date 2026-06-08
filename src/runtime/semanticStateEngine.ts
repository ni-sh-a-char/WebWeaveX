/**
 * Converted from Python: core/runtime/semantic_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "./pyCompat.js";

export function trackSemanticState(ir: any, stage: any = "runtime"): any {
  var lineage: any = py.or2(py.get(ir, "lineage", {}), () => ({}));
  var stages: any = ((Array.isArray(py.get(lineage, "stages"))) ? [...py.iter(py.get(lineage, "stages", []))] : []);
  py.listAppend(stages, {"stage": stage});
  return {...(ir), "lineage": {...(lineage), "stages": stages, "depth": py.len(stages)}};
}
