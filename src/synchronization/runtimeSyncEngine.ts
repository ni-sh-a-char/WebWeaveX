/**
 * Converted from Python: core/synchronization/runtime_sync_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let RUNTIME_SYNC_HANDLERS: any = ["browser", "electron", "terminal", "vm", "remote"];
export function synchronizeRuntime(snapshots: any, tick: any = 0): any {
  var synchronized: any[] = [];
  var runtime: any;
  for (runtime of py.iter(RUNTIME_SYNC_HANDLERS)) {
    var payload: Record<string, any> = {};
    var snapshot: any;
    for (snapshot of py.iter(snapshots)) {
      var key: any = (!py.eq(runtime, "browser") ? `${py.toStr(runtime)}_runtime` : "browser_runtime");
      if (py.eq(runtime, "electron")) {
        key = "native_runtime";
      }
      var value: any = py.get(snapshot, key, py.get(snapshot, "native_runtime", {}));
      if (py.truthy(value)) {
        payload = {...(payload), ...((((value !== null && typeof value === "object" && !Array.isArray(value) && !(value instanceof Set) && !(value instanceof Map))) ? value : {"data": value}))};
      }
    }
    py.listAppend(synchronized, {"runtime": runtime, "synced": py.truthy(payload), "tick": tick, "handler": `sync_${py.toStr(runtime)}`});
  }
  return {"synchronized": synchronized, "count": py.len(py.iter(synchronized).filter((item: any) => py.truthy(py.at(item, "synced"))).map((item: any) => item)), "bounded": true};
}
