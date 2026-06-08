/**
 * Converted from Python: core/kernel/runtime_boundary.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_PAYLOAD_BYTES: any = 50000000;
export let MAX_IR_COUNT: any = 10000;
export function enforceRuntimeBoundary(payload: any): any {
  var size: any = py.len(py.jsonDumps(payload, {sortKeys: true, defaultStr: true}));
  var ir_count: any = py.len(py.get(payload, "irs", []));
  return {"within_size": py.le(size, MAX_PAYLOAD_BYTES), "within_ir_count": py.le(ir_count, MAX_IR_COUNT), "size": size, "ir_count": ir_count, "bounded": true};
}
