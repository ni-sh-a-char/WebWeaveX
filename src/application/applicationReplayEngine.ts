/**
 * Converted from Python: core/application/application_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replayApplicationRuntime(memory: any): any {
  return {"application_state": py.get(memory, "application_state", {}), "workflows": py.get(memory, "workflows", {}), "routes": py.get(memory, "navigation_flows", {}), "forms": py.get(memory, "forms", {}), "action_graphs": py.get(memory, "action_graphs", {}), "objectives": py.get(memory, "objectives", []), "replayed": true, "bounded": true};
}
