/**
 * Converted from Python: core/semantic/contradiction_restraint_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { computeContradictionPressure } from "./contradictionPressureEngine.js";

export function applyContradictionRestraint(bundle: any): any {
  var contradicted: any = py.or2(py.get(bundle, "contradicted", {}), () => (py.or2(py.get(bundle, "contradictions", {}), () => ({}))));
  var pressure: any = computeContradictionPressure(contradicted);
  py.setItem(bundle, "contradiction_pressure", pressure);
  py.setItem(bundle, "fragility_pressure", {...(py.get(bundle, "fragility_pressure", {})), "contradiction": py.at(pressure, "pressure")});
  return bundle;
}
export { computeContradictionPressure };
