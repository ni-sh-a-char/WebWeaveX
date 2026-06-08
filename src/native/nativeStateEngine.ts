/**
 * Converted from Python: core/native/native_state_engine.py
 * @generated — WebWeaveX python→javascript library port
 */

import * as py from "../runtime/pyCompat.js";

export function buildNativeState(runtime: any, windows: any, desktop: any, focused_element: any = null): any {
  return {"runtime": runtime, "focused_window": py.get(windows, "focused_window", ""), "window_count": py.len(py.get(windows, "windows", [])), "active_apps": py.get(desktop, "active_apps", []), "dialogs": py.get(desktop, "dialogs", []), "notifications": py.get(desktop, "notifications", []), "focused_element": py.or2(focused_element, () => ({})), "bounded": true};
}
