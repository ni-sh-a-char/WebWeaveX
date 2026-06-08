/**
 * Converted from Python: core/adaptive/extraction_consistency_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function verifyExtractionConsistency(previous: any, current: any): any {
  var previous_fields: any = py.toSet(py.get(previous, "fields", []));
  var current_fields: any = py.toSet(py.get(current, "fields", []));
  return {"stable": py.eq(previous_fields, current_fields), "added": py.sorted(py.sub(current_fields, previous_fields)), "removed": py.sorted(py.sub(previous_fields, current_fields)), "bounded": true};
}
