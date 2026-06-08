/**
 * Converted from Python: core/native/native_stream_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function captureNativeStreams(terminal: any = null, desktop: any = null, electron: any = null, mutations: any = null): any {
  terminal = py.or2(terminal, () => ({}));
  desktop = py.or2(desktop, () => ({}));
  electron = py.or2(electron, () => ({}));
  mutations = [...py.iter(py.or2(mutations, () => ([])))];
  return {"terminal_streams": (py.truthy(terminal) ? [{"stream_id": py.get(terminal, "stream_id", ""), "lines": py.len(py.get(terminal, "output", []))}] : []), "notifications": [...py.iter(py.get(desktop, "notifications", []))], "electron_updates": [...py.iter(py.get(electron, "routes", []))], "mutations": py.slice(mutations, null, 10000), "bounded": true};
}
