/**
 * Converted from Python: core/native/native_replay_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function replayNativeRuntime(memory: any): any {
  return {"windows": py.get(memory, "windows", {}), "dialogs": py.get(py.get(memory, "accessibility_trees", {}), "dialogs", []), "interactions": py.get(memory, "interactions", []), "terminal_flows": py.get(memory, "terminal_streams", {}), "electron_routes": py.get(py.get(memory, "electron_state", {}), "routes", []), "ui_graph": py.get(memory, "runtime_graphs", {}), "replayed": true, "bounded": true};
}
