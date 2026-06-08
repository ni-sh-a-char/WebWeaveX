/**
 * Converted from Python: core/execution/runtime_action_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildRuntimeAction(action_type: any, runtime: any, payload: any = null, tick: any = 0): any {
  payload = py.pyDict(py.or2(payload, () => ({})));
  var canonical: any = py.jsonDumps({"runtime": runtime, "action_type": action_type, "payload": payload, "tick": tick}, {sortKeys: true});
  var action_id: any = py.slice(py.hashNew("sha256", py.encode(canonical, "utf-8")).hexdigest(), null, 32);
  return {"id": action_id, "runtime": runtime, "action_type": action_type, "payload": payload, "timestamp": tick, "bounded": true};
}
