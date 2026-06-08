/**
 * Converted from Python: core/autonomy/semantic_constraint_solver.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function solveSemanticConstraints(constraints: any): any {
  var valid: any[] = [];
  var invalid: any[] = [];
  var constraint: any;
  for (constraint of py.iter(constraints)) {
    if (py.truthy(py.get(constraint, "valid", true))) {
      py.listAppend(valid, constraint);
    } else {
      py.listAppend(invalid, constraint);
    }
  }
  return {"valid_constraints": valid, "invalid_constraints": invalid};
}
