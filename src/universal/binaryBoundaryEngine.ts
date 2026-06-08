/**
 * Converted from Python: core/universal/binary_boundary_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function detectBinaryBoundary(payload: any): any {
  var data: any = ((typeof payload === "string") ? py.encode(payload, "utf-8") : py.or2(payload, () => (new py.PyBytes(""))));
  return {"is_binary": (py.count(py.slice(data, null, 2048), 0) > 0), "size": py.len(data)};
}
