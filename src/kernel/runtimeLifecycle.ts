/**
 * Converted from Python: core/kernel/runtime_lifecycle.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";
import { buildRuntimeContext } from "./runtimeContext.js";
import { buildKernelPolicy } from "./runtimePolicy.js";
import { buildKernelState } from "./runtimeState.js";

export function initializeRuntime(runtime_type: any = "browser", tick: any = 0): any {
  var context: any = buildRuntimeContext(runtime_type, tick);
  var policy: any = buildKernelPolicy();
  var state: any = buildKernelState(context);
  return {"context": context, "policy": policy, "state": state, "initialized": true, "bounded": true};
}
export function shutdownRuntime(state: any): any {
  return {"shutdown": true, "final_tick": py.toInt(py.get(state, "tick", 0)), "bounded": true};
}
export { buildKernelPolicy, buildKernelState, buildRuntimeContext };
