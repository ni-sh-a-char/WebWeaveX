/**
 * Converted from Python: core/native/native_process_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function enumerateNativeProcesses(snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var processes: any = py.slice([...py.iter(py.get(snap, "processes", []))], null, 10000);
  return {"processes": py.sorted(processes, {key: ((item: any) => py.toStr(py.get(item, "name", py.get(item, "pid", "")))) as (item: any) => any}), "count": py.len(processes), "bounded": true};
}
