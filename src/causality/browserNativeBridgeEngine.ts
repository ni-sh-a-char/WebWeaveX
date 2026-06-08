/**
 * Converted from Python: core/causality/browser_native_bridge_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function bridgeBrowserNativeRuntime(browser_events: any, native_events: any): any {
  var bridges: any[] = [];
  var step: any = py.len(browser_events);
  var index: any;
  var native_event: any;
  for ([index, native_event] of py.enumerate(py.slice(native_events, null, 5000))) {
    var source: any = (py.truthy(browser_events) ? py.at(browser_events, (-1)) : {"id": "browser:root"});
    py.listAppend(bridges, {"from_runtime": "browser", "to_runtime": py.toStr(py.get(native_event, "runtime", "desktop")), "from_event": py.toStr(py.get(source, "id", "")), "to_event": py.toStr(py.get(native_event, "id", `native:${py.toStr(index)}`)), "relation": "propagates", "step": py.add(step, index)});
  }
  return {"bridges": bridges, "chain_length": py.len(bridges), "bounded": true};
}
