/**
 * Converted from Python: core/causality/electron_terminal_bridge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function bridgeElectronTerminalRuntime(electron_events: any, terminal_events: any): any {
  var bridges: any[] = [];
  var electron_ref: any = (py.truthy(electron_events) ? py.at(electron_events, (-1)) : {"id": "electron:root"});
  var index: any;
  var terminal_event: any;
  for ([index, terminal_event] of py.enumerate(py.slice(terminal_events, null, 5000))) {
    py.listAppend(bridges, {"from_runtime": "electron", "to_runtime": "terminal", "from_event": py.toStr(py.get(electron_ref, "id", "")), "to_event": py.toStr(py.get(terminal_event, "id", `terminal:${py.toStr(index)}`)), "relation": "triggers", "step": index});
  }
  return {"bridges": bridges, "synchronization_chain": py.iter(bridges).map((b: any) => py.at(b, "to_event")), "bounded": true};
}
