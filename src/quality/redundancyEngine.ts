/**
 * Converted from Python: core/quality/redundancy_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function computeRedundancy(items: any): any {
  var total: any = py.len(py.or2(items, () => ([])));
  var unique: any = py.len(py.toSet(py.or2(items, () => ([]))));
  return {"total": total, "unique": unique, "redundancy": py.max([0, py.sub(total, unique)])};
}
