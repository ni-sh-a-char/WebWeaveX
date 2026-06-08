/**
 * Converted from Python: core/serialize/float_normalization_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function normalizeFloat(value: any): any {
  if ((py.truthy(Number.isNaN(value)) || py.truthy((value === Infinity || value === -Infinity)))) {
    return py.F(0.0);
  }
  return py.toFloat(py.format(value, ".15g"));
}
