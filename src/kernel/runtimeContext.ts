/**
 * Converted from Python: core/kernel/runtime_context.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeContext(runtime_type: any = "browser", tick: any = 0, sources: any = null, policy: any = null): any {
  sources = py.or2(sources, () => ({}));
  return {"runtime_type": runtime_type, "tick": tick, "sources": py.pyDict(sources), "policy": py.pyDict(py.or2(policy, () => ({}))), "phase_state": {}, "bounded": true};
}
