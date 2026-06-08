/**
 * Converted from Python: core/evidence/lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildLineage(stages: any): any {
  var chain: any[] = [];
  var idx: any;
  var stage: any;
  for ([idx, stage] of py.enumerate(py.or2(stages, () => ([])))) {
    if (!((stage !== null && typeof stage === "object" && !Array.isArray(stage) && !(stage instanceof Set) && !(stage instanceof Map)))) {
      continue;
    }
    py.listAppend(chain, {"step": idx, "stage": py.get(stage, "stage", `step_${py.toStr(idx)}`), "inputs": ((Array.isArray(py.get(stage, "inputs"))) ? py.sorted(py.get(stage, "inputs", [])) : []), "outputs": ((Array.isArray(py.get(stage, "outputs"))) ? py.sorted(py.get(stage, "outputs", [])) : [])});
  }
  return {"stages": chain, "depth": py.len(chain)};
}
