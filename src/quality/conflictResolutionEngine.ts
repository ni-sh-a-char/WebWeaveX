/**
 * Converted from Python: core/quality/conflict_resolution_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function resolveConflicts(values: any): any {
  var uniq: any = py.sorted(py.toSet(py.or2(values, () => ([]))));
  return {"resolved": uniq, "conflicts": py.max([0, py.sub(py.len(py.or2(values, () => ([]))), py.len(uniq))])};
}
