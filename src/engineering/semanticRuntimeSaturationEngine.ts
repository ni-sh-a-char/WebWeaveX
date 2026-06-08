/**
 * Converted from Python: core/engineering/semantic_runtime_saturation_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let MAX_SATURATION: any = 100000;
export function measureRuntimeSaturation(runtime_ir: any): any {
  var size: any = py.len(runtime_ir);
  return {"saturated": py.ge(size, MAX_SATURATION), "runtime_size": size};
}
