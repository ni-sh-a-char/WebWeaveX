/**
 * Converted from Python: core/universal/binary_boundary_v4_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function inspectBinaryBoundary(payload: any): any {
  var data: any = ((typeof payload === "string") ? py.encode(payload, "utf-8") : py.or2(payload, () => (new py.PyBytes(""))));
  return {"size": py.len(data), "has_null_byte": py.contains(py.slice(data, null, 4096), 0)};
}
