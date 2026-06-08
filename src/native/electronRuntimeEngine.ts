/**
 * Converted from Python: core/native/electron_runtime_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export let ELECTRON_APPS: any = {"discord": {"routes": ["/channels/@me"], "storage_keys": ["token", "user"]}, "slack": {"routes": ["/client"], "storage_keys": ["team", "user"]}, "vscode": {"routes": ["/workspace"], "storage_keys": ["workspace"]}, "notion": {"routes": ["/"], "storage_keys": ["user"]}, "figma": {"routes": ["/file"], "storage_keys": ["file"]}};
export function extractElectronRuntime(application: any = "", snapshot: any = null): any {
  var app_key: any = py.strip(String(application).toLowerCase());
  var profile: any = py.get(ELECTRON_APPS, app_key, {"routes": ["/"], "storage_keys": []});
  var snap: any = py.or2(snapshot, () => ({}));
  return {"application": py.or2(app_key, () => ("electron")), "chromium_runtime": {"version": py.toStr(py.get(snap, "chromium_version", "structural")), "bounded": true}, "routes": py.sorted([...py.iter(py.get(snap, "routes", py.get(profile, "routes", [])))], {key: (py.toStr) as (item: any) => any}), "internal_storage": py.pyDict(py.get(snap, "internal_storage", {})), "indexed_db": py.slice([...py.iter(py.get(snap, "indexed_db", []))], null, 1000), "windows": [...py.iter(py.get(snap, "windows", []))], "preload_state": py.pyDict(py.get(snap, "preload_state", {})), "bounded": true};
}
