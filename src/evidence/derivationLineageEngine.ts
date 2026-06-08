/**
 * Converted from Python: core/evidence/derivation_lineage_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildLineage } from "./lineageEngine.js";

export function trackDerivation(steps: any, inputs: any, outputs: any): any {
  var stages: any = py.iter(py.sorted(py.toSet(py.or2(steps, () => ([]))))).map((step: any) => ({"stage": step, "inputs": py.sorted(inputs), "outputs": py.sorted(outputs)}));
  return buildLineage(stages);
}
export { buildLineage };
