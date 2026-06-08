/**
 * Converted from Python: core/native/native_vm_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let VM_BACKENDS: any = ["virtualbox", "vmware", "qemu", "hyper-v"];
export function extractVmRuntime(backend: any = "qemu", snapshot: any = null): any {
  var snap: any = py.or2(snapshot, () => ({}));
  var normalized: any = py.replace(String(backend).toLowerCase(), "_", "-");
  if ((!py.contains(VM_BACKENDS, normalized) && !py.eq(normalized, "hyperv"))) {
    normalized = "qemu";
  }
  return {"backend": normalized, "vm_state": py.toStr(py.get(snap, "vm_state", "stopped")), "window_streams": [...py.iter(py.get(snap, "window_streams", []))], "active_sessions": [...py.iter(py.get(snap, "active_sessions", []))], "metadata": py.pyDict(py.get(snap, "metadata", {})), "bounded": true};
}
